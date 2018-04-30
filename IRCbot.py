#!/usr/bin/python3

import socket
import datetime

#IRC Information:
SERVER =	'irc.freenode.net'
PORT =		6667
NICKNAME =	'GromacsBot'
CHANNEL =	'#gromacs'

#Response Text:
TEXT = 'Hello, I am a bot. This is a young channel dedicated for Gromacs Molecular Dynamics Simulation, be patient and more people will join. Help us grow the channel by telling other users to join us :-)'

#Send Data
def send_data(command):
	'''To send data to IRC'''
	IRC.send((command + '\n').encode())

#Logo
print('\x1b[35m_ _ _ {} _ _ _\x1b[0m'.format(datetime.date.today()))
#print('''\x1b[32m\n╦╦═╗╔═╗  ╔╗ ╔═╗╔╦╗\n║╠╦╝║    ╠╩╗║ ║ ║ \n╩╩╚═╚═╝  ╚═╝╚═╝ ╩ \n\x1b[0m''')

#Connect To IRC:
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
	if msg == []:
		continue
	elif msg[1] == 'NOTICE':
		print('\x1b[36m{} {}\x1b[0m'.format('Calling' , msg[0]))
		server_a = msg[0].split(':')
		server_b = server_a[1]
	elif msg[1] == '001':
		print('\x1b[33m{}\x1b[0m'.format('- - CONNECTED - -'))
	elif msg[1] == 'JOIN':
		print('\x1b[32m--> {}\x1b[0m'.format(msg[0].split('!')[0].split(':')[1]))
	elif msg[1] == 'PART':
		print('\x1b[31m<-- {}\x1b[0m'.format(msg[0].split('!')[0].split(':')[1]))
	elif msg[0] == 'PING':
		server1 = msg[1].split(':')
		server2 = server1[1]
		send_data('PONG {}'.format(server2))
	#Chat
	elif msg[1] == 'PRIVMSG':
		text = ' '.join(msg[3 : ]).split(':')[1 : ][0]
		nick1 = msg[0].split('!')
		nick2 = nick1[0].split(':')
		print('{:25}|{}'.format(nick2[1] , text))
		#Response:
		for string in msg:
			if (string == ':' + NICKNAME + ':' or string == NICKNAME):
				package = 'PRIVMSG {} :{}\r\n'.format(CHANNEL , TEXT)
				IRC.send((package).encode())
				print('Sent Notice')
