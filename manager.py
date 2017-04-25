#! /usr/bin/python3



import sys
import subprocess
import os
import os.path
import logging
import argparse



# setup env
__LOCATION__ = os.path.dirname(__file__)


# configuration
__EDITOR__               = 'C:/Program Files/Notepad++/notepad++.exe'
__OPTION__               = '-n9999999'

__DEFAULT_NOTE_FILE__    = 'note.txt'
__DEFAULT_NOTE_MESSAGE__ = '\n\n\nNEW NOTE'

__LOG_FILE__ = 'note.log'
__LOG_FILE__ = os.path.join(__LOCATION__, __LOG_FILE__)




logging.basicConfig(
	filename = __LOG_FILE__,
	level = logging.DEBUG)

logging.info('start process @"%s"' % __LOCATION__)
logging.info('begin setup')

__DEFAULT_NOTE_FILE__ = os.path.join(__LOCATION__, __DEFAULT_NOTE_FILE__)

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
	__CMD__ = ['new', 'log', 'open']
	


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




