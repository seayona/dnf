from urllib.parse import urlencode
from configparser import ConfigParser
import datetime
import requests
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


class Notification(object):
    def __init__(self):
        print("【通知】读取通知配置")
        self.conf = ConfigParser()
        self.conf.read('./conf/notification.ini', encoding='UTF-8')
        self.wechat = {}
        self.mail = {}
        self._init_wechat()
        self._init_ssl_mail()

    def _init_wechat(self):
        self.wechat['push_server_url'] = self.conf.get('Wechat', 'PushServerUrl')
        try:
            self.wechat['token'] = eval(self.conf.get('Wechat', 'Token'))
        except SyntaxError:
            self.wechat['token'] = self.conf.get('Wechat', 'Token')

    def _init_ssl_mail(self):
        self.mail['host'] = self.conf.get('SSLMail', 'Host')
        self.mail['port'] = self.conf.get('SSLMail', 'Port')
        self.mail['user'] = self.conf.get('SSLMail', 'User')
        self.mail['pwd'] = self.conf.get('SSLMail', 'Pwd')
        self.mail['receive'] = self.conf.get('SSLMail', 'Receive')

    def send(self, content):
        self._send_wechat(content)
        self._send_mail(content)

    def _send_wechat(self, content):
        def s(server_url, send_params):
            print("【通知】发送请求" + f'{server_url}?{urlencode(send_params)}')
            response = requests.get(f'{server_url}?{urlencode(send_params)}')
            if response.status_code == 200:
                print("【通知】通知发送成功")

        content += "-------------------" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(self.wechat['token'], list):
            for t in self.wechat['token']:
                s(self.wechat['push_server_url'], {'title': content, 'content': content, 'token': t})
        else:
            s(self.wechat['push_server_url'], {'title': content, 'content': content, 'token': self.token})

    def _send_mail(self, content):
        ret = True
        try:
            msg = MIMEText(content, 'plain', 'utf-8')
            msg['From'] = formataddr(["Private Secretary", self.mail['user']])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            msg['To'] = formataddr(["FK", self.mail['receive']])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
            msg['Subject'] = "Notification"  # 邮件的主题，也可以说是标题

            server = smtplib.SMTP_SSL(self.mail['host'], self.mail['port'])  # 发件人邮箱中的SMTP服务器，端口是25
            server.login(self.mail['user'], self.mail['pwd'])  # 括号中对应的是发件人邮箱账号、邮箱密码
            server.sendmail(self.mail['user'], [self.mail['receive'], ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.quit()  # 关闭连接
        except Exception as e:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
            ret = False
        return ret
