# -*- coding:utf-8 -*-

try:
    import cookielib
except:
    import http.cookiejar as cookielib
import re

import requests

session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='cookies.txt')
try:
    session.cookies.load(ignore_discard=True)
except:
    print ("cookie未能加载")

user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
headers = {
    'User-Agent': user_agent
}

def is_login():
    inbox_url = 'https://www.zhihu.com/inbox/'
    response = session.get(inbox_url, headers=headers, allow_redirects=False)
    if response.status_code is 200:
        return True
    else:
        return False

def get_xsrf():
    response = session.get('https://www.zhihu.com/', headers=headers)
    result = re.search('.*name="_xsrf" value="(.*?)"', response.text)
    if result:
        return result.group(1)
    else:
        return ''

def zhihu_login(account, password):

    post_data = {
        '_xsrf': get_xsrf(),
        'account': account,
        'password': password
    }
    if re.match(r'^1\d{10}', account):
        print('手机登录')
        post_url = 'https://www.zhihu.com/login/phone_num'
    else:
        if '@' in account:
            print('邮箱登录')
        post_url = 'https://www.zhihu.com/login/email'
    response = session.post(post_url, data=post_data, headers=headers)
    print(response.text)
    session.cookies.save()
