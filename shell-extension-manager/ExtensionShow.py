from ExtensionStatus import ExtensionStatus
from Extension 	import Extension
from Config 	import Config
from Utils 		import *
from json 		import load
from os 		import listdir

class ExtensionShow:
	def show(self, optList, optActive):
		showList 	= {}
		activeExt 	= []

		#get active extensions
		exStatus = ExtensionStatus()
		activeExt = exStatus.activeExtensions()
		
		#get system wide extensions
		for fn in listdir('/usr/share/gnome-shell/extensions/'):
			json_data=open('/usr/share/gnome-shell/extensions/'+fn+"/metadata.json")
			extension = Extension(json_data.read())
			extension.install = 'System'

			if(optActive):
				if(extension.getUuid() in activeExt):
					showList[extension.getName()] = extension
			else:
				showList[extension.getName()] = extension

		#get user
		user = None
		if(Config.user == "root" and Config.sudoUser != None):
			user = Config.sudoUser
		else:
			user = Config.user

		#get user extensions
		userDir = '/home/'+user+'/.local/share/gnome-shell/extensions/'
		for fn in listdir(userDir):
			json_data=open(userDir+fn+"/metadata.json")
			extension = Extension(json_data.read())

			if(extension.getName() in showList):
				showList[extension.getName()].install += ', User' 
				continue
			extension.install = 'User'
			if(optActive):
				if(extension.getUuid() in activeExt):
					showList[extension.getName()] = extension
			else:
				showList[extension.getName()] = extension
		
		for ex in sorted(showList):
			
			if(showList[ex].getUuid() in activeExt):
				display( "*"+ex )
			else:
				display( ex )
			if(optList):
				display( "Location:\t"+showList[ex].install )
				display( "UUID:    \t"+showList[ex].getUuid())
				display( "Description:\t"+showList[ex].getDescription())
				display("---")