#!/usr/bin/python

import socket, select

def broadcast(socket,message):
	global list
	global s
	host, port = socket.getpeername()
	msg = "[%s:%s]: %s" % (str(host), str(port), str(message))
	for sock in list:
		if sock != socket and sock != s:
			sock.send(msg)
			

def acceptConn():
	try:	
		global s
		global list
		global dbUsers
		sNew,pNew= s.accept()
		s.settimeout(.1)
		existsuserName= 0
		while existsuserName == 0:
			sNew.send("Introduce tu nuevo nombre de usuario")
			userName =sNew.recv(2048)
			if userName not in dbUsers:
				existsuserName=1
				list[sNew]=userName
				dbUsers.append(userName)
		
				
	except:
		pass

def getMsg(socket):
	global list
	try:
		ret=socket.recv(4096)
		socket.settimeout(.1)
		if str(ret) == "/quit" or str(ret) == "/Quit":
			host,port=socket.getpeername()
			print ("["+str(host)+" :"+str(port)+"] ha salido.")
			list.remove(socket)
			socket.close()
			return None 
		return ret
	except:
		host,port=socket.getpeername()
		
		print ("["+str(host)+" :"+str(port)+"] ha salido.")		

		list.remove(socket)
		return None 

global s
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("",8888))
print( "Server working on port 9999")
s.listen(10)
global list
list=[s]
while True:
	acceptConn()
	readdable,writeable,error=select.select(list,[],[])
	for i in readdable: 
		if i != s:
			data=getMsg(i)
			if data:
				broadcast(i,data)
				
		
s.close()
