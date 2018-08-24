"""
@Author  : monabai
@Time    : 2018/8/22 16:26
@Software: PyCharm
@File    : wx_ip.py
"""
import sys
sys.path.append('../')
import os
import io
import requests
from basic import Basic
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


class WXIP(object):
    def __init__(self):
        pass

    def generate(self, accessToken):
        print('accessToken', accessToken)
        getUrl = "https://api.weixin.qq.com/cgi-bin/getcallbackip?access_token=%s" % accessToken
        response = requests.get(getUrl)
        # print('response', response.json())
        return response.json()


if __name__ == '__main__':
    wx_ip_list = WXIP()
    accessToken = Basic().get_access_token()
    # accessToken = '12_kbcGrkH5SFrENwLgK9RP0ulAqsKvFCL0D_WNJgjNvL_26YFc11rEQba5is4-FF8omDDLI-TgA7nAi9EmzaBSpnYDEl0qCDP4-Hwx6b_ujU2qiR5fVi068Nlg2IAGPThAFASBF'
    data = wx_ip_list.generate(accessToken)
    ip_list_file = os.getcwd() +'/wx_ip_list.txt'
    with open(ip_list_file, 'w', encoding='utf-8') as f:
        for item in data:
            result = ','.join(data[item])
            f.write(result)
    # with open(ip_list_file) as f:
    #     result = f.readlines()
    # if '101.91.60.105' in result[0].split(','):
    #     print('ok')
