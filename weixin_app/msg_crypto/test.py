"""
@Author  : monabai
@Time    : 2018/8/22 17:51
@Software: PyCharm
@File    : test.py
"""

if __name__ == "__main__":
    from WXBizMsgCrypt import WXBizMsgCrypt
    """ 
    1.第三方回复加密消息给公众平台；
    2.第三方收到公众平台发送的消息，验证消息的安全性，并对消息进行解密。
    """
    encodingAESKey = "B56slIjnkNC0V7QiP3w0OUXdnXBLdhXTEvkVRXnfQNo"
    to_xml = """ <xml><ToUserName><![CDATA[oia2TjjewbmiOUlr6X-1crbLOvLw]]></ToUserName><FromUserName><![CDATA[gh_7f083739789a]]></FromUserName><CreateTime>1407743423</CreateTime><MsgType>  <![CDATA[video]]></MsgType><Video><MediaId><![CDATA[eYJ1MbwPRJtOvIEabaxHs7TX2D-HV71s79GUxqdUkjm6Gs2Ed1KF3ulAOA9H1xG0]]></MediaId><Title><![CDATA[testCallBackReplyVideo]]></Title><Descript  ion><![CDATA[testCallBackReplyVideo]]></Description></Video></xml>"""
    token = "abcdef"
    nonce = "1320562132"
    appid = "wx1a5d1d7cd4fedd7b"

    # 测试加密接口
    print()
    encryp_test = WXBizMsgCrypt(token, encodingAESKey, appid)
    ret, encrypt_xml = encryp_test.EncryptMsg(to_xml, nonce)
    print('ret: ', ret)
    print('encrypt_xml: ', encrypt_xml)

    # 测试解密接口
    timestamp = "1409735669"
    signature = "d5250257bafcd531b62914ddf154aa4e2c40a33c"

    from_xml = """<xml><ToUserName><![CDATA[gh_10f6c3c3ac5a]]></ToUserName><FromUserName><![CDATA[oyORnuP8q7ou2gfYjqLzSIWZf0rs]]></FromUserName><CreateTime>1409735668</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[abcdteT]]></Content><MsgId>6054768590064713728</MsgId><Encrypt><![CDATA[b'068W4qZ2Qy6Wv2eTSxuSOTb1poqtpmb2Tb1lFERiV9gMRCmEqAD8Vtc3MWULwey2KbeTIF1DHQ8BQtNU/Ljy1kQKV5Xh/SVHNMLXAAN6jkBm9RvFhPY/uzwMvQrLK5DLC958oKTQgTptKprQspWqysD3ARj75KHiU6bNMhR/AdWOLC3C+L48P/9rY4YDjRarB8h4Sj0Lbig3e4xGIHEU9Tft3OMWVRQoUxVbF+iuvrNdGL0DiMEkUmnyHcYNAa9Y78FOf5oZqztM6rd+OAEMI3c/UotfryXVcB6TMi+axo2gl5V8C3JuPXKJ+4aTKCINU4EkuLz9WuDqutvJekDUgAw6oPs81otwsdXNM++WkKKB3oX2lXyK/LIugLjXNHnqAOeUT9RcDJfP6jX9HuZS2bMKZFzAswD5hLtNgDAhV8Bux3gVYAFax+TXez31WrjeajavnfIdbTIepl1DsXCBvDCd9aikEPh3gd1cu3ys6GgdqoWjeOSlNgKHCaXaUNlsxqYcfVu1TiSxjVWO8CgYmkjuOj816zKBVs5NFmdKflc=']]></Encrypt></xml>"""
    decrypt_test = WXBizMsgCrypt(token, encodingAESKey, appid)
    ret, decryp_xml = decrypt_test.DecryptMsg(from_xml, signature, timestamp, nonce)
    print('ret: ', ret)
    print('decryp_xml: ', decryp_xml)
