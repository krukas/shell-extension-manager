#!/usr/bin/env python
from ExtensionController import ExtensionController
from Config import Config
from sys import argv
from sys import exit

# command name
COMMAND = ""

# Argumenten
ARGS = []

# Create the ExtensionManager
exController = ExtensionController()

# Check if command is given
if(len(argv) < 2):
	exController.print_help()
	exit()

commands = ['install', 'remove', 'update', 'update-index', 'show', 'search', 'create', 'enable', 'disable']

# check if command is valid
if(argv[1] in commands):
	COMMAND = argv[1]
else:
	exController.print_help()
	exit()

# check for arguments
if(len(argv) > 2 ):
	for x in xrange(2,len(argv)):
		arg = argv[x]
		if(arg == "-h" or arg == "--help"):
			exController.print_help()
			exit()
		elif(arg == "-q" or arg == "--quiet"):
			Config.optQuiet = True
		elif(arg == "-y" or arg == "--yes"):
			Config.optYes = True
		elif(arg == "-a" or arg == "--active"):
			Config.optActive = True
		elif(arg == "-l" or arg == "--list"):
			Config.optList = True
		else:
			ARGS.append(arg)

commands = ['install', 'remove', 'search', 'create', 'enable', 'disable']

if(COMMAND in commands and len(ARGS) <= 0 ):
	exController.print_help()
	exit()

if(COMMAND == 'install'):
	exController.install(ARGS)

elif(COMMAND == 'remove'):
	exController.remove(ARGS)

elif(COMMAND == 'update'):
	exController.update(ARGS)

elif(COMMAND == 'update-index'):
	exController.updateIndex()

elif(COMMAND == 'enable'):
	exController.enable(ARGS)

elif(COMMAND == 'disable'):
	exController.disable(ARGS)

elif(COMMAND == 'show'):
	exController.show(ARGS)

elif(COMMAND == 'create'):
	exController.create(ARGS)






