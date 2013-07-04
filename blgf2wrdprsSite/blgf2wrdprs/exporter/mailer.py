import smtplib
from email.mime.text import MIMEText


def sendEmail(you, me, textFile, attached):
   print "I am in mailer"
   msg = MIMEText("This is a test")
   me = 'smirzai@gmail.com'
   you = 'smirzai@gmail.com'

   msg['Subject'] = 'sample subject'
   msg['From'] = me
   msg['To'] = you

   s = smtplib.SMTP('localhost')
   print msg.as_string()
   s.sendmail(me, [you], msg.as_string())
   s.quit()
