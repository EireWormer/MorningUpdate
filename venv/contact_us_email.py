# Send an HTML email with an embedded image and a plain text message for
# email clients that don't want to display the HTML.
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template
from pathlib import Path
import configparser


def send_contact_us_email(email_from, email_subject, email_message):
    config = configparser.ConfigParser()
    config.read(Path('./static/req.env'))

    email_to = config.get("contact_us", "destination")
    login_email = config.get("contact_us", "login")
    login_key = config.get("contact_us", "login_key")

    # Create the root message and fill in the from, to, subject and message fields
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = email_subject
    msgRoot['From'] = email_from
    msgRoot['To'] = email_to
    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)
    html = Template(Path('./static/contact_us_email/email.html').read_text())
    msgText = MIMEText(html.substitute(msg_from=email_from, msg_subject=email_subject, msg_txt=email_message), 'html')
    msgAlternative.attach(msgText)

    # Send the email
    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        # get from env.csv
        smtp.login(login_email, login_key)
        smtp.sendmail(email_from, email_to, msgRoot.as_string())

