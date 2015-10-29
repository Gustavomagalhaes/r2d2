import socket
import sys

# le o hostname que sera consultado
host = str(raw_input("digite um hostname: "))
try:
	
  iphost = socket.gethostbyname(host)
  print "IP: " + str(iphost)
except socket.error:
  print "erro ao resolver host"