import io

from flask import Blueprint, send_file, jsonify, render_template, request, g

from App.views.spider.qq_groups_spider import QQGroups

qq_group_bluprint = Blueprint('qq_gourp', __name__)

q = QQGroups()

f = {}

@qq_group_bluprint.route('/index/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('qqun.html')
    elif request.method == 'POST':
        global f
        print('xxxxxxxxxxxxxx')
        sort = int(request.form.get('sort'))
        pn = int(request.form.get('pn'))
        kws = request.form.get('kws')
        ft = request.form.get('ft')
        token, attachments = q.start_search(sort=sort, pn=pn, kws=kws, ft=ft)
        f.update(attachments=attachments,token=token)

        data = {
            'msg': 'ok',
            'token': token
        }
        return jsonify(data)


@qq_group_bluprint.route('/getqrcode/')
def get_qrcode():
    '''
    获取登陆二维码
    :return: 二维码图片
    '''

    qrcode_bytes = q.get_qrcode().content
    return send_file(io.BytesIO(qrcode_bytes),
                     attachment_filename='qrcode.jpg',
                     mimetype='image/jpg')


@qq_group_bluprint.route('/login/')
def login():
    data = q.do_login()
    return jsonify(data)


@qq_group_bluprint.route('/search/', methods=['POST'])
def search():
    '''
    QQ群搜索
    :return:zip打包文件
    '''
    sort = int(request.form.get('sort'))
    pn = int(request.form.get('pn'))
    kws = request.form.get('kws')
    ft = request.form.get('ft')

    token, attachments = q.start_search(sort=sort, pn=pn, kws=kws, ft=ft)
    print(token, attachments)

    f = attachments.get(token, '')  # 得到io流
    f.seek(0)  # 绝对文件定位
    return send_file(f,
                     attachment_filename='myfile.zip',
                     mimetype='application/zip', as_attachment=True)


@qq_group_bluprint.route('/download')
def download():
    global f
    token = request.args.get('token')
    print(token)
    if not token == f.get('token'):
        return '文件不存在'
    attachments = f.get('attachments')
    f = attachments.get(token, '')  # 得到io流
    f.seek(0)  # 绝对文件定位
    return send_file(f,
                     attachment_filename='myfile.zip',
                     mimetype='application/zip', as_attachment=True)



@qq_group_bluprint.route('/test/', methods=['GET', 'POST'])
def test():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        sort = int(request.form.get('sort'))
        pn = int(request.form.get('pn'))
        kws = request.form.get('kws')
        ft = request.form.get('ft')
        print(sort, pn, kws, ft)
        token, attachments = q.start_search(sort=sort, pn=pn, kws=kws, ft=ft)
        print(token, attachments)

        f = attachments.get(token, '')  # 得到io流
        f.seek(0)  # 绝对文件定位
        return send_file(f,
                         attachment_filename='myfile.zip',
                         mimetype='application/zip', as_attachment=True)
