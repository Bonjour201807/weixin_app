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
    'change_qa_reply': '现在是问答搜索模式，输入女神说的话，就能知道应该如何回复[Smart]\n'
                       '如需切换其他搜索模式，请点击底部菜单栏的【搜索切换】进行切换\n'
                       '也可以使用语音【切换到**模式】进行切换',
    'change_gl_reply': '现在是惯例搜索模式，输入你想了解的内容，就能得到对话套路[Smart]\n'
                       '如需切换其他搜索模式，请点击底部菜单栏的【搜索切换】进行切换\n'
                       '也可以使用语音【切换到**模式】进行切换\n'
                       '5分钟如无任何操作，系统将自动切换到默认的问答模式',
    'change_qh_reply': '现在是情话搜索模式，输入你想了解的内容，就能获得甜度100%的情话[Smart]\n'
                       '如需切换其他搜索模式，请点击底部菜单栏的【搜索切换】进行切换\n'
                       '也可以使用语音【切换到**模式】进行切换\n'
                       '5分钟如无任何操作，系统将自动切换到默认的问答模式',
    'change_cl_reply': '现在是恋爱策略搜索模式，输入你想了解的内容，就能解锁恋爱攻略[Smart]\n'
                       '如需切换其他搜索模式，请点击底部菜单栏的【搜索切换】进行切换\n'
                       '也可以使用语音【切换到**模式】进行切换\n'
                       '5分钟如无任何操作，系统将自动切换到默认的问答模式',
    'subscribe': '能找到这里的桃花运都不错哦[Smirk][Hey][Smart]\n'
                 '看在你这么机智的份上，就让我这个撩妹小助理，来告诉你怎么回复女神/:rose/:rose/:rose\n'
                 '首先把女神的话复制到下面的对话框，'
                 '然后我会用叼炸天的人工智能算法帮你挑选几个候选情话，你只需双击文本然后选择复制满意的回复即可🎉🎁💪\n'
                 '助你撩妹成功/:,@f/:handclap/:love\n'
                 '(这是我们的第一个版本，希望兄弟们多多支持，后面还会不断优化改进，给大家带来更多的惊喜，非常感谢～)',
    'bussiness': '商务合作请联系\n'
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
            reply_content = '您今天的搜索次数已经达到上限50次，欢迎明天再来使用，祝您生活愉快～'
        elif response.json():
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
            # if len(response.text) >= 1024:
            #     reply_temp = reply_temp[:-1]
            reply_content = '\n============\n'.join(reply_temp)
        else:
            reply_content = 'relax, everything will be fine'
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
                reply_content = '小助手暂时还没有学会识别图片消息，我们还是先用文字交流吧😜\n' \
                                '当然语音也可以[Smart]'
            elif msgType == 'voice':
                # 处理语音消息
                recognition = recMsg.Recognition
                # print('message_type: ', msgType)
                # print('query_recognition: ', recognition)
                if recognition:
                    # 判断是否进行模式切换
                    if '切换' in recognition:
                        if '问答' in recognition:
                            payload['mode'] = '0'
                            response = requests.post('http://182.254.227.188:1889/v1/api/switch', data=payload)
                            if response.text == 'ok':
                                reply_content = reply_words['change_qa_reply']
                        elif '惯例' in recognition or '管理' in recognition:
                            payload['mode'] = '1'
                            response = requests.post('http://182.254.227.188:1889/v1/api/switch', data=payload)
                            if response.text == 'ok':
                                reply_content = reply_words['change_gl_reply']
                        elif '情' in recognition:
                            payload['mode'] = '2'
                            response = requests.post('http://182.254.227.188:1889/v1/api/switch', data=payload)
                            print(response.text)
                            if response.text == 'ok':
                                reply_content = reply_words['change_qh_reply']
                        elif '爱' in recognition or '略' in recognition:
                            payload['mode'] = '3'
                            response = requests.post('http://182.254.227.188:1889/v1/api/switch', data=payload)
                            if response.text == 'ok':
                                reply_content = reply_words['change_cl_reply']
                        elif '模式' in recognition or '默认' in recognition:
                            payload['mode'] = '0'
                            response = requests.post('http://182.254.227.188:1889/v1/api/switch', data=payload)
                            if response.text == 'ok':
                                reply_content = reply_words['change_qa_reply']
                        else:
                            reply_content = '抱歉，小助手没听出来你在说什么，麻烦再说一遍[Facepalm]'
                    else:
                        # 语音内容搜索
                        payload['query'] = recognition
                        response = requests.post('http://182.254.227.188:1889/v1/api/search', data=payload)
                        reply_content = self.reply_format(response)
                else:
                    reply_content = '抱歉，小助手没听出来你在说什么，麻烦再说一遍[Facepalm]'
                # print('reply_content: ', reply_content)
            elif msgType == 'event':
                # 处理关注或则会取消关注事件
                if recMsg.Event == 'subscribe':
                    reply_content = reply_words['subscribe']
                elif recMsg.Event == 'CLICK':
                    eventKey = recMsg.EventKey
                    # 第一个菜单栏【搜索切换】，点击事件处理
                    if eventKey == "bonjourChat_v1_search_0":
                        # 【搜索切换】问答模式
                        payload['mode'] = '0'
                        response = requests.post('http://182.254.227.188:1889/v1/api/switch', data=payload)
                        if response.text == 'ok':
                            reply_content = reply_words['change_qa_reply']
                    elif eventKey == "bonjourChat_v1_search_1":
                        # 【搜索切换】惯例模式
                        payload['mode'] = '1'
                        response = requests.post('http://182.254.227.188:1889/v1/api/switch', data=payload)
                        if response.text == 'ok':
                            reply_content = reply_words['change_gl_reply']
                    elif eventKey == "bonjourChat_v1_search_2":
                        # 【搜索切换】情话模式
                        payload['mode'] = '2'
                        response = requests.post('http://182.254.227.188:1889/v1/api/switch', data=payload)
                        print(response.text)
                        if response.text == 'ok':
                            reply_content = reply_words['change_qh_reply']
                    elif eventKey == "bonjourChat_v1_search_3":
                        # 【搜索切换】恋爱策略
                        payload['mode'] = '3'
                        response = requests.post('http://182.254.227.188:1889/v1/api/switch', data=payload)
                        if response.text == 'ok':
                            reply_content = reply_words['change_cl_reply']
                    # 第二个菜单栏【恋爱话术】，点击事件处理
                    elif eventKey == "bonjourChat_v1_topic_0":
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
                    elif eventKey == "bonjourChat_v1_topic_4":
                        # 【恋爱话术】恋爱课程
                        reply_content = reply_words['others']
                    elif eventKey == "bonjourChat_v1_bussiness":
                        reply_content = reply_words['bussiness']
                    elif eventKey == "bonjourChat_v1_feedback":
                        reply_content = reply_words['feedback']
                    else:
                        reply_content = reply_words['others']
            # print('reply_content', reply_content)
            replyMsg = reply.TextMsg(toUser, fromUser, reply_content)
            print('replyMsg', replyMsg.send())
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
