import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from flask import Flask, request
from flask_cors import *
import hashlib
from handel import Handel

app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route("/weixin/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        print('request:', [item for item in request.args.items()])
        signature = request.args.get('signature')
        timestamp = request.args.get('timestamp')
        nonce = request.args.get('nonce')
        echostr = request.args.get('echostr')
        print(echostr)
        return echostr
        token = 'abcdef'
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
        print('webData: ', webData)
        return Handel().handel_msg(webData)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
