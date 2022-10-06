import smtplib
from Views.error_window import ErrorWindow
from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")

FROM = config["EMAIL"]["gmail_login"]
TO = config["EMAIL"]["to"]


def send_email(subject, text):
    """
    Išsiunčia e-mail iš FROM į TO paštą
    :param subject: laiško tema
    :param text: laiško tekstas
    """
    message = "\r\n".join(
        [f"From: {FROM}", f"To: {TO}", f"Subject: {subject}", "", f"{text}"]
    )
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(config["EMAIL"]["gmail_login"], config["EMAIL"]["gmail_app_key"])
        server.sendmail(FROM, TO, message)
        server.close()
        ErrorWindow("Sent successfully!")
    except:
        ErrorWindow("Failed to send e-mail!!!")
