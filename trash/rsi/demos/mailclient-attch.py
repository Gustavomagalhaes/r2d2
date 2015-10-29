#!/usr/bin/python

import smtplib
import base64

filename = "ufrpe.jpg"
sender = 'junior@ufrpe.br'
receivers = ['ufrpe@grr.la']

# Read a file and encode it into base64 format
fo = open(filename, "rb")
filecontent = fo.read()
fo.close()

body="""Veja a logo desta importante universidade.
[]s, Junior.
"""

marker = "AUNIQUEMARKER"

# Define the main headers.
part1 = """From: Junior <abraao@genesis.com>
To: Bob <bob@hamburguer.edu>
Subject: Logo da ufrpe.
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary=%s
--%s
""" % (marker, marker)

# Define the message action
part2 = """Content-Type: text/plain
Content-Transfer-Encoding:8bit

%s
--%s
""" % (body,marker)

encodedcontent = base64.b64encode(filecontent)  # base64

# Define the attachment section
part3 = """Content-Type: multipart/mixed; name=\"%s\"
Content-Transfer-Encoding:base64
Content-Disposition: attachment; filename=%s

%s
--%s--
""" %(filename, filename, encodedcontent, marker)
message = part1 + part2 + part3

try:
   conn = smtplib.SMTP('grr.la',25)
   conn.sendmail(sender, receivers, message)         
   conn.quit()
   print "Successfully sent email"
except Exception as inst:
   print "Error: unable to send email"
   print inst
