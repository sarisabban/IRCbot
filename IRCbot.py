#!/usr/bin/python3

import socket

#IRC Information:
SERVER =	'irc.freenode.net'
PORT =		6667
NICKNAME =	'NoticeBot'
CHANNEL =	'#gromacs'

#Response Text:
TEXT='Hello, I am a bot. This is a young channel, be patient and more people will join. Help us by telling other users to join here so we can have a community with everyone helping each other use Gromacs. :-)'

#Connect To IRC:
def send_data(command):
	'''To send data to IRC'''
	IRC.send((command + '\n').encode())

#Logo
print('''\x1b[32m
╦╦═╗╔═╗  ╔╗ ╔═╗╔╦╗
║╠╦╝║    ╠╩╗║ ║ ║ 
╩╩╚═╚═╝  ╚═╝╚═╝ ╩ 
\x1b[0m''')

network = SERVER.split('.')
IRC = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
IRC.connect((SERVER , PORT))
send_data('USER user host server name')
send_data('NICK ' + NICKNAME)
send_data('JOIN ' + CHANNEL)

#Maintian Connection:
while True:
	buffer = IRC.recv(1024)
	msg = buffer.decode().split()
	#print(msg)
	if msg[1] == 'NOTICE':
		print('\x1b[36m' + 'Calling' + msg[0] + '\x1b[0m')
		server_a = msg[0].split(':')
		server_b = server_a[1]
	if msg[1] == 'JOIN':
		print('\x1b[33m' + '---------------------------')
		print('\tCONNECTED')
		print('Network:\t' , network[1] , '\nServer:\t\t' , server_b , '\nChannel:\t' , msg[2])
		print('---------------------------' + '\x1b[0m')
	if msg[0] == 'PING': #When server pings answer with pong to maintain connection.
		server1 = msg[1].split(':')
		server2 = server1[1]
		send_data('PONG %s' % server2)
		#print('Received' , msg[0] , 'from' , msg[1] , 'Sent back:' , 'PONG')

#Response:
	if msg[1] == 'PRIVMSG':
		text = ' '.join(msg[3 : ])
		nick1 = msg[0].split('!')
		nick2 = nick1[0].split(':')
		print(nick2[1] , '\t' , text)
		for string in msg:
			if (string == ':' + NICKNAME + ':' or string == NICKNAME):
				IRC.send(('PRIVMSG ' + CHANNEL + ' :' + TEXT + '\r\n').encode())
				print(TEXT)
