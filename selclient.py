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

#set up window
base = 0
windowSize = 4
nextSeqNum = 0
maxSeqNum = 8

#whether packet should corrupt
isCorrupt = 1

#function to make packets
def mkpkt(seqNum, data):
	global isCorrupt
	chksum = ip_checksum(str(data))
	if isCorrupt == 1 and data == 1:
		isCorrupt = 0
		chksum = 'corrupted'
	pkt = str(seqNum) + str(data) + chksum
	return pkt

#function to add timer to packet and send
def timerStart(nextSeqNum, threadList, index):
	threadList[index] = threading.Timer(2, timerStart, [nextSeqNum, threadList, index])
	threadList[index].start()
	sndpkt = mkpkt(nextSeqNum, nextSeqNum)
	s.sendto(sndpkt, (host, port))
	print 'Packet ' + str(nextSeqNum) + ' sent'


def resetWindow():
	global base, nextSeqNum
	base = 0
	nextSeqNum = 0

def findBase(ackList, base, windowSize):
	global error
	for i in range(base, base + windowSize):
		if ackList[i] == error:
			return i
	#only reaches here if there is no error
	nextSeqNum = base + windowSize
	return nextSeqNum

#used if the ack number is corrupt
error = -1

while 1:
	msg = raw_input('Press enter to send: ')
	try:
		#resets base and next sequence number
		resetWindow()
		#initialize thread list of size 4
		threadList = [None] * windowSize
		#initialize ack list of size 8
		ackList = [error] * maxSeqNum

		for i in range(base, base + windowSize):
			timerStart(nextSeqNum, threadList, i)
			nextSeqNum = nextSeqNum + 1
		
		while 1:
			d = s.recvfrom(1024)
			reply = d[0]

			ackNum = int(reply[0])
			ackChksum = reply[1:]
			chksum = ip_checksum(str(ackNum))

			#check if ACK is corrupt
			if ackChksum == chksum:
				ackList[ackNum] = ackNum
				#ACK received correctly so cancel timer
				index = ackNum % 4
				threadList[index].cancel()
				
				print 'ACK ' + str(ackNum) + ' received'
				
				if base == maxSeqNum - 1:
					break

				#check if next packet sent is in sender window
				#base + windowSize is packet number
				#nextSeqNum is index number
				if nextSeqNum < maxSeqNum and base == ackNum:
					#index should be nextSeqNum % 4 
					index = nextSeqNum % 4
					timerStart(nextSeqNum, threadList, index)
					nextSeqNum = nextSeqNum + 1
					#move window
					base = findBase(ackList, base, windowSize)
			else:
				ackList[ackNum] = error
				print 'Corrupt ACK ' + str(ackNum) + ' received'
					
	except socket.error, msg:
		print 'Error Code: ' + str(msg[0]) + 'Message ' + msg[1]
		sys.exit()
