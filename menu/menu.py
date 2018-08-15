# -*- coding: utf-8 -*-
# filename: menu.py
import requests
from weixin_app.basic import Basic


class Menu(object):
    def __init__(self):
        pass

    def create(self, postData, accessToken):
        print(accessToken)
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % accessToken
        response = requests.post(postUrl, data=postData)
        print(response.json())

    def query(self, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/get?access_token=%s" % accessToken
        response = requests.post(postUrl)
        print(response.json())

    def delete(self, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/delete?access_token=%s" % accessToken
        response = requests.post(postUrl)
        print(response.json())

    #获取自定义菜单配置接口
    def get_current_selfmenu_info(self, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/get_current_selfmenu_info?access_token=%s" % accessToken
        response = requests.post(postUrl)
        print(response.json())


if __name__ == '__main__':
    myMenu = Menu()
    postJson = {
        "button": [
            {
                "type": "click",
                "name": "会员注册",
                "url": "http://132.232.16.50:8080"

            },
            {
                "type": "view",
                "name": "我有好句",
                "url": "http://132.232.16.50:8080"
            },
            {
                "type": "view",
                "name": "笨猪旅行",
                "url": "http://132.232.16.50:8080"
            }
        ]
    }
    # "key": "V1001_TODAY_MUSIC"
    accessToken = Basic().get_access_token()
    #myMenu.delete(accessToken)
    myMenu.create(postJson, accessToken)
