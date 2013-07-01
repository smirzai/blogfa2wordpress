#!/usr/bin/python

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders


sender = 'blogfa2wordpress@saeidmirzaei.com'
receivers = ['smirzai@gmail.com']


msg = MIMEMultipart()
msg['Subject'] = "test with attachment" 
msg['From'] = "blogfa2wordpress@saeidmirzaei.com"
msg['To'] = "smirzai@gmail.com"

messageText = "Hi Saeid, would you please consider this as a first draft "

textPart = MIMEText(messageText, 'plain')

part = MIMEBase('application', "octet-stream")
part.set_payload( open("smirzai.zip","rb").read() )
Encoders.encode_base64(part)
part.add_header('Content-Disposition', 'attachment; filename=smirzai.zip')
msg.attach(textPart)
msg.attach(part)

smtpObj = smtplib.SMTP('localhost')


smtpObj.sendmail(sender, receivers, msg.as_string())         


print "Successfully sent email"

