from check import ip_checksum
import time
import threading
import socket
import sys
	
HOST = ''
PORT = 8888

try:
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	print 'Socket created'
except socket.error, msg :
	print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()

try:
	s.bind((HOST, PORT))
except socket.error, msg:
	print 'Bind failed. Error Code: ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()

print 'Socket bind complete'

def mkpkt(ackNum):
	chksum = ip_checksum(str(ackNum))
	pkt = str(ackNum) + chksum
	return pkt

#setup window
base = 0
windowSize = 4
maxSeqNum = 8

#check if packet is out of bounds

while 1:

	d = s.recvfrom(1024)
	recv = d[0]
	addr = d[1]

	#if recv is empty break
	if not recv:
		break
	
	#open package
	recvSeqNum = int(recv[0])
	recvData = int(recv[1])
	recvChksum = recv[2:]
	chksum = ip_checksum(str(recvData))
	
	#check if data is corrupt
	if recvChksum == chksum:
		#check receive sequence number in relation to base
		
		#if this happens I know window is full
		if recvSeqNum > base and recvSeqNum >= base + windowSize:
			base = recvSeqNum
		#duplicate packet
		if recvSeqNum < base:
			print '< Packet ' + str(recvSeqNum) + ' received'
			sndpkt = mkpkt(recvSeqNum)
		#some packets missing waiting to be received
		if recvSeqNum > base and recvSeqNum < base + windowSize:
			print '> Packet ' + str(recvSeqNum) + ' received'
			sndpkt = mkpkt(recvSeqNum)
		#according to plan bitches
		if recvSeqNum == base:
			print '== Packet ' + str(recvSeqNum) + ' received'
			sndpkt = mkpkt(recvSeqNum)
			base = base + 1
		
		s.sendto(sndpkt, addr)
		print 'ACK ' + str(recvSeqNum) + ' sent'
		
		if base == maxSeqNum:
			#reset base
			base = 0
	else:
		print 'Corrupt packet ' + str(recvSeqNum) + ' received'

		
s.close()
