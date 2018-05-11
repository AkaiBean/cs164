from check import ip_checksum
import threading
import socket
import sys

try:
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
	print 'Failed to create socket'
	sys.exit()

host = 'localhost';
port = 8888;

#t to reference thread
t = None

#set up window
base = 0
nextSeqNum = 0
maxSeqNum = 7
windowSize = 4
#number of times I want to send 4 packets at a time with infinite sequence numbers
iteration = 2
#whether packet is corrupted
isCorrupt = 1
#expected ACK number
expACKNum = 0

def mkpkt(seqNum, data):
	global isCorrupt
	if isCorrupt == 1 and data == 1:
		isCorrupt = 0
		chksum = 'corrupted'
	else:
		chksum = ip_checksum(str(data))
#	chksum = ip_checksum(str(data))
	pkt = str(seqNum) + str(data) + chksum
	return pkt

#function to start timer for resending packet
def timerStart(base, windowSize):
	global t
	global nextSeqNum
	t = threading.Timer(2, timerStart, [base, windowSize])
	t.start()
	print
	for i in range(base, base + windowSize):
		if i <= maxSeqNum:
			sndpkt = mkpkt(i, i)
			s.sendto(sndpkt, (host, port))
			nextSeqNum = i + 1
			print 'packet ' + str(i) + ' sent'	

def resetWindow():
	global base
	global nextSeqNum
	global expACKNum
	if  base > maxSeqNum:
		base = 0
		nextSeqNum = 0
		expACKNum = 0

	
while 1:
	msg = raw_input('Press enter to send: ')
	try:
		#reset
		resetWindow()

		#run iteration 2 times
		for _ in range(iteration):
			if base == nextSeqNum:
				timerStart(base, windowSize)
			
			while 1:
				d = s.recvfrom(1024)
				reply = d[0]
				ackNum = int(reply[0])
				ackChksum = reply[1:]
				Chksum = ip_checksum(str(ackNum))
				
				#ACK is not corrupt and correct ACK number
				if ackChksum == Chksum and ackNum == expACKNum:
					expACKNum = expACKNum + 1
					base = ackNum + 1
					#if base is at end of window cancel timer
					if base == nextSeqNum:
						t.cancel()
						break
					else:
						#cancel timer for batch
						#move window
						#start timer for new batch/window 
						t.cancel()
						t = threading.Timer(2, timerStart, [base, windowSize])
						t.start()
						
	except socket.error, msg:
		print 'Error Code: ' + str(msg[0]) + 'Message ' + msg[1]
		sys.exit()
