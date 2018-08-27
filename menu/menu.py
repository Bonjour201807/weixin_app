# -*- coding: utf-8 -*-
# filename: menu.py
import sys
sys.path.append('../')
import io
import requests
from weixin_app.basic import Basic
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


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
    postJson = """
    {
        "button": [
            {
                "name": "恋爱话术",
                "sub_button": [
                    {
                        "type": "click",
                        "name": "撩妹话术",
                        "key": "bonjourChat_v1_topic_0",
                        "sub_button": []
                    },
                    {
                        "type": "click",
                        "name": "精选惯例",
                        "key": "bonjourChat_v1_topic_1",
                        "sub_button": []
                    },
                    {
                        "type": "click",
                        "name": "迷你情话",
                        "key": "bonjourChat_v1_topic_2",
                        "sub_button": []
                    },
                    {
                        "type": "click",
                        "name": "恋爱策略",
                        "key": "bonjourChat_v1_topic_3",
                        "sub_button": []
                    }
                ]
            },
            {
                "name": "恋爱课程",
                "type": "view",
                "url": "https://mp.weixin.qq.com/mp/homepage?__biz=MzUzMTgwMTc3OQ%3D%3D&hid=1&sn=710fb8fdb2cb204fc199bf28c108d70b",
                "sub_button": []
            },
            {
                "name": "联系我们",
                "sub_button": [
                    {
                        "type": "click",
                        "name": "商务合作",
                        "key": "bonjourChat_v1_business",
                        "sub_button": []
                    },
                    {
                        "type": "click",
                        "name": "意见反馈",
                        "key": "bonjourChat_v1_feedback",
                        "sub_button": []
                    },
                    {
                        "type": "click",
                        "name": "贡献话术",
                        "key": "bonjourChat_v1_huashu",
                        "sub_button": []
                    },
                    {
                        "type": "view",
                        "name": "使用教程",
                        "url": "https://mp.weixin.qq.com/mp/homepage?__biz=MzUzMTgwMTc3OQ%3D%3D&hid=2&sn=109c09d3b3ba88b42856e5f26f801506",
                        "sub_button": []
                    }
                ]
            }
        ]
    }
    """
    accessToken = Basic().get_access_token()
    myMenu.delete(accessToken)
    myMenu.create(postJson.encode('utf-8'), accessToken)
