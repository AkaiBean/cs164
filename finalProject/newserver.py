import socket, select, sys, thread
from newmenu import*
from _game import*

inputs = []
userList = []	#so each client can keep track at which part of the menu they are in
tempList = []	#temporary storage for immutable objects
delList = []	#users to be deleted
hostList = []
gameList = []
HOST = ''
PORT = 8888

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print 'Socket created'
try:
	s.bind((HOST, PORT))
except socket.error, msg:
	print 'Bind failed. Error code: ' + str(msg[0]) + ' Error message: ' + msg[1]
	sys.exit()
print 'Socket bind complete'
s.listen(10)
print 'Socket now listening'

userfile = 'users.txt'
wordfile = 'wordlist.txt'
hsfile = 'highscores.txt'
hoff = 'hof.txt'
inputs.append(s)

def serverMenu():
	printMenu = createServerMenu()
	print printMenu
	while 1:
		choice = raw_input('<You> ')
		if choice == '1':
			if not userList:
				print 'No users are currently logged on.'
			else:
				print '\nList of Users'
				print '-------------'
				for users in userList:
					print users[1]
		elif choice == '2':
			f = open(wordfile, 'r')
			table = f.readlines()
			f.close()
			print '\nList of Words'
			print '-------------'
			for row in table:
				print row
		elif choice == '3':
			word = raw_input('Add word: ') + '\n'
			f = open(wordfile, 'a')
			f.write(word)
			f.close()

		print printMenu 
		

thread.start_new_thread(serverMenu, ())

