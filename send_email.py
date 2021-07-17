import smtplib, ssl

from email.mime.base import MIMEBase 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

subject = "whatever"
body = "whatever the subject is"
sender = ""
receiver = ""
pwd = ""


email = MIMEMultipart()
email["From"] = sender
email["To"] = receiver
email["Subject"] = subject

email.attach(MIMEText(body, "plain"))

 
session = smtplib.SMTP('smtp-mail.outlook.com', 587)
session.starttls()
session.login(sender, pwd)
text = email.as_string()
session.sendmail(sender, receiver, text)
session.quit()
print("sent")

