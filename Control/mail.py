import smtplib
from Views.ErrorWindow import ErrorWindow
FROM = "marius.rekus@gmail.com"
TO = "marius.rekus@gmail.com"


def send_email(subject, text):
    message = "\r\n".join(
        [f"From: {FROM}",
         f"To: {TO}",
         f"Subject: {subject}",
         "",
         f"{text}"]
    )
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login("marius.rekus@gmail.com", "qcxefxmzeatwpdaa")
        server.sendmail(FROM, TO, message)
        server.close()
    except:
        ErrorWindow("Failed to send order e-mail")
