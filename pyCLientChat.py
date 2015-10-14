#!/usr/bin/python

import socket, sys , select

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try :
	s.connect(("localhost" ,9999))
except :
	sys.exit()
print "Connection succesfully"
 
list = [sys.stdin, s]

while True:

	readdable,writeable,error=select.select(list,[],[])
	for i in readdable:
		if i==s:
			data=i.recv(4096)
			if data:
				sys.stdout.write(data)
			else : 
				print "Disconnected"
				sys.exit()
		else : 
			msg=sys.stdin.readline()
			s.send(msg)

	



