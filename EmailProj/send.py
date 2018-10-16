import smtplib 
import os
import mimetypes 
from email import encoders
from email.mime.text import MIMEText 
from email.mime.multipart import MIMEMultipart

def send_email(addr_to, msg_subj, msg_text, files):
    """Sends an email with text attachments"""
    addr_from = 'testhunta@yandex.ru'
    passfile = open('F:/Email/password.txt')
    password = passfile.read()


    msg = MIMEMultipart()
    msg['From'] = addr_from
    msg['To'] = addr_to
    msg['Subject'] = msg_subj

    body = msg_text
    msg.attach(MIMEText(body, 'plain'))
    for f in files:
        attach_file(msg, f)

    server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
    server.login(addr_from, password)
    server.send_message(msg)
    server.quit()
    passfile.close()


def attach_file(msg, filepath):
    """Makes an attachment file
    """
    filename = os.path.basename(filepath)
    ctype, encoding = mimetypes.guess_type(filepath)
    if ctype is None or encoding is not None:
        ctype = 'application/octet-stream' 
    maintype, subtype = ctype.split('/', 1)
    if maintype == 'text':
        tfile = open(filepath)
        file = MIMEText(tfile.read(), _subtype=subtype)
        tfile.close()
    file.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(file)

addr_to = 'testhunta@yandex.ru'
files = ['F:/Email/text1.txt', 'F:/Email/text2.txt']

send_email(addr_to, 'test message', 'Михаил Афанасьевич Булгаков. Мастер и Маргарита. Отрывок.', files)

