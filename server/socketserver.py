# -*- coding: utf-8 -*-

import socket
import threading
import json
import sys

HOST = '127.0.0.1'	#127.0.0.1 for native access, leave a blank or fill in with 0.0.0.0 for remote access
PORT = 32123		#the binding port
RECVBUFFER = 1024	#the maximum amount of data to be received at once
MAXTHREADS = 100	#the maximum threads
RELEASEPKG = True	#if release the model which was imported by a client call
APPFOLDER = 'app'	#folder name of the python script which is waiting for client call

class Gear(threading.Thread):
	def __init__(self, socket):
		threading.Thread.__init__(self)
		self.socket = socket

	def run(self):
		while True:
			self.socket.listen(5)
			clientsock, clientaddr = self.socket.accept()
			print 'Got connection from', clientsock.getpeername()
			print self.getName(), 'is handling this connection.'
			datasize = clientsock.recv(11)
			try:
				datasize = int(float(datasize))
			except:
				datasize = 0

			data = ''
			while True:
				recv = clientsock.recv(RECVBUFFER)
				datasize -= RECVBUFFER
				data += recv
				if datasize <= 0:
					break

			try:
				datamap = json.loads(data)
			except:
				datamap = {'entry': '', 'func': '', 'param': []}

			entry = datamap['entry']
			func = datamap['func']
			param = datamap['param']
			e = ''
			try:
				src = __import__(APPFOLDER + '.' + entry, globals(), locals(), -1)
				if len(param) == 0:
					try:
						exec("result = src." + func + "()")
					except Exception as e:
						result = []
				else:
					for i in range(0, len(param)):
						param[i] = str(param[i])
						paramstring = "','".join(param)
					try:
						exec("result = src." + func + "('" + paramstring + "')")
					except Exception as e:
						result = []
				if RELEASEPKG:
					try:
						exec("del sys.modules['" + APPFOLDER + '.' + entry + "']")
						#del src
					except:
						pass
			except Exception as e:
				result = []

			send = json.dumps({'data': result, 'error': str(e)})
			sendsize = len(send)
			sendsize = str(sendsize) + '.'
			if len(sendsize) > 11:
				pass
			while len(sendsize) < 11:
				sendsize += '0'
			send = sendsize + send
			clientsock.send(send)
			clientsock.close()

class Engine():
	def __init__(self):
		self.socket = None

	def run(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			self.socket.bind((HOST, PORT))
		except:
			print 'PPY ERROR[PYTHON]: socket.bind() error'
			raise SystemExit
		i = 0
		while i < MAXTHREADS:
			gear = Gear(self.socket)
			gear.start()
			i += 1


if __name__ == '__main__':
	engine = Engine()
	engine.run()