while 1:

	#select function probably checks for listening sockets with server socket
	read_sockets, write_sockets, error_sockets = select.select(inputs, [], [])
	for rsock in read_sockets:
		
		if rsock == s:
			#handle new connection
			conn, addr = s.accept()
			inputs.append(conn)
			print 'Connected with ' + addr[0] + ':' + str(addr[1])
			
			#create welcome menu and send to client
			line_dash = '---------------------\n'
			conn.sendall(line_dash)
			welcome_message = 'Welcome to Hangman\'s!\n'
			conn.sendall(welcome_message)
			printMenu = createWelMenu()
			conn.sendall(printMenu)			
			
		else:
			#-------------
			welMenu = 1
			startMenu = 2
			diffMenu = 3
			game = 4
			listGameMenu = 5
			gameJoin = 6
			#-------------
			endGame = 1
			contGame = 3
			menu = welMenu	
			sock = ''
			usr = ''			

			#check if user is logged in
			for obj in userList:
				sock = obj[0]
				if rsock == sock:
					sock, usr, menu = obj
				
			
			if menu == welMenu:
				choice = rsock.recv(1024)
				if choice == '1':
					#login
					rsock.sendall('\nUsername: ')
					username = rsock.recv(1024)
					rsock.sendall('Password: ')
					password = rsock.recv(1024)
					account = username + '\t' + password + '\n'

					#open file and find account
					f = open(userfile, 'r')
					table = f.readlines()
					for row in table:
						if row == account:
							f.close()
							userList.append((rsock, username, startMenu))
							rsock.sendall('Login Successful!\n')
							printMenu = createStartMenu()
							rsock.sendall(printMenu)
					if not f.closed:
						#warning doesn't check if file is opened by other processes!
						f.close()
						rsock.send('Invalid username or password!\n')
							
						#print welcome menu
						printMenu = createWelMenu()
						rsock.sendall(printMenu)
				
				elif choice == '2':
					#create new user
					rsock.sendall('\nWhat is your username? ')
					username = rsock.recv(1024)
					f = open(userfile, 'r')
					table = f.readlines()
					for row in table:
						row = row.split()[0]
						if row == username:
							rsock.sendall('Error: Username \'' + username + '\' is already taken!\n')
							rsock.sendall('Returning to Welcome Menu...\n')
							f.close()
					
					if not f.closed:
						#if file is not closed
						f.close()
						rsock.sendall('What is your password? ')
						password = rsock.recv(1024)
						f = open(userfile, 'a')
						f.write(username + '\t' + password + '\n')
						f.close()
						rsock.sendall('Account ceate successful!\n')
					printMenu = createWelMenu()
					rsock.sendall(printMenu)

				elif choice == '3':
					#show hall of fame
					printMenu = createHallofFame(hsfile)
					rsock.sendall(printMenu)
					printMenu = createWelMenu()
					rsock.sendall(printMenu)					

				elif choice == '4':
					#cut connection with client
					inputs.remove(rsock)
					rsock.shutdown(socket.SHUT_RDWR)
					rsock.close()
				else:
					rsock.sendall('Invalid choice. Please choose again.\n')
					printMenu = createWelMenu()
					rsock.sendall(printMenu)

			elif menu == startMenu:

				#remove empty games from game list
				for games in gameList:
					#if game list is empty
					if not games.playerList: 						
						gameList.remove(games)						

				#start menu
				choice = rsock.recv(1024)
				if choice == '1':
					#show difficulty menu
					userList.remove((rsock, usr, menu))
					userList.append((rsock, usr, diffMenu))
					printMenu = createDiffMenu()
					rsock.sendall(printMenu)					
				
				elif choice == '2':
					#show list of games
					
					#no host no game case
					if not hostList:
						for games in gameList:
							gameList.remove(games)					

					for host in hostList:
						for games in gameList:
							if host[1] != games.gameid:
								gameList.remove(games)
					userList.remove((rsock, usr, menu))
					userList.append((rsock, usr, listGameMenu))
					printMenu = createListGameMenu(gameList)
					rsock.sendall(printMenu)
				
				elif choice == '3':
					#show hall of fame
					printMenu = createHallofFame(hsfile)
					rsock.sendall(printMenu)
					printMenu = createStartMenu()
					rsock.sendall(printMenu)					

				elif choice == '4':
					#cut connection with client				
					inputs.remove(rsock)
					userList.remove((rsock, usr, menu))
					rsock.shutdown(socket.SHUT_RDWR)
					rsock.close()
				else:
					rsock.sendall('Invalid choice. Please choose again.\n')
					printMenu = createStartMenu()
					rsock.sendall(printMenu)
	
			elif menu == diffMenu:
				#difficulty menu
				difficulty = 0
				choice = rsock.recv(1024)
				if choice >= '1' and choice <= '3':
					if choice == '1':
						difficulty = 3
					if choice == '2':
						difficulty = 2
					if choice == '3':
						difficulty = 1
					
					newGame = gameObj((rsock, usr, menu), wordfile, difficulty, hsfile, hoff)
					gameList.append(newGame)
					hostList.append((rsock, newGame.gameid))
					newGame.printGame()					
					
					#change menu	
					userList.remove((rsock, usr, menu))
					userList.append((rsock, usr, game))
				else:
					rsock.sendall('Invalid choice. Please choose again.\n')
					printMenu = createDiffMenu()
					rsock.sendall(printMenu)

			elif menu == game:
				#run game
				currentGame = None
				userInput = rsock.recv(1024)
				
				#get game id from host				
				for host in hostList:
					if rsock == host[0]:
						gameid = host[1]
				for currGame in gameList:
					if currGame.gameid == gameid:
						currentGame = currGame
				#try:
				status = currentGame.runGame(rsock, userInput)
				#except:
					#pass
				
				if status == startMenu: 
					#go to start menu
					userList.remove((rsock, usr, menu))
					userList.append((rsock, usr, startMenu))
					printMenu = createStartMenu()
					rsock.sendall(printMenu)

				elif status == endGame:
					currentGame.printGame()
					for user in userList:
						for player in currentGame.playerList:
							if user[1] == player[1]:
								sock = user[0]
								usr = user[1]
								delList.append(user)
								tempList.append((sock, usr, startMenu))
					try:
						hostList.remove((rsock, gameid))
					except:
						pass
	
					for user in delList:
						userList.remove(user)
					del delList[:]
					
					printMenu = createStartMenu()
					for user in tempList:
						userList.append(user)
						user[0].sendall(printMenu)
					del tempList[:]
						
				elif status == contGame:					
					currentGame.printGame()
			
			elif menu == listGameMenu:
				gameFound = 0
				printMenu = ''
				choice = rsock.recv(1024)
				if choice != 'q' and choice != 'quit':
					#add yourself to player list in game object
					for games in gameList:
						if choice == str(games.gameid):
							games.playerList.append((rsock, usr, menu, 0, 0))
							games.playerPrintGame(rsock)
							gameFound = 1
					if gameFound:
						userList.remove((rsock, usr, menu))
						userList.append((rsock, usr, gameJoin))
					else:
						rsock.sendall('No games with game id ' + choice + ' is found\n')
						rsock.sendall('Try again!\n')
						printMenu = createListGameMenu(gameList)
						rsock.sendall(printMenu) 
									
				if choice == 'q' or choice == 'quit':
					#go back to start menu
					userList.remove((rsock, usr, menu))
					userList.append((rsock, usr, startMenu))
					rsock.sendall('\n')
					printMenu = createStartMenu()
					rsock.sendall(printMenu)
			
			elif menu == gameJoin:
				currentGame = None
				userInput = rsock.recv(1024)

				#go through player list to find which game client is in
				for games in gameList:
					for players in games.playerList:
						if rsock == players[0]:
							currentGame = games
				#try:
				status = currentGame.runGame(rsock, userInput)
				#except:
						
				if status == startMenu:
					#go to start menu
					userList.remove((rsock, usr, menu))
					userList.append((rsock, usr, startMenu))
					printMenu = createStartMenu()
					rsock.sendall(printMenu)

#------------------------------------------------------------------------
#NOTE: I went this the roundabout way because python doesn't allow tuples
#	   inside a list to be changed through direct assignment

#	   For example: user[0] = xxx, user[1] = yyy, user[2] = zzz are not
#	   are not allowed. That is because tuples are immutable.
				elif status == endGame:
					
					currentGame.printGame()	
					
					#find users in game 
					for user in userList:
						for player in currentGame.playerList:               
							if user[1] == player[1]:
								sock = user[0]
								usr = user[1]
								delList.append(user)	
								tempList.append((sock, usr, startMenu))
					
					#delete host from game
					for host in hostList:
						if currentGame.gameid == host[1]:
							hostList.remove(host)

					#delete users in game
					for user in delList:
						userList.remove(user)
					del delList[:]
						
					#repopulate user list from temp list
					printMenu = createStartMenu()
					for user in tempList:
						userList.append(user)
						user[0].sendall(printMenu)
					del tempList[:]	
#------------------------------------------------------------------------
				elif status == contGame:		
					currentGame.printGame()
