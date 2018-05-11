f = open('wordlist.txt', 'r')
for i, word in enumerate(f, 1):
	if i == 1:
		print word.split()
		break
f.close()
