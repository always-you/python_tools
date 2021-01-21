import smtplib
from email.mime.text import MIMEText
from email.header import Header


def send_email(title, content, from_addr, to_addr, password, content_type='plain', encoding='utf-8'):
    """
    发送邮件
    :param title: 邮件标题
    :param content: 邮件内容
    :param from_addr: 发送邮件的邮箱地址
    :param to_addr: 接收邮件的邮箱列表
    :param password: 发送邮件的邮箱密码
    :param content_type: 邮件内容类型  plain/html/..
    :param encoding: 编码
    """
    smtp_server = 'smtp.exmail.qq.com'

    # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
    msg = MIMEText(content, content_type, encoding)

    # 邮件头信息
    msg['From'] = Header(from_addr)
    msg['To'] = ','.join(to_addr)
    msg['Subject'] = Header(title)

    # 开启发信服务，这里使用的是加密传输
    server = smtplib.SMTP_SSL(host=smtp_server)
    server.connect(smtp_server, 465)
    # 登录发信邮箱
    server.login(from_addr, password)
    # 发送邮件
    server.sendmail(from_addr, msg['To'].split(','), msg.as_string())
    # 关闭服务器
    server.quit()

    # send_email(title='测试', data='测试1', to_addr=['huangwenbin@myzaker.com'], from_addr='monitor@myzaker.com', password='Jsyb371')