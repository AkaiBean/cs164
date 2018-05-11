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

i = 0
expSeqNum = 0
while 1:
	if expSeqNum > 7:
		expSeqNum = 0

	d = s.recvfrom(1024)
	recv = d[0]
	addr = d[1]

	#if recv is empty
	if not recv:
		break
	
	recvSeqNum = int(recv[0])
	recvData = int(recv[1])
	recvChksum = recv[2:]
	Chksum = ip_checksum(str(recvData))
	
	#print every 4 times
	if i % 4 == 0:
		print
	i = i + 1
	
	#if data is not corrupt
	if recvChksum == Chksum:
		#check if the sequence number is correct
		#if it is correct, send ACK and increment expected sequence number 
		#otherwise send previous ACK
		if recvSeqNum == expSeqNum:
			print 'Packet ' + str(recvSeqNum) + ' received'
			print 'ACK ' + str(expSeqNum) + ' sent'
			sndpkt = mkpkt(expSeqNum)
			expSeqNum = expSeqNum + 1
		else:
			print 'Packet ' + str(recvSeqNum) + ' received'
			print 'ACK ' + str(expSeqNum - 1) + ' sent'	
			sndpkt = mkpkt(expSeqNum - 1)
	else:
		print 'Packet ' + str(recvSeqNum) + ' received'
		print 'ACK ' + str(expSeqNum - 1) + ' sent'	
		sndpkt = mkpkt(expSeqNum - 1)
	s.sendto(sndpkt, addr)
		
s.close()
