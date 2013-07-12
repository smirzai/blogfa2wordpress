# -*- coding: utf-8 -*- 

import smtplib, os

from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders



def sendEmail(you, fileName, website ):
   me = "blogfa2wordpress@saeidmirzaei.com"

   msg = MIMEMultipart()
   msg['From'] = me
   msg['To'] = you
   msg['Date'] = formatdate(localtime=True)
   msg['Subject'] = u"فایل پشتیبان از وبلاگ " + website;

   this_directory = os.path.dirname(__file__)
   
   textFile = file(os.path.join(this_directory, '../../textMessage.txt'))
   text = textFile.read()
   

   f = file(fileName+ ".zip", "rb")
   msg.attach(MIMEText(text))
   part = MIMEBase('application', "octet-stream")
   part.set_payload( f.read() )
   Encoders.encode_base64(part)
   part.add_header('Content-Disposition', 'attachment; filename="%s"' %  website + ".zip") 
   msg.attach(part)


   s = smtplib.SMTP('localhost')

   s.sendmail(me, [you], msg.as_string())
   s.close()
