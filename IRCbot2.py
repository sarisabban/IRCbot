#!/usr/bin/python3

import time
import socket
import datetime
import threading

def chat(irc, buffer, channel, v=True):
	''' Send text to IRC channel '''
	msg = 'hello'
	if v: print(f'\x1b[32m{msg}\x1b[0m')
	irc.send(f'PRIVMSG {channel} :{msg}\r\n'.encode())

def connect(server, port, nickname, channel, v=True):
	''' Maintain connection to network '''
	network = server.split('.')
	irc = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
	irc.connect((server, port))
	irc.send('USER user host server name\r\n'.encode())
	irc.send(f'NICK {nickname}\r\n'.encode())
	irc.send(f'JOIN {channel}\r\n'.encode())
	while True:
		buffer = irc.recv(4096)
		*lines, _ = buffer.split(b'\r\n')
		for line in lines:
			line = line.decode()
			server = line.split()[0][1:]
			cmd = line.split()[1] if line.startswith(':') else line.split()[0]
			if cmd == 'NOTICE':
				if v: print(f'\x1b[36mCalling {server} ...\x1b[0m')
			elif cmd == '001':
				if v: print(f'\x1b[33m- - CONNECTED - -\x1b[0m')
			elif cmd == 'JOIN':
				text = line.split('!')[0][1:]
				if v: print(f'\x1b[97m--> {text}\x1b[0m')
			elif cmd == 'PART':
				text = line.split('!')[0][1:]
				if v: print(f'\x1b[90m<-- {text}\x1b[0m')
			elif cmd == 'PING':
				irc.send((f'PONG {server}' + '\r\n').encode())
				if v: print(f'\x1b[35mPONG\x1b[0m')
			elif cmd == 'PRIVMSG':
				chat(irc, buffer, channel, v)

def main():
	''' Main function '''
	connect('irc.libera.chat', 6667, 'testing13213', '#gromacs')

if __name__ == '__main__': main()
