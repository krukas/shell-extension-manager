#!/usr/bin/env python
from ExtensionManager import ExtensionManager
from Config import Config
from sys import argv
from sys import exit

# command name
COMMAND = ""

# Argumenten
ARGS = []

# Create the ExtensionManager
exManager = ExtensionManager()

# Check if command is given
if(len(argv) < 2):
	exManager.print_help()
	exit()

commands = ['install', 'remove', 'update', 'show', 'search', 'create', 'enable', 'disable']

# check if command is valid
if(argv[1] in commands):
	COMMAND = argv[1]
else:
	exManager.print_help()
	exit()

# check for arguments
if(len(argv) > 2 ):
	for x in xrange(2,len(argv)):
		arg = argv[x]
		if(arg == "-h" or arg == "--help"):
			exManager.print_help()
			exit()
		elif(arg == "-q" or arg == "--quiet"):
			Config.optQuiet = True
		elif(arg == "-y" or arg == "--yes"):
			Config.optYes = True
		elif(arg == "-a" or arg == "--all"):
			Config.optAll = True
		elif(arg == "-l" or arg == "--list"):
			Config.optList = True
		else:
			ARGS.append(arg)

commands = ['install', 'remove', 'search', 'create', 'enable', 'disable']

if(COMMAND in commands and len(ARGS) <= 0 ):
	exManager.print_help()
	exit()

if(COMMAND == 'install'):
	exManager.install(ARGS)

elif(COMMAND == 'remove'):
	exManager.remove(ARGS)

elif(COMMAND == 'update'):
	exManager.update(ARGS)

elif(COMMAND == 'enable'):
	exManager.enable(ARGS)

elif(COMMAND == 'disable'):
	exManager.disable(ARGS)

elif(COMMAND == 'show'):
	exManager.show(ARGS)

elif(COMMAND == 'create'):
	exManager.create(ARGS)






