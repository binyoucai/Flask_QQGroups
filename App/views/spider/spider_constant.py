headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.59 QQ/8.9.3.21169 Safari/537.36'
}

# 状态码
HTTP_NOT_CERTIFICATION = 0  # 没有扫码
HTTP_NOT_EXPIRED = 4  # 二维码未失效
HTTP_IN_CERTIFICATION = 1  # 扫码中
HTTP_LOGINED = 2  # 扫码登陆成功
HTTP_EXPIRED = 3  # 二维码已过期


# 防盗链
sourceURL = 'http://find.qq.com/index.html?version=1&im_version=5533&width=910&height=610&search_target=0'

# 登陆
login_url = 'http://ui.ptlogin2.qq.com/cgi-bin/login'

# 二维码
qrcode_ptqrshow_url = 'http://ptlogin2.qq.com/ptqrshow'

# 验证扫码登陆
ptqrlogin_url = 'http://ptlogin2.qq.com/ptqrlogin'

# 搜索
pc_group_search_url = 'http://qun.qq.com/cgi-bin/group_search/pc_group_search'

# 分组名
groups = [(u'群名称', u'群号', u'群人数', u'群上限',
           u'群主', u'地域', u'分类', u'标签', u'群简介')]
