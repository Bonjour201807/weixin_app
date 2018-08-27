"""
@Author  : monabai
@Time    : 2018/8/13 16:29
@Software: PyCharm
@File    : handel.py.py
"""
import requests
from weixin_app import receive
from weixin_app import reply

reply_words = {
    'use_limit': '您今天的使用次数已经达到上限50次，欢迎明天再来使用，祝您生活愉快～',
    'no_voice_recognition': '抱歉，撩妹助理没听出来您在说什么，麻烦再说一遍[Facepalm]',
    'no_search_result': '这个问题太高深了，撩妹助理现在也不知道怎么回答[Facepalm]\n',
    'image_msg': '撩妹助理暂时还没有学会识别图片消息，我们还是先用文字交流吧[Smart]\n'
                 '当然语音也可以[Smirk]',
    'subscribe': '海量撩妹话术、精选惯例、迷你情话和恋爱策略可供搜索，并支持语音搜索，您的智能撩妹恋爱助理/:8-)\n'
                 '使用方法：首先把女神的话复制到下面的对话框（支持语音），'
                 '然后我会用叼炸天的人工智能算法帮你挑选几个候选情话，你只需双击文本然后选择复制满意的回复即可🎉🎁💪\n'
                 '助你撩妹成功/:,@f/:handclap/:love',
    'business': '商务合作请联系\n'
                 '手机/微信号：15622146998\n'
                 '邮箱：421542148@qq.com\n'
                 '感谢您的支持与认可～',
    'feedback': '意见反馈请联系\n'
                '手机/微信号：15622146998\n'
                '邮箱：421542148@qq.com\n'
                '您的支持与反馈是我们前进的不竭动力，非常感谢~',
    'others': '功能正在建设中，敬请期待/:,@f\n'
              '意见或者建议反馈请联系\n'
              '手机/微信号：15622146998\n'
              '邮箱：421542148@qq.com\n'
              '您的支持与反馈是我们前进的不竭动力，非常感谢~'
}


class Handel:
    def __init__(self):
        pass

    def reply_format(self, response):
        if response.text == 'error':
            reply_content = reply_words['use_limit']
        else:
            try:
                reply_temp = []
                for item in response.json():
                    temp = []
                    for key, value in item.items():
                        if key == '内容':
                            temp.append('============\n' + value)
                        elif key == '迷你情话':
                            temp.append(value)
                        else:
                            temp.append(key + ': ' + value)
                    reply_temp.append('\n'.join(temp))
                reply_content = '\n============\n'.join(reply_temp)
            except Exception as e:
                print(e)
                reply_content = reply_words['no_search_result']
                print('no search result')
        return reply_content

    def handel_msg(self, webData, encryp_test=None, nonce=None):
        recMsg = receive.parse_xml(webData)
        # print('recMsg: ', recMsg)
        if isinstance(recMsg, receive.Msg):
            # 发送与接收时的主体和客体是相反的
            toUser = recMsg.FromUserName   # 用户
            fromUser = recMsg.ToUserName   # 公众号
            createTime = recMsg.CreateTime
            msgType = recMsg.MsgType
            reply_content = ''
            payload = {
                'query': '',
                'open_id': toUser,
                'create_time': createTime,
                'msg_type': msgType,
                'mode': 0
            }
            if msgType == 'text':
                # 处理文本消息
                msgId = recMsg.MsgId
                receive_content = recMsg.Content
                payload['query']=receive_content
                response = requests.post('http://182.254.227.188:1889/v1/api/search', data=payload)
                # print('response: ', response)
                # print('response.text: ', response.text)
                reply_content = self.reply_format(response)
            elif msgType == 'image':
                picUrl = recMsg.PicUrl
                msgId = recMsg.MsgId
                mediaId = recMsg.MediaId
                reply_content = reply_words['image_msg']
            elif msgType == 'voice':
                # 处理语音消息
                recognition = recMsg.Recognition
                # print('message_type: ', msgType)
                # print('query_recognition: ', recognition)
                if recognition:
                    # 语音内容搜索
                    payload['query'] = recognition
                    response = requests.post('http://182.254.227.188:1889/v1/api/search', data=payload)
                    reply_content = self.reply_format(response)
                else:
                    reply_content = reply_words['no_voice_recognition']
                # print('reply_content: ', reply_content)
            elif msgType == 'event':
                # 处理关注或则会取消关注事件
                if recMsg.Event == 'subscribe':
                    reply_content = reply_words['subscribe']
                elif recMsg.Event == 'CLICK':
                    eventKey = recMsg.EventKey
                    # 第一个菜单栏【恋爱话术】，点击事件处理
                    if eventKey == "bonjourChat_v1_topic_0":
                        # 【恋爱话术】撩妹话术
                        response = requests.post('http://182.254.227.188:1889/v1/api/QA', data=payload)
                        reply_content = self.reply_format(response)
                    elif eventKey == "bonjourChat_v1_topic_1":
                        # 【恋爱话术】精选惯例
                        response = requests.post('http://182.254.227.188:1889/v1/api/GL', data=payload)
                        reply_content = self.reply_format(response)
                    elif eventKey == "bonjourChat_v1_topic_2":
                        # 【恋爱话术】迷你情话
                        response = requests.post('http://182.254.227.188:1889/v1/api/QH', data=payload)
                        reply_content = self.reply_format(response)
                    elif eventKey == "bonjourChat_v1_topic_3":
                        # 【恋爱话术】恋爱策略
                        response = requests.post('http://182.254.227.188:1889/v1/api/CL', data=payload)
                        reply_content = self.reply_format(response)
                    # 第三个菜单栏【联系我们】，点击事件处理
                    elif eventKey == "bonjourChat_v1_business":
                        # 【联系我们】商务合作
                        reply_content = reply_words['business']
                    elif eventKey == "bonjourChat_v1_feedback":
                        # 【联系我们】意见反馈
                        reply_content = reply_words['feedback']
                    else:
                        reply_content = reply_words['others']
            # print('reply_content', reply_content)
            replyMsg = reply.TextMsg(toUser, fromUser, reply_content)
            # print('replyMsg', replyMsg.send())
            if nonce:
                ret, encrypt_xml = encryp_test.EncryptMsg(replyMsg.send(), nonce)
                return encrypt_xml
            else:
                return replyMsg.send()
        else:
            print("wait a minute")
            return "success"


if __name__ == '__main__':
    data = [{'主题': '约会套路', '标题': '缘分惯例'}]
    reply_temp = []
    for item in data:
        temp = []
        for key, value in item.items():
            temp.append(key + ': ' + value)
        reply_temp.append('\n'.join(temp))
    reply_content = '\n============\n'.join(reply_temp)
    print('reply_content:\n', reply_content)
