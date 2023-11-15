import random, string
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.header import Header


# 发送邮件
def send_email(receiver, ecode):
    content = (
        f"<br/>欢迎注册awu网站，您的邮箱验证码为："
        f"<span style='color: red; font-size: 40px;'>{ecode}</span>"
        f"请复制到注册窗口中继续完成注册。<br>"
    )

    sender = "awu2024@126.com"

    message = MIMEText(content, "html", "utf-8")
    message["Subject"] = Header("awu的网站注册验证码", "utf-8")
    message["From"] = sender
    message["To"] = receiver

    smtpObj = SMTP_SSL("smtp.126.com")
    smtpObj.login(user="awu2024@126.com", password="LQMAYOVCLTXTASSW")

    smtpObj.sendmail(sender, receiver, str(message))
    smtpObj.quit()


# 生成6位随机字符串作为邮箱验证码
def gen_email_code():
    str = random.sample(string.ascii_letters + string.digits, 6)
    return "".join(str)
