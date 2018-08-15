# -*- coding: utf-8 -*-
# filename: basic.py
import requests
import time


class Basic:
    def __init__(self):
        self.__accessToken = ''
        self.__leftTime = 0

    def __real_get_access_token(self):
        appId = "wxe76eb9f73643f074"
        appSecret = "520cd136d20a3d33ec94e40ab4342fe9"
        getUrl = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (appId, appSecret))
        urlResp = requests.get(getUrl)
        urlResp = urlResp.json()
        self.__accessToken = urlResp['access_token']
        self.__leftTime = urlResp['expires_in']
    
    def get_access_token(self):
        if self.__leftTime < 10:
            self.__real_get_access_token()
        return self.__accessToken
    
    def run(self):
        while(True):
            if self.__leftTime > 10:
                time.sleep(2)
                self.__leftTime -= 2
            else:
                self.__real_get_access_token()
