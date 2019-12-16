import smtplib
from email.mime.text import MIMEText


def send_mail(msg):
    SMTP_SERVER = "smtp.mail.yahoo.co.jp"
    SMTP_PORT = 587
    SMTP_USERNAME = "oruka2365@yahoo.co.jp"  # 送信元アドレス
    SMTP_PASSWORD = "Bessho199665@"  # パスワード
    EMAIL_FROM = "oruka2365@yahoo.co.jp"  # 送信元アドレス
    EMAIL_TO = "oruka199665@yahoo.co.jp"  # 送信先アドレス
    EMAIL_SUBJECT = "ビットフライヤーの自動取引プログラムの運用報告について"
    co_msg = msg
    msg = MIMEText(co_msg)
    msg['Subject'] = EMAIL_SUBJECT
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    mail = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    mail.login(SMTP_USERNAME, SMTP_PASSWORD)
    mail.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
    mail.quit()
