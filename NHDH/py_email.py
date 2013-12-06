import smtplib
import os
import yaml
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def py_email(SUBJECT, BODY):
    configFile = os.path.abspath('NHDH/config.yml')
    configStr = open(configFile, 'r')
    configObj =  yaml.load(configStr)
    """With this function we send out our html email"""

    for recipient in configObj['recipients']:

        # Create message container - the correct MIME type is multipart/alternative here!
        MESSAGE = MIMEMultipart('alternative')
        MESSAGE['subject'] = SUBJECT
        MESSAGE['To'] = recipient['address']
        MESSAGE['From'] = str(configObj['smtp']['sender_address'])
        MESSAGE.preamble = """
            Your mail reader does not support the report format.
        Please visit us <a href="http://www.mysite.com">online</a>!"""

        # Record the MIME type text/html.
        HTML_BODY = MIMEText(BODY, 'html')

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        MESSAGE.attach(HTML_BODY)

        # The actual sending of the e-mail
        server = smtplib.SMTP(configObj['smtp']['server']+':'+configObj['smtp']['port'])

        # Print debugging output when testing
        if __name__ == "__main__":
            server.set_debuglevel(1)

        server.starttls()
        server.login(configObj['smtp']['user'],configObj['smtp']['password'])
        server.sendmail(str(configObj['smtp']['sender_address']), [recipient['address']], MESSAGE.as_string())
        server.quit()