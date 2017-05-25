#! /usr/bin/python3



import sys
import subprocess
import os
import os.path
import logging
import argparse
import configparser



class BufferStack(object):
	def __init__(self, file):
		self.stack = list()
		self.file = file

		if os.path.exists(file):
			with open(file, 'rt') as f:
				__ = f.read()
				__ = [x.strip() for x in __.split('\n')]
				__ = [x for x in __ if len(x) > 0]
				for i in __:
					self.push(i)

	def save(self):
		with open(self.file, 'wt') as f:
			__ = '\n'.join(self.stack)
			f.write(__)

	def last(self):
		return self.stack[-1]

	def push(self, x):
		self.stack.append(x)

	def pop(self):
		return self.pop()

def getNewName():
	import time
	from hashlib import sha1

	h = sha1()
	h.update(b'0123456')
	h.update(str(time.time()).encode('utf-8'))
	return h.hexdigest()



# setup env
__LOCATION__ = os.path.dirname(__file__)



# __CONFIG__ = os.path.join(__LOCATION__, 'config.ini')

# config = configparser.ConfigParser()
# config.read(__CONFIG__)
# config.sections()





# configuration
__EDITOR__               = 'C:/Program Files/Notepad++/notepad++.exe'
__OPTION__               = '-n9999999'

__DEFAULT_NOTE_FILE__    = 'note.txt'
__DEFAULT_NOTE_MESSAGE__ = '\n\n\nNEW NOTE\n\n\n'

__STACK__                = os.path.join(__LOCATION__, 'stack.txt')

__STACK__                = BufferStack(__STACK__)





# get abs path
__DEFAULT_NOTE_FILE__ = os.path.join(__LOCATION__, __DEFAULT_NOTE_FILE__)

__LOG_FILE__ = os.path.join(__LOCATION__, 'note.log')



logging.basicConfig(
	filename = __LOG_FILE__,
	level = logging.DEBUG)

logging.info('start process @"%s"' % __LOCATION__)
logging.info('begin setup')




# initialize command pipe line
__COMMAND__ = list()
__COMMAND__.append(__EDITOR__)
__COMMAND__.append(__OPTION__)



def create(path, text = None):
	if not os.path.exists(path):
		with open(path, 'wt') as f:
			if not (text is None):
				f.write(str(text))
	else:
		raise Exception('File \'%s\' already exist !!' % path)



logging.info('goto main')

if __name__ == '__main__':

	# the white list of commands
	__CMD__ = ['new', 'log', 'open', 'push']
	


	parser = argparse.ArgumentParser()
	
	parser.add_argument(
		'cmd', type = str, nargs = '?', default = 'open',
		help = 'it can be %s' % str(__CMD__))

	command = parser.parse_args()
	command = command.cmd

	if not (command in __CMD__):
		logging.info('the unknown "%s" be called' % command)
		exit(0)



	try:
		logging.info('run command "%s"' % command)

		if command == 'open':
			try:
				create(__DEFAULT_NOTE_FILE__, __DEFAULT_NOTE_MESSAGE__)
			except:
				pass

			__COMMAND__.append(__DEFAULT_NOTE_FILE__)

		elif command == 'log':
			__COMMAND__.append(__LOG_FILE__)

		elif command == 'push':
			__ = getNewName()
			__STACK__.push(__)
			__ = os.path.join(__LOCATION__, __)
			__COMMAND__.append(__)
			create(__, __DEFAULT_NOTE_MESSAGE__)
			

		else:
			raise Exception('function "%s" havn\'t be implement yet.' % command)

	except Exception as e:
		logging.error(str(e))
		exit(0)



	# try to do the job
	try:
		subprocess.run(__COMMAND__)
	except Exception as e:
		logging.error(str(e))
		exit(-1)


	__STACK__.save()



