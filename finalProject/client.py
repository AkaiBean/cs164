import socket	#for sockets
import sys	#for exit
import select 
from thread import*

try:
	#create an AF_INET, STREAM socket (TCP)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
	print 'Failed to create socket. Error code: ' + str(msg[0]) + ' Error message: ' + msg[1]
	sys.exit()
print 'Socket Created'

#HOST stores ip address, PORT stores port number
HOST = 'localhost'
#HOST = '10.0.0.4'
PORT = 8888
#connect to remote server
s.connect((HOST, PORT))
print 'Socket connected to ' + HOST

while 1:
	socket_list = [sys.stdin, s]
	read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
	
	for rsock in read_sockets:
		#incoming message from remote server
		if rsock == s:
			data = rsock.recv(1024)
			if not data:
				sys.exit()
			else:
				sys.stdout.write(data)
				sys.stdout.flush()

		else:
			msg = raw_input()
			s.sendall(msg)
			
