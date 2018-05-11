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

expSeqNum = '0'
while 1:
	d = s.recvfrom(1024)
	data = d[0]
	addr = d[1]

	if not data:
		break

	seqNum = data[0]
	recvData = data[1]
	recvChecksum = data[2:]
	checksum = ip_checksum(recvData)
	print 'Current sequence number: ' + seqNum
	print 'Current expected sequence number: ' + expSeqNum
	
	if seqNum == expSeqNum and checksum == recvChecksum:
		
		if expSeqNum == '0':
			expSeqNum = '1'
		else:
			expSeqNum = '0'

		print 'Current ACK sequence number: ' + seqNum
		reply = 'OK...' + recvData
		print 'Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + recvData.strip() + '\n'

		ack = 'OCK'
		ackChecksum = ip_checksum(ack)
		sndpkt = seqNum+ack+ackChecksum	
		s.sendto(sndpkt, addr)

	else:
		ack = 'ACK'
		ackChecksum = ip_checksum(ack)
		sndpkt = seqNum+ack+ackChecksum
		s.sendto(sndpkt, addr)
		print 'Data: ' + recvData
		print 'Error: Sending ACK' + seqNum + '\n'
			

s.close()
