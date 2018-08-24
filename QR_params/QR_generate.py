"""
@Author  : monabai
@Time    : 2018/8/16 16:39
@Software: PyCharm
@File    : QR_generate.py
"""
import sys
sys.path.append('../')
import io
import requests
from weixin_app.basic import Basic
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


class QR(object):
    def __init__(self):
        pass

    def generate(self, postData, accessToken):
        print(accessToken)
        postUrl = "https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token=%s" % accessToken
        response = requests.post(postUrl, data=postData)
        print(response.json())


if __name__ == '__main__':
    myQR = QR()
    postJson = """
    {"action_name":"QR_LIMIT_SCENE", "action_info": {"scene": {"scene_id": 1}}}
    """
    accessToken = Basic().get_access_token()
    myQR.generate(postJson, accessToken)

    """{
        'ticket':
         'gQHl8DwAAAAAAAAAAS5odHRwOi8vd2VpeGluLnFxLmNvbS9xLzAyMDZTbDluUDRlM2kxMDAwME0wM3QAAgTRPXVbAwQAAAAA',
        'url':
            'http://weixin.qq.com/q/0206Sl9nP4e3i10000M03t'}
    """
