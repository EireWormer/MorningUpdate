import configparser
import mysql.connector
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template
from pathlib import Path


def get_subscriber_addresses(host, database, user, password):
    connection = mysql.connector.connect()
    email_addresses = []
    try:
        connection = mysql.connector.connect(host=host,
                                             database=database,
                                             user=user,
                                             password=password)
        sql_select_query = "SELECT Email FROM subscriber_emails"
        cursor = connection.cursor()
        cursor.execute(sql_select_query)
        emails = cursor.fetchall()
        for row in emails:
            email_addresses.append(row[0])
    except configparser.Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        if connection.is_connected():
            connection.close()
            cursor.close()
        return email_addresses


def send_contact_us_email():
    config = configparser.ConfigParser()
    config.read(Path('./static/req.env'))

    # Retrieving address list from db
    host = config.get("mysql", "host")
    database = config.get("mysql", "database")
    user = config.get("mysql", "user")
    password = config.get("mysql", "password")
    address_list = get_subscriber_addresses(host, database, user, password)

    # Send email to entire address list
    email_to = config.get("contact_us", "destination")
    login_email = config.get("contact_us", "login")
    login_key = config.get("contact_us", "login_key")

    # Create individual email
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = "Morning Update"
    msgRoot['From'] = login_email
    msg = MIMEMultipart('alternative')
    msgRoot.attach(msg)
    html = Template(Path('./static/update_email/email.html').read_text())
    msgText = MIMEText(html.substitute(top_stories="insert top stories here"), 'html')
    msg.attach(msgText)

    # send email to each email in address_list
    for address in address_list:
        msgRoot['To'] = address
        with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            # get from env.csv
            smtp.login(login_email, login_key)
            smtp.sendmail(login_email, address, msgRoot.as_string())