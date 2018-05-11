def createWelMenu():
	title = '\nWelcome Menu\n'
	opt1 = '1. Login\n'
	opt2 = '2. Make New User\n'
	opt3 = '3. Hall of Fame\n'
	opt4 = '4. Exit\n'
	prompt = '<You> '
	menu = title + opt1 + opt2 + opt3 + opt4 + prompt
	return menu

def createStartMenu():
	title = '\nStart Menu\n'
	opt1 = '1. Start New Game\n'
	opt2 = '2. Get List of the Games\n'
	opt3 = '3. Hall of Fame\n'
	opt4 = '4. Exit\n'
	prompt = '<You> '
	menu = title + opt1 + opt2 + opt3 +opt4 + prompt
	return menu

def createDiffMenu():
	title = '\nChoose the difficulty\n'
	opt1 = '1. Easy\n'
	opt2 = '2. Medium\n'
	opt3 = '3. Hard\n'
	prompt = '<You> '
	menu = title + opt1 + opt2 + opt3 + prompt
	return menu

def createListGameMenu(gameList):
	emptyStr = ''
	title = '\nList of Avaliable Games\n'
	#framwork is '1. User's game.gameid
	for i, games in enumerate(gameList, 1):
		emptyStr = emptyStr + str(i) + '. ' + games.playerList[0][1] + '\'s game (gameid: ' + str(games.gameid) + ')\n'
	prompt = '<join> '
	menu = title + emptyStr + prompt
	return menu

def createHallofFame(filename):
	emptyStr = '\n'
	f = open(filename, 'r')
	table = f.readlines()
	for row in table:
		emptyStr = emptyStr + row
	return emptyStr

def createServerMenu():
	title = '\nServer Menu\n'
	opt1 = '1. Current List of Users\n'
	opt2 = '2. Current List of Words\n'
	opt3 = '3. Add new word to the list of words'
	menu = title + opt1 + opt2 + opt3
	return menu
