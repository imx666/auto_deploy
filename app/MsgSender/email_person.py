import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

# 设置SMTP服务器信息
smtp_server = 'smtp.163.com'
smtp_port = 25

# 发件人邮箱信息
EMAIL_SENDER_ADDRESS = os.getenv('EMAIL_PERSON_SENDER_ADDRESS')
EMAIL_AUTHORIZATION_CODE = os.getenv("EMAIL_PERSON_AUTHORIZATION_CODE")


def send_email(subject, text_body, recipient_email):
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(EMAIL_SENDER_ADDRESS, EMAIL_AUTHORIZATION_CODE)

        try:
            # 创建邮件内容
            msg = MIMEMultipart()
            head = Header("鼠鼠的小爬虫", 'utf-8')
            head.append('iuxwilson@163.com', 'ascii')
            msg['From'] = head
            # msg["Subject"] = "学校通知"
            # msg['Subject'] = "学校通知 - 关键词：'公示'"
            msg['Subject'] = subject
            msg["To"] = recipient_email
            msg.attach(MIMEText(text_body, "html"))

            server.sendmail(EMAIL_SENDER_ADDRESS, recipient_email, msg.as_string())
            print(f"success to {recipient_email}")
        except Exception as e:
            print(f"{recipient_email} - Error: {str(e)}")

        print("All emails sent successfully!")





if __name__ == "__main__":
    recipient_email = ["18924622559@163.com"]

    html_content = """
<html lang="en">
<meta charset="UTF-8">

 <body>
    <br>
    <br>
    <br>
    <br>

    <div class="contact-info">
        <div class="code">
            <h1 style="color: red;">验证码：{verification_code}</h1>
        </div>

        <h4>本验证码仅用于绑定微信小程序</h4>
        <h4>请勿将此验证码透露给他人，5分钟内有效。</h4>
        <h4>如果您未进行此操作，请忽略此邮件。</h4>
    </div>

    <br>
    <br>

</body>


</html>
<style>
    .contact-info h5 {
        margin: 2px 0;
    }

    .contact-info h2 {
        margin: 2px 0;
    }

    .contact-info h4 {
        margin: 2px 0;
    }
</style>
    """

    send_email("注册验证码", html_content, recipient_email)