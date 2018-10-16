import sys
import imaplib
import email
import os
 
server = 'imap.yandex.ru'
port = "143"
login = 'testhunter@yandex.ru'
passfile = open('F:/Email/password.txt')
password = passfile.read()
putdir="/home/pavel/";

mail = imaplib.IMAP4_SSL(server)
mail.login(login, password)
mail.list()
mail.select("inbox")
#получаем UID последнего письма
result, data = mail.uid('search', None, "ALL")       
try:
    latest_email_uid = data[0].split()[-1]     
except IndexError:
    print("писем нет!");
result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
raw_email = data[0][1]
try:
    email_message = email.message_from_string(raw_email)   
except TypeError:
    email_message = email.message_from_bytes(raw_email)
print ("--- нашли письмо от: ", email.header.make_header(email.header.decode_header(email_message['From'])));
for part in email_message.walk():
    print(part.get_content_type())
    if "application" in part.get_content_type() :       
        filename = part.get_filename()
        filename=str(email.header.make_header(email.header.decode_header(filename)))
        if not(filename): 
            filename = "test.txt"         
        print("---- нашли вложение ", filename);        
        fp = open(os.path.join('F:/Email/', filename), 'wb')
        fp.write(part.get_payload(decode=1))
        fp.close

passfile.close()

