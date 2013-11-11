from Config import Config

def error(error):
	print error
	exit()

def display(message):
	if( not Config.optQuiet):
		print message