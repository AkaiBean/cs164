import socket	#for sockets
import sys	#for exit
from thread import*
from menu import*
from game import*
from player import*

#create an AF_INET, STREAM socket (TCP)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket Created'

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

HOST = ''	#symbolic name meaning all available interfaces
PORT = 8888	#arbitary port number
#bind server to host and port
try:
	s.bind((HOST, PORT))
except socket.error, msg:
	print 'Bind failed. Error code: ' + str(msg[0]) + ' Error message: ' + msg[1]
	sys.exit()
print 'Socket bind complete'


#start listening on socket
s.listen(10)
print 'Socket now listening'


#function for handling client threads
def clientthread(conn, gameList, connList):
	#used like enum
	#1 for welcome_menu
	#2 for start_menu
	#3 for start_game
	welcomeMenu = 1
	startMenu = 2
	startGame = 3
	exitGame = 4
	menu = welcomeMenu
	errMsg = ''
	numError = 0
	player0 = None
	userList = []
	global s
	server_socket = s

	while 1:
		if menu == welcomeMenu:
			menu, errMsg, player0 = welcome_menu(conn, userfile, errMsg)

		if menu == startMenu:
			menu, errMsg, numError = start_menu(conn, userfile, errMsg) 
			
		if menu == startGame:
			userList.append(player0)
			gameList.append(userList)	
			menu, errMsg = start_game(conn, wordfile, numError, userList, server_socket)
			gameList.remove(userList)

		if menu == exitGame:	#self explanatory
			break
		
		

		

	#for some reason came out of loop
	connList.remove(conn)
	conn.shutdown(socket.SHUT_RDWR)	#socket cannot send or receive
	conn.close() #closes socket and all future operations on the socket will fail

userfile = 'users.txt'
wordfile = 'wordlist.txt'
hsfile = 'highscores.txt'
gameList = []
connList = []
connList.append(s)

#now keep talking with clients
while 1:
	conn, addr = s.accept()
	connList.append(conn)
	print 'Connected with ' + addr[0] + ':' + str(addr[1])
	#start new thread for client 
	start_new_thread(clientthread ,(conn, gameList, connList))
#for some reason came out of loop
s.close()
