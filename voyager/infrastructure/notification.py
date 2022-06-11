from urllib.parse import urlencode
from configparser import ConfigParser
import datetime
import requests


class Notification(object):
    def __init__(self):
        print("【通知】读取通知配置")
        conf = ConfigParser()
        conf.read('./conf/notification.ini', encoding='UTF-8')

        self.push_server_url = conf.get('Notification', 'PushServerUrl')
        try:
            self.token = eval(conf.get('Notification', 'Token'))
        except SyntaxError:
            self.token = conf.get('Notification', 'Token')

        print("【通知】读取到的通知配置地址", self.push_server_url)

    def send(self, content):
        def s(server_url, send_params):
            print("【通知】发送请求" + f'{server_url}?{urlencode(send_params)}')
            response = requests.get(f'{server_url}?{urlencode(send_params)}')
            if response.status_code == 200:
                print("【通知】通知发送成功")

        content += "-------------------" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(self.token, list):
            for t in self.token:
                s(self.push_server_url, {'title': content, 'content': content, 'token': t})
        else:
            s(self.push_server_url, {'title': content, 'content': content, 'token': self.token})


