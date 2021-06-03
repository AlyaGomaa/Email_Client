from smtplib import *
from email.mime.text import MIMEText


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
        message = MIMEText(self.message_body, 'plain')
        message['Subject'] = self.subject
        message['From'] = mail_sender
        message['To'] = self.recipients

        # connect to Google's servers using SSL
        server = SMTP(self.smtp_ssl_host, self.smtp_ssl_port)

        server.connect(self.smtp_ssl_host, self.smtp_ssl_port)
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


# todo separate the while true loop in a different file

while True:
    print("Welcome to your email client.")
    print("To enable signing in from a non secure app like our, you need to enable less secure apps from your google settings.")
    print("To avoid the hassle, we set up a test email for you. \nFeel free to use it. here's the credentials:")
    print("Email: marymicky158@gmail.com ")
    print("Password: marymicky18M")
    mail_sender = input("Sender Email: ")

    # todo hide the password from terminal
    password = input("Password: ")

    # todo support multiple recipients
    mail_recipients = input("Receiver Email: ")

    print("---------------------------------")

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
        continue
    # mail sent, break out of the loop
    print("Mail Sent.")
    break

