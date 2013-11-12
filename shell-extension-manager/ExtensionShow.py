from ExtensionStatus import ExtensionStatus
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
			extension = load(json_data)
			name = extension['name'].replace(' ', '-').lower() 
			extension['install'] = 'System'

			if(optActive):
				if(extension['uuid'] in activeExt):
					showList[name] = extension
			else:
				showList[name] = extension

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
			extension = load(json_data)
			name = extension['name'].replace(' ', '-').lower() 
			if(name in showList):
				showList[name]['install'] += ', User' 
				continue
			extension['install'] = 'User'
			if(optActive):
				if(extension['uuid'] in activeExt):
					showList[name] = extension
			else:
				showList[name] = extension
		
		for ex in sorted(showList):
			
			if(showList[ex]['uuid'] in activeExt):
				display( "*"+ex )
			else:
				display( ex )
			if(optList):
				display( "Location:\t"+showList[ex]['install'] )
				display( "UUID:    \t"+showList[ex]['uuid'])
				display( "Description:\t"+showList[ex]['description'])
				display("---")