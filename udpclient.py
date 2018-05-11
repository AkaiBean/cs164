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
seqNum = '1'

while(1):
	msg = raw_input('Press enter to send: ')
	try:
		for number in range(1):
			data = str(number)
			checksum = ip_checksum(data)
			if seqNum == '1':
				seqNum = '0'
			else:
				seqNum = '1'
			
			sndpkt = seqNum+data+checksum
			for i in range(4):
				s.sendto(sndpkt, (host, port))

#			data = 'a'
#			checksum = ip_checksum(data)
#			sndpkt = seqNum+data+checksum
#			t = threading.Timer(1, s.sendto, [sndpkt, (host, port)])
#			t.start()

			d = s.recvfrom(1024)
			reply = d[0]
			reply2 = d[1]

			pktSeqNum = reply[0]
			pktData = reply[1:4]
			pktRecvChecksum = reply[4:]
			pktChecksum = ip_checksum(pktData)
			print 'Packet ' + seqNum + ' sent'
			print 'ACK ' + pktSeqNum + ' received'
			
			if pktSeqNum == seqNum and pktRecvChecksum == pktChecksum:
#				t.cancel()
				print 'Server reply: ' + pktData + ' ' + pktSeqNum + '\n'
				print reply2	
			
			while(pktSeqNum != seqNum or pktRecvChecksum != pktChecksum):
				print 'Error: Received bad ACK .. Wait for timeout'
				d = s.recvfrom(1024)
				reply = d[0]
				addr = d[1]
				
				pktSeqNum = reply[0]
				pktData = reply[1:4]
				pktRecvChecksum = reply[4:]
				

	
	except socket.error, msg:
		print 'Error Code: ' + str(msg[0]) + 'Message ' + msg[1]
		sys.exit()
