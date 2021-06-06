from email.mime.text import MIMEText
from smtplib import *
import imaplib
import email
from email.header import decode_header
import webbrowser
import os
import threading
import time


class EmailSender(threading.Thread):
    def __init__(self, threadID, mail_sender, password, mail_recipients, subject, message_body):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.mail_sender = mail_sender
        self.password = password
        self.recipients = mail_recipients
        self.subject = subject
        self.message_body = message_body
        self.smtp_ssl_host = 'smtp.gmail.com'
        self.smtp_ssl_port = 587

    def send_mail(self) -> bool:
        # connect to Google's servers using SSL
        server = SMTP(self.smtp_ssl_host, self.smtp_ssl_port)

        server.connect(self.smtp_ssl_host, self.smtp_ssl_port)
        print("connected to the server")
        server.ehlo()
        server.starttls()
        server.ehlo()

        try:
            # to interact with the server, first we log in
            # and then we send the message
            server.login(self.mail_sender, self.password)

        except SMTPAuthenticationError:
            print("Incorrect username or password.")

    def run(self):
        # the email lib has a lot of templates
        # for different message formats,
        # on our case we will use MIMEText
        # to send only text
        message = MIMEText(self.message_body, 'plain')
        message['Subject'] = self.subject
        message['From'] = mail_sender
        message['To'] = self.recipients
        print("email ready")
        try:
            # send the actual mail
            server.send_message(message)
            print("Mail sent to "+self.recipients)
        except:
            print("Problem sending Mail to "+self.recipients)

        server.quit()


class EmailReader(threading.Thread):

    def __init__(self, res, msg ):
        threading.Thread.__init__(self)
        self.res = res
        self.msg = msg


    def run(self):
        # fetch the email message by ID

        for response in self.msg:
            if isinstance(response, tuple):
                # parse a bytes email into a message object
                msg = email.message_from_bytes(response[1])
                # decode the email subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    # if it's a bytes, decode to str
                    subject = subject.decode(encoding)
                # decode email sender
                From, encoding = decode_header(msg.get("From"))[0]
                if isinstance(From, bytes):
                    From = From.decode(encoding)
                print("Subject:", subject)
                print("From:", From)
                # if the email message is multipart
                if msg.is_multipart():
                    # iterate over email parts
                    for part in msg.walk():
                        # extract content type of email
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        # get the email body
                        body = part.get_payload(decode=True).decode()

                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            # print text/plain emails and skip attachments
                            print(body)
                            print("-------------*************--------------")
                else:
                    # extract content type of email
                    content_type = msg.get_content_type()
                    # get the email body
                    body = msg.get_payload(decode=True).decode()
                    if content_type == "text/plain":
                        # print only text email parts
                        print(body)
                        print("-------------*************--------------")


print("Welcome to your email client.")
print("To enable signing in from a non secure app like our, you need to enable less secure apps from your google settings.")
print("To avoid the hassle, we set up a test email for you. \nFeel free to use it. here's the credentials:")
print("Email: marymicky158@gmail.com ")
print("Password: marymicky18M")
print("--------------------------------")
print("Choose your service: ")
chose = int(input("For sending mails type 1 \nFor reading mails from inbox type 2 \n "))

threads = []

if chose == 1:
    # todo separate the while true loop in a different file
    while True:

        mail_sender = input("Sender Email: ")

        # todo hide the password from terminal
        password = input("Password: ")

        # multiple recipients
        mail_recipients = []
        receiver = input("Receivers Emails list Type ok when done: ")
        while receiver != "ok":
            mail_recipients.append(receiver)
            receiver = input("Receivers Emails: ")
        print(mail_recipients)
        print("---------------------------------")
        # randa.yasser1999@gmail.com

        subject = input("Subject: ")
        # todo support multiline msg body
        message_body = input("Msg to send: ")

        # sending mails in threads
        for i in range(len(mail_recipients)):
            # Create an instance
            EmailSender_ = EmailSender(i, mail_sender, password, mail_recipients[i], subject, message_body)

            # send the mail
            EmailSender_.send_mail()
            EmailSender_.start()
            # adding threads to the thread queue
            threads.append(EmailSender_)
        # mails sent, break out of the loop
        for t in threads:
            t.join

        print("All threads done!")
        threads = []
        break

# reading mails from inbox

else:
    print("Reading E-mail from inbox never been easier! ")
    # account credentials
    username = input("E-mail: ")
    password = input("Password: ")

    # create an IMAP4 class with SSL
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    # authenticate
    imap.login(username, password)
    status, messages = imap.select("INBOX")
    # number of top emails to fetch
    sender = input("View mails from: ")
    N = int(input("Enter numbers of recent mail you want to fetch: "))

    typ, data = imap.search(None, 'From', sender)

    ids = data[0]  # data is a list.
    id_list = ids.split()  # ids is a space separated string

    # total number of emails
    messages = int(messages[0])
    if N > len(id_list):
        N = len(id_list)
        print("Only found "+str(N))
    print("\n--------------------------------")
    for i in range(N):
        res, msg = imap.fetch(id_list[i], "(RFC822)")
        EmailReader_ = EmailReader(res, msg)
        EmailReader_.start()
        # adding threads to the thread queue
        threads.append(EmailReader_)

    for t in threads:
        t.join()
    print("All threads done!")
    threads = []

    # close the connection and logout
    imap.close()
    imap.logout()
    print("Done")
