import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
 
def send_email(subject, message):
    msg = MIMEMultipart()
    msg['From'] = 'pulkit.dwivedi.logger@outlook.com'
    msg['To'] = 'pulkitdwivedi123@gmail.com'
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP('smtp-mail.outlook.com', 587)
    server.starttls()
    server.login(msg['From'], 'pulkitdwivedilogger123')
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()