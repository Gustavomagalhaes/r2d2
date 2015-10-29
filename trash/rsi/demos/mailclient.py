#!/usr/bin/python

import smtplib

sender = 'alice@crepes.fr'
receivers = ['ufrpe@grr.la']

message = """From: Alice <alice@crepes.fr>
To: Bob <ufrpe@grr.la>
Subject: Important question.

Do you like ketchup?
[]s, Alice.
"""

try:
   conn = smtplib.SMTP('grr.la',25)
   conn.sendmail(sender, receivers, message)         
   conn.quit()
   print "Successfully sent email"
except Exception as inst:
   print "Error: unable to send email"
   print inst
