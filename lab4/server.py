import socket
import sys
from thread import *
 
HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
 
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
 
#Start listening on socket
s.listen(10)
print 'Socket now listening'
 
#Function for handling connections. This will be used to create threads
def clientthread(conn, connList):
    #Sending message to connected client
    conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string
     
    #infinite loop so that function do not terminate and thread do not end.
    while True:
                
        #Receiving from client
        data = conn.recv(1024)
        print(data)
	
	#Break out of loop
        print(data[0:2])
    	if data[0:2] == '!q':
	    	break
	
	#Reply to all clients
	elif data[0:8] == '!sendall':
	    reply = data[9:len(data)]
	    for conn in connList:
		conn.sendall(reply)		
	else:
            reply = 'OK...' + data
            if not data: 
                break
            conn.sendall(reply)
     
    #came out of loop
    connList.remove(conn)
    conn.close()

connList = []
 
#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
     
    connList.append(conn)    

    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn, connList,))
 
s.close()
