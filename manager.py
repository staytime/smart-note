#! /usr/bin/python3





import subprocess
import os.path
import logging
import argparse
import configparser
import inspect
from enum import Enum, unique, auto





@unique
class Command(Enum):
	OPEN    = 'open'
	PUSH    = 'push'
	LOG     = 'log'



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
	h.update(b'01234567')
	h.update(str(time.time()).encode('utf-8'))
	return '%s.txt' % h.hexdigest()



def create(path, text = None):

	if not os.path.exists(path):
		with open(path, 'wt') as f:
			if not (text is None):
				f.write(str(text))

	else:
		raise Exception('File \'%s\' already exist !!' % path)



# setup env
__LOCATION__ = os.path.abspath(os.path.dirname(__file__))



# configuration
__EDITOR__               = 'C:/Program Files/Notepad++/notepad++.exe'
__OPTION__               = '-n9999999'

__DEFAULT_NOTE_MESSAGE__ = '\n\n\nNEW NOTE\n\n\n'

__LOG_FILE__             = os.path.join(__LOCATION__, 'note.log')



__STACK__                = os.path.join(__LOCATION__, 'stack.txt')
__STACK__                = BufferStack(__STACK__)



logging.basicConfig(
	filename = __LOG_FILE__,
	level = logging.DEBUG)

logging.info('start process @"%s"' % __LOCATION__)
logging.info('begin setup')




# initialize command pipe line
__COMMAND__ = list()
__COMMAND__.append(__EDITOR__)
__COMMAND__.append(__OPTION__)



logging.info('goto main')



def runCommand(command):

	logging.info('call %s' % inspect.stack()[0][3])

	try:
		logging.info('run command "%s"' % command)

		if command is Command.OPEN:
			try:
				__ = __STACK__.last()
				__COMMAND__.append(__)

			except:
				runCommand(Command.PUSH)

		elif command is Command.LOG:
			__COMMAND__.append(__LOG_FILE__)

		elif command is Command.PUSH:
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



if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument(
		'cmd', type = str, nargs = '?', default = Command.OPEN,
		help = 'it can be %s' % str(list(Command)))

	__ = parser.parse_args().cmd
	cmd = None
	
	if __ in Command:
		cmd = __

	else:
		__ = str(__).upper()

		try:
			cmd = getattr(Command, __)

		except:
			logging.info('the unknown "%s" be called' % __)
			exit(0)



	runCommand(cmd)

	__STACK__.save()




