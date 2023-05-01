from email.message import EmailMessage
import ssl
import smtplib


def send_smtp_msg(url, sts_code):
    email_sender = 'serversmtp53@gmail.com'
    email_pw = "kcvcnnemhzexqgie"
    email_receiver = 'navodrukshan2000@gmail.com'
    subject = "Attention status: " + sts_code
    message = url + "\t" + sts_code + "please check. "

    email = EmailMessage()
    try:
        email['From'] = email_sender
        email['To'] = email_receiver
        email['Subject'] = subject
        email.set_content(message)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_pw)
            smtp.sendmail(email_sender, email_receiver, email.as_string())
    except Exception as e:
        print(f"ERROR : {e}")