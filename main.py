from email.mime.text import MIMEText
from smtplib import *
import imaplib
import email
from email.header import decode_header
import webbrowser
import os
import threading
import time
import sys

class EmailSender:
    def __init__(self, mail_sender, password, mail_recipients, subject, message_body):
        self.mail_sender = mail_sender
        self.password = password
        self.recipients = mail_recipients
        self.subject = subject
        self.message_body = message_body
        self.smtp_ssl_host = 'smtp.gmail.com'
        self.smtp_ssl_port = 587

    def send_mail(self) -> bool:
        # the email lib has a lot of templates
        # for different message formats,
        # on our case we will use MIMEText
        # to send only text
        for mail_receiver in self.recipients:

            message = MIMEText(self.message_body, 'plain')
            message['Subject'] = self.subject
            message['From'] = mail_sender
            message['To'] = mail_receiver
            print("email ready")
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
                # send the actual mail
                server.send_message(message)
                server.quit()
            except SMTPAuthenticationError:
                print("Incorrect username or password.")


class MyThread(threading.Thread):

    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("Starting " + self.name)

        print("Exiting " + self.name)


print("Welcome to your email client.")
print("To enable signing in from a non secure app like ours, you need to enable less secure apps from your google settings.")
print("To avoid the hassle, we set up a test email for you. \nFeel free to use it. Here's the credentials:")
print("Email: marymicky158@gmail.com ")
print("Password: marymicky18M")

print("Choose your service: ")
try:
    chose = int(input("For sending mails type 1. \nFor reading mails from inbox type 2. \n>> "))
except ValueError:
    print("Invalid Input. Aborting.")
    sys.exit()

if chose == 1:
    # todo separate the while true loop in a different file
    while True:
        print("--------------------------------\n")
        mail_sender = input("Sender Email: ")
        # todo hide the password from terminal
        password = input("Password: ")

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

        try:
            # Create an instance
            EmailSender_ = EmailSender(
                mail_sender, password, mail_recipients, subject, message_body)
            # send the mail
            EmailSender_.send_mail()
        except:
            # problem with authentication, ask for username and pw again
            print("Problem with authentication. Retry.")
            continue
        # mail sent, break out of the loop
        print("Mail Sent.")
        break

# reading mails from inbox

elif chose == 2:
    print("Reading E-mail from inbox never been easier!")
    # account credentials
    username = input("E-mail: ")
    password = input("Password: ")
    #username = "marymicky158@gmail.com"
    #password = "marymicky18M"
    # create an IMAP4 class with SSL
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    # authenticate
    imap.login(username, password)
    status, messages = imap.select("INBOX")
    # does the user want all inbox or emails from a specific sender?
    sender = input("View mails from a specific sender or view all inbox?\nType 'all' or the sender's email >> ")
    if 'all' not in sender.lower():
        typ, data = imap.search(None, 'From', sender)
        # number of top emails to fetch
        N = int(input("Enter numbers of recent mail you want to fetch: "))
    else:
        # get all inbox
        typ, data = imap.search(None, 'ALL')
        # set number of top emails to fetch to 100 by default
        N = 100




    ids = data[0]  # data is a list.
    id_list = ids.split()  # ids is a space separated string

    # total number of emails
    messages = int(messages[0])
    if N > len(id_list):
        # emails requested is less than emails in the user's inbox
        N = len(id_list)
        print("Only found "+str(N) + " emails. Fetching..")
    print("--------------------------------")
    for i in range(N):
        # range(messages, messages-N, -1):
        # fetch the email message by ID
        res, msg = imap.fetch(id_list[i], "(RFC822)")
        for response in msg:
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
                if not msg.is_multipart():
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

    # close the connection and logout
    imap.close()
    imap.logout()
    print("Done")
else:
    print("Invalid Number. Aborting.")