import configparser
from pathlib import Path
import mysql.connector

def add_subscriber_to_db(email):
    config = configparser.ConfigParser()
    config.read(Path('./static/req.env'))

    host = config.get("mysql", "host")
    database = config.get("mysql", "database")
    user = config.get("mysql", "user")
    password = config.get("mysql", "password")

    connection = mysql.connector.connect()
    try:
        connection = mysql.connector.connect(host=host,
                                             database=database,
                                             user=user,
                                             password=password)
        mysql_insert_query = f"INSERT INTO subscriber_emails (Email) VALUES (\'{email}\');"
        cursor = connection.cursor()
        cursor.execute(mysql_insert_query)
        connection.commit()
        print(cursor.rowcount, "Record inserted successfully into Laptop table")
        cursor.close()

    except mysql.connector.Error as error:
        print("Failed to insert record into subscriber_emails table {}".format(error))
    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")