import random
class gameObj:
	gid = 0
	
	#constructor	
	def __init__(self, (rsock, username, menu), filename, difficulty, hallOfFame, hoff):
		#game properties
		turn = 1									#whoever created game gets first turn
		points = 0
		self.playerList = [(rsock, username, menu, turn, points)]
		gameObj.gid = gameObj.gid + 1
		self.gameid = gameObj.gid
		#game logic properties
		self.word = self.get_word(filename)
		self.wordLength = len(self.word)
		self.arrayString = ['_ '] * self.wordLength	#what string should look like to game
		self.screenString = '_ ' * self.wordLength	#what string should look like to player
		self.actualString = ''						#the string word actually compares to
		self.incorrectString = ''					
		self.diff = difficulty
		self.hof = hallOfFame
		self.actualHof = hoff

	#functions for initializing member fields
	def get_numWord(self,filename):
		numWord = 0
		f = open(filename, 'r')
		table = f.readlines()
		for word in table:	
			numWord = numWord + 1
		f.close()
		return numWord

	def	get_word(self, filename):
		numWord = self.get_numWord(filename)
		wordNumber = random.randint(1, numWord)
		f = open(filename, 'r')
		for i, word in enumerate(f, 1):
			if i == wordNumber:
				word = word.split()[0].lower()
				break
		f.close()
		return word
	
	#helper functions for game logic
#------------------------------------------------------------------------------------
	#NOTE: Calling update_arrayString automatically calls update_screenString which
	#	   automatically calls update_actualString. Think of update_arrayString as
	#	   user input trying to update the actual_string
	 
	#helper function - never gets directly called
	def update_actualString(self, screenString):
	#converts screen string into actual string
	#converts '_ _ l e t t e r s _ _ _' into __letters___'
		emptyStr = ''
		for letter in self.screenString:
			if letter != ' ':
				emptyStr = emptyStr + letter
		self.actualString = emptyStr

	#helper function - never gets directly called
	def update_screenString(self, arrayString):
		#converts array string into screen string
		# ['_ ', '_ ', '_ ', ... '_ '] into '_ ' + '_ ' + ... '_ '
		# which equals _ _ _ ... _
		emptyStr = ''
		for i, letter in enumerate(arrayString):
			emptyStr = emptyStr + arrayString[i]
		self.screenString = emptyStr
		self.update_actualString(self.screenString)

	#helper function - never gets directly called
	def update_arrayString(self, letter, index):
		#updates arrayString with user input (letter)
		self.arrayString[index] = letter + ' '
		self.update_screenString(self.arrayString)
		return 1	#update successful

	#helper function - never gets directly called
	def updateIncString(self, letter):
		if(len(self.incorrectString) > self.wordLength - 1):
			return 1	#game over 
		self.incorrectString = self.incorrectString + letter
		return 0	#not game over

	#helper function - never gets directly called
	def changeTurn(self, plyr):
		delList = []
		tempList = []

		#find player
		for player in self.playerList:
			if plyr == player:
				sock = player[0]
				username = player[1]
				menu = player[2]
				points = player[4]
				if player[3] == 1:
					turn = 0
				else:
					turn = 1
				delList.append(player)
				tempList.append((sock, username, menu, turn, points))
		
		#remove player
		for player in delList:
			self.playerList.remove(player)
		
		#add player
		for player in tempList:
			self.playerList.append(player)
			return player
		return -1	#error occured
	
	#helper function - never gets directly called	
	def addPoint(self, plyr, points):
		delList = []
		tempList = []
			
		#find player
		for player in self.playerList:
			if plyr[0] == player[0]:
				sock = player[0]
				username = player[1]
				menu = player[2]
				turn = player[3]
				points = points + player[4]
				delList.append(player)
				tempList.append((sock, username, menu, turn, points))
		
		#remove player
		for player in delList:
			self.playerList.remove(player)
		
		#add player
		for player in tempList:
			self.playerList.append(player)
			return player
		return -1	#error occured

	def highscores(self, filename, player, hoffilename):
		playerFound = 0
		playerName = player[1]
		playerScore = player[4]
		score = playerName + '\t' + str(playerScore) + '\n'

		usernameLength = len(player[1])
		scoreLength = (len(str(player[4])) * -1) - 1
		untilNull = -1

		f = open(filename, 'r')
		table = f.readlines()
		f.close()

		for i, row in enumerate(table):
			#find player with same name 
			if row[:usernameLength] == player[1]:
				playerFound = 1
				#check if recorded score is less than current score
				if int(row[scoreLength:untilNull]) < player[4]:
					#update table
						table[i] = score
		if not playerFound:
			table.append(score)
		table = [row.replace('\n', '') for row in table]
		table = [[row.split('\t')[0], row.split('\t')[1]] for row in table]
		table = sorted(table, key=lambda row: int(row[1]), reverse=True)

		#empty file before appending
		f = open(filename, 'w')
		f.close() 

		f = open(filename, 'a')
		for row in table:
			score = row[0] + '\t' + row[1] + '\n'
			f.write(score)
		f.close()

#------------------------------------------------------------------------------------

	#functions for game logic
	def runGame(self, sock, userInput):
		#should change strings based on user input using functions for game logic
		isMatch = 0
		isGameover = 0
		tookTurn = 0
		turn = 1
		gameEnd = 1
		startMenu = 2
		contGame = 3
		gameMenu = 4
		updatedPlayer = None
		if len(userInput) > 1:
			#answer is incorrect
			if userInput != self.word:
				sock.sendall('Uh oh. You Lost! Better luck next time!\n')
				sock.sendall('The answer was ' + self.word + '\n')
				numPlayers = len(self.playerList)
				for player in self.playerList:
					if sock == player[0] and numPlayers > 1:
						self.highscores(self.hof, player, self.actualHof)
						updatedPlayer = self.changeTurn(player)
						self.changeTurn(self.playerList[0])
						self.playerList.remove(updatedPlayer)
						return startMenu
					elif sock == player[0] and numPlayers == 1:
						self.highscores(self.hof, player, self.actualHof)
						return gameEnd
			
			#answer is correct
			self.screenString = userInput
			winnerName = ''
			for player in self.playerList:
				if sock == player[0]:
					updatedPlayer = self.addPoint(player, self.wordLength)
					self.highscores(self.hof, updatedPlayer, self.actualHof)
					player[0].sendall('\nCongrats! You\'ve won the game!')
					winnerName = player[1]	
					break

			for player in self.playerList:
				if player[0] != sock:
					self.highscores(self.hof, player, self.actualHof)
					player[0].sendall('\nUh oh. ' + winnerName + ' won the game! You Lost. Better luck next time!')
			return gameEnd

		else:
			for player in self.playerList:
				#Not actually player 0, player is a tuple
				#find player and see it is their turn
				if sock == player[0]:
					if player[3] == turn:
						self.changeTurn(player)
						self.changeTurn(self.playerList[0])				
						#check if user input matches any letter of the word
						for i, letter in enumerate(self.word):
							if userInput == letter:
								isMatch = self.update_arrayString(userInput, i)
								self.addPoint(player, 1)	
					
						if self.actualString == self.word:
							for player in self.playerList:
								player[0].sendall('\nCongrats! You\'ve won the game!')
								self.highscores(self.hof, player, self.actualHof)
							return gameEnd
						
						if not isMatch:
							isGameover = self.updateIncString(userInput)
							if isGameover:
								for player in self.playerList:
									player[0].sendall('\nUh oh. You Lost! Better luck next time!')
								return gameEnd
						
						return contGame
					else:
						sock.sendall('It\'s not your turn!\n')

	#functions for screen
	def printGame(self):
		turn = 1
		#should print game to every player in the game
		for player in self.playerList:
			sock = player[0]	#NOT actually player 0
								#player is a tuple
			sock.sendall('\n' + self.screenString + '\n')
			sock.sendall(self.incorrectString + '\n')
			for plyr in self.playerList:
				if plyr[3] == turn:
					sock.sendall(plyr[1] + ' ' + str(plyr[4]) + ' *\n')
				else:
					sock.sendall(plyr[1] + ' ' + str(plyr[4]) + '\n')
			sock.sendall(self.word + '\n')
		
	def playerPrintGame(self, sock):
		turn = 1
		sock.sendall('\n' + self.screenString + '\n')
		sock.sendall(self.incorrectString + '\n')
		for plyr in self.playerList:
			if plyr[3] == turn:
				sock.sendall(plyr[1] + ' ' + str(plyr[4]) + ' *\n')
			else:
				sock.sendall(plyr[1] + ' ' + str(plyr[4]) + '\n')
		sock.sendall(self.word + '\n')
