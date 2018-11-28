import csv
import json
import re
import zipfile
from io import BytesIO, StringIO
from random import random
from time import time, sleep
from uuid import uuid4
import requests
import pyexcel as pe

from App.views.spider.spider_constant import headers, sourceURL, HTTP_NOT_EXPIRED, HTTP_IN_CERTIFICATION, HTTP_LOGINED, \
    HTTP_EXPIRED, pc_group_search_url, HTTP_NOT_CERTIFICATION, qrcode_ptqrshow_url, \
    ptqrlogin_url, login_url, groups


class QQGroups(object):
    '''
    爬取QQ群信息
    '''

    def __init__(self):
        super(QQGroups, self).__init__()
        self.js_ver = '10226'
        self.create_session()

    def create_session(self):
        '''
        会话维持创建
        :return:
        '''
        self.session = requests.Session()
        self.session.headers.update(headers)
        return self.session

    def get_qrcode(self):
        '''
        获取二维码
        :return:
        '''
        self.create_session()
        try:
            params = {
                'appid': '715030901',
                'daid': '73',
                'pt_no_auth': '1',
                's_url': sourceURL
            }
            response = self.session.get(login_url, params=params, timeout=1000)
            pattern = r'imgcache\.qq\.com/ptlogin/ver/(\d+)/js'
            try:
                self.js_ver = re.search(pattern, response.content).group(1)
            except:
                pass
            self.session.headers.update({'Referer': login_url})
            params = {
                'appid': '715030901',
                'e': '2',
                'l': 'M',
                's': '3',
                'd': '72',
                'v': '4',
                't': '%.17f' % (random()),
                'daid': '73'
            }
            response = self.session.get(qrcode_ptqrshow_url, params=params, timeout=1000)
        except:
            response = None
        return response

    def do_login(self):
        '''
        扫码之后的参数构造过程，扫码之后获得令牌，用令牌再构造真实登陆过程，即登陆的完整过程
        :return: dict
        '''
        login_sig = self.session.cookies.get_dict().get('pt_login_sig', '')
        qrsig = self.session.cookies.get_dict().get('qrsig', '')
        status = HTTP_NOT_CERTIFICATION
        errorMsg = ''
        status_code = None
        if all([login_sig, qrsig]):
            params = {
                'u1': sourceURL,
                'ptqrtoken': self.genqrtoken(qrsig),
                'ptredirect': '1',
                'h': '1',
                't': '1',
                'g': '1',
                'from_ui': '1',
                'ptlang': '2052',
                'action': '0-0-%d' % (time() * 1000),
                'js_ver': self.js_ver,
                'js_type': '1',
                'login_sig': login_sig,
                'pt_uistyle': '40',
                'aid': '715030901',
                'daid': '73'
            }
            try:
                response = self.session.get(ptqrlogin_url, params=params, timeout=1000)
                result = response.text
                status_code = response.status_code
                if '二维码未失效' in result:
                    status = HTTP_NOT_EXPIRED
                elif '二维码认证中' in result:
                    status = HTTP_IN_CERTIFICATION
                elif '登录成功' in result:
                    status = HTTP_LOGINED
                elif '二维码已失效' in result:
                    status = HTTP_EXPIRED
                else:
                    errorMsg = result
            except:
                errorMsg = status_code
        data = {
            'status': status,
            'time': time(),
            'errorMsg': errorMsg,
        }

        return data

    def start_search(self, sort=1, pn=1, ft='csv', kws='python'):
        '''
        模拟qq群搜索框部分，
        :param sort: 排序方式 1=默认 2=群人数 3=活跃度
        :param pn: 页码
        :param ft: ft = format 格式： json
        :param kws: 搜索关键词
        :return:
        '''
        attachments = {}
        if ft.lower() not in ['json', 'xls', 'csv']:
            return 'ft格式输入有误,请输入json xls csv其中之一,大小写都行'
        kws = kws.strip()
        kws = re.sub(r'[\r\n]', '\t', kws)
        kws = [k.strip() for k in kws.split('\t') if k.strip()]
        self.session.headers.update({'Referer': sourceURL})
        skey = self.session.cookies.get_dict().get('skey', '')

        # 压缩文件
        buff = BytesIO()
        zip_archive = zipfile.ZipFile(buff, mode='w')
        temp = []
        if ft in ['json', 'csv']:
            for i in range(len(kws)):
                temp.append(StringIO())
        else:
            for i in range(len(kws)):
                temp.append(BytesIO())

        for i, kw in enumerate(kws[:10]):
            gListRaw = []
            for page in range(0, pn):
                data = {
                    'k': u'交友',
                    'n': '8',
                    'st': '1',
                    'iso': '1',
                    'src': '1',
                    'v': '4903',
                    'bkn': self.genbkn(skey),
                    'isRecommend': 'false',
                    'city_id': '0',
                    'from': '1',
                    'keyword': kw,
                    'sort': sort,
                    'wantnum': '24',
                    'page': page,
                    'ldw': self.genbkn(skey)
                }
                response = self.session.post(pc_group_search_url, data=data, timeout=1000)
                if not response.status_code == 200:
                    data = {
                        'msg': 'QQ服务器响应'
                    }
                    return data
                result = json.loads(response.content)
                gList = result['group_list']
                gListRaw.extend(gList)
                for g in gList:
                    name = self.rmWTS(g['name'])
                    code = g['code']
                    member_num = g['member_num']
                    max_member_num = g['max_member_num']
                    owner_uin = g['owner_uin']
                    qaddr = ' '.join(g['qaddr'])
                    try:
                        gcate = ' | '.join(g['gcate'])
                    except:
                        gcate = ''
                    try:
                        _labels = [l.get('label', '') for l in g['labels']]
                        labels = self.rmWTS(' | '.join(_labels))
                    except:
                        labels = ''
                    memo = self.rmWTS(g['memo'])
                    gMeta = (name, code, member_num, max_member_num,
                             owner_uin, qaddr, gcate, labels, memo)
                    groups.append(gMeta)
                if len(gList) == 1:
                    break
                sleep(2.5)

                if ft == 'xls':
                    sheet = pe.Sheet(groups)
                    sheet.save_to_memory('xls', temp[i])
                elif ft == 'csv':
                    writer = csv.writer(temp[i], dialect='excel')
                    writer.writerows(groups)
                elif ft == 'json':
                    json.dump(gListRaw, temp[i], indent=4, sort_keys=True)
        for i in range(len(kws)):
            zip_archive.writestr((kws[i] + '.' + ft), temp[i].getvalue())
        zip_archive.close()
        token = uuid4().hex
        attachments.update({token: buff})
        return token, attachments

    def genqrtoken(self, qrsig):
        e = 0
        for i in range(0, len(qrsig)):
            e += (e << 5) + ord(qrsig[i])
        qrtoken = (e & 2147483647)
        return str(qrtoken)

    def genbkn(self, skey):
        b = 5381
        for i in range(0, len(skey)):
            b += (b << 5) + ord(skey[i])
        bkn = (b & 2147483647)
        return str(bkn)

    def rmWTS(self, content):
        pattern = r'\[em\]e\d{4}\[/em\]|&nbsp;|<br>|[\r\n\t]'
        content = re.sub(pattern, ' ', content)
        content = content.replace('&amp;', '&').strip()
        return content


if __name__ == '__main__':
    q = QQGroups()
    resut = q.get_qrcode()
