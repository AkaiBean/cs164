f = open('hof.txt', 'r')
table = f.readlines()
f.close()



for row in table:
	#make tuple
	table2.append(row[:usernameLength], row[scoreLength:untilNull)

print table
#table = sorted(table, key=lambda variable: int(variable[-2:-1]), reverse=True)
#print table
for i, row in enumerate(table):
	if row[:4] == 'akai':
		if int(row[-2:-1]) < 10:
			table[i] = 'akai' + '\t' + '10' + '\n'
print table
table = sorted(table, key=lambda variable: variable[][-2:-1])
print table
