import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from flask import Flask, request
from flask_cors import *
import hashlib
from weixin_app.handel import Handel
from weixin_app.msg_crypto.WXBizMsgCrypt import WXBizMsgCrypt

app = Flask(__name__)
CORS(app, supports_credentials=True)

ip_list_file = 'wx_ip_list/wx_ip_list.txt'
with open(ip_list_file) as f:
    result = f.readlines()
wx_ip_list = result[0].split(',')

# 型男助理
appid = 'wx1a5d1d7cd4fedd7b'
encodingAESKey = "B56slIjnkNC0V7QiP3w0OUXdnXBLdhXTEvkVRXnfQNo"
# BonjourAI
# appid = 'wxe76eb9f73643f074'
# encodingAESKey = "mrr07UAiXDxspQ7AqMelrGR3NmRYGn1VpzXptocj9i2"
token = 'abcdef'
handel = Handel()


@app.route("/weixin/", methods=["GET", "POST"])
def index():
    ip = request.remote_addr
    if ip in wx_ip_list:
        if request.method == "GET":
            # print('request_get:', request.args)
            # print('request:', [item for item in request.args.items()])
            signature = request.args.get('signature')
            timestamp = request.args.get('timestamp')
            nonce = request.args.get('nonce')
            echostr = request.args.get('echostr')
            # print(echostr)
            return echostr
            data = [token, timestamp, nonce]
            data.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, data)
            hashcode = sha1.hexdigest()
            if hashcode == signature:
                return echostr
            else:
                return echostr
        elif request.method == 'POST':
            webData = request.stream.read()
            # print('webData: ', webData)
            # print('request.values', request.values)
            if request.values.get('encrypt_type'):
                encrypt_type = request.values.get('encrypt_type')
                if encrypt_type == 'aes':
                    # signature = request.values.get('signature')
                    timestamp = request.values.get('timestamp')
                    nonce = request.values.get('nonce')
                    # open_id = request.values.get('openid')
                    msg_signature = request.values.get('msg_signature')
                    decrypt_test = WXBizMsgCrypt(token, encodingAESKey, appid)
                    ret, decryp_xml = decrypt_test.DecryptMsg(webData, msg_signature, timestamp, nonce)
                    encrypt_xml = handel.handel_msg(decryp_xml, decrypt_test, nonce)
                    return encrypt_xml
            else:
                return handel.handel_msg(webData)
    else:
        print('非微信ip地址: ', ip)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
