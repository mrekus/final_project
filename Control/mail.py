import smtplib
from Views.error_window import ErrorWindow


FROM = "marius.rekus@gmail.com"
TO = "marius.rekus@gmail.com"


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
        server.login("marius.rekus@gmail.com", "qcxefxmzeatwpdaa")
        server.sendmail(FROM, TO, message)
        server.close()
    except:
        ErrorWindow("Failed to send e-mail!!!")
