"""
@Author  : monabai
@Time    : 2018/8/13 16:29
@Software: PyCharm
@File    : handel.py.py
"""
import requests
import receive
import reply


class Handel:
    def __init__(self):
        pass

    @classmethod
    def handel_msg(cls, webData):
        recMsg = receive.parse_xml(webData)
        print('recMsg: ', recMsg)
        if isinstance(recMsg, receive.Msg):
            toUser = recMsg.FromUserName
            fromUser = recMsg.ToUserName
            createTime = recMsg.CreateTime
            msgType = recMsg.MsgType
            reply_content = ''
            if recMsg.MsgType == 'text':
                # 处理文本消息
                msgId = recMsg.MsgId
                receive_content = recMsg.Content
                payload = {
                    'query': receive_content,
                    'open_id': fromUser,
                    'create_time': createTime,
                    'msg_type': msgType,
                    'msg_id': msgId
                }
                response = requests.post('http://182.254.227.188:1889/v1/api/search', data=payload)
                if response.json():
                    if len(response.json()) == 1:
                        for key, value in response.json():
                            reply_content = key + ': ' + value
                    else:
                        reply_temp = []
                        for item in response.json():
                            temp = []
                            for key, value in item.items():
                                temp.append(key + ': ' + value)
                            reply_temp.append('\n'.join(temp))
                        reply_content = '\n============\n'.join(reply_temp)
                    print('reply_content', reply_content)
                else:
                    reply_content = 'relax, everything will be fine'
                    print('no search result')
            elif recMsg.MsgType == 'event':
                print('recMsg.Event: ', recMsg.Event)
                # 处理关注或则会取消关注事件
                if recMsg.Event == 'subscribe':
                    reply_content = '能找到这里的桃花运都不错哦[Smirk][Hey][Smart]\n' \
                                    '看在你这么机智的份上，让我这个撩妹小助手，来告诉你怎么回复你的女神/:rose/:rose/:rose\n' \
                                    '把女神的话复制到下面的对话框，' \
                                    '然后我会用叼炸天的人工智能算法帮你挑选几个候选情话，你只需双击文本然后选择复制满意的回复即可🎉🎁💪\n' \
                                    '助你撩妹成功/:,@f/:handclap/:love'
            replyMsg = reply.TextMsg(toUser, fromUser, reply_content)
            print('replyMsg', replyMsg)
            return replyMsg.send()
        else:
            print("wait a minute")
            return "success"


if __name__ == '__main__':
    pass
