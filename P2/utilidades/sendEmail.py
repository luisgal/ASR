import smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

"""
EXAMPLE

sendWarningEmail(subject="Reporte de dispositivo",
                     body="Se incluye el reporte del dispositivo monitoreado",
                     sender_email="lgalindor1998@gmail.com",
                     receiver_email="lgalindor1998@gmail.com",
                     password="Sabritas01$",
                     filereport="./report/ReporteDisp"+disp[4]+".pdf")
"""

def sendWarningEmail(subject, body, filereport, sender_email="lgalindor1998@gmail.com", receiver_email="lgalindor1998@gmail.com", password="Sabritas01$"):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    filename = filereport

    with open(filename, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)

    part.add_header(
        "Content-Disposition",
        f"attachment; filename=reporte.pdf",
    )

    message.attach(part)
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)