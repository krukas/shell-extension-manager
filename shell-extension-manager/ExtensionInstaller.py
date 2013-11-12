from ExtensionStatus import ExtensionStatus
from Utils 		import *
from Config 	import Config
from os 		import listdir, remove
from os.path 	import isfile, isdir
from shutil	 	import rmtree
from json 		import load
from urllib 	import urlopen, urlretrieve
from zipfile 	import ZipFile

class ExtensionInstaller:

	def install(self, extensions, optYes):
		currExt 	= self.getInstalledExtensions()
		installList = []
		updateList 	= []
		newest		= []
		
		display("Checking for newest version.")
		for ex in range(len(extensions)): 
			# get extension info 
			rex = self.searchExtension(extensions[ex])
			if(rex == None):
				error("Error: Extension '"+extensions[ex]+"' not found!")

			#check if extensions is already installed
			if(extensions[ex] in currExt):
				name = rex['name'].replace(' ', '-').lower()
				currVersion = currExt[extensions[ex]]['version']
				remVersion	= rex['version']
				#check if currunt extension is older version
				if (currVersion < remVersion):
					updateList.append(rex)
				else:
					newest.append(name+" is already the newest version.")
			else:
				installList.append(rex)

		#print out extensions that already is installed with newest version
		for ex in range(len(newest)):
			display(newest[ex])

		#print out to be installed extensions
		if(len(installList) > 0 ):
			display("The following extensions will be newly installed:")
			for ex in range(len(installList)):
				name = installList[ex]['name'].replace(' ', '-').lower()
			 	display("   "+name+" version "+str(installList[ex]['version']))	

		#print out to be updated extensions
		if(len(updateList) > 0):
			print "The following extensions have an older version and will be updated:"
			for ex in range(len(updateList)):
				name = updateList[ex]['name'].replace(' ', '-').lower()
			 	print "   "+name+" "+str(updateList[ex]['version'])+" => "+str(currExt[name]['version'])

		# confirm message
		if(not optYes and (len(installList) > 0 or len(updateList) > 0) ):
			inputValid = False
			while (not inputValid):
				inputVar = raw_input("Do you want to continue (Yes/no): ")
				if (inputVar.lower() == 'yes' or inputVar.lower() == 'y' or inputVar == ''):
					inputValid = True
				elif(inputVar.lower() == 'no' or inputVar.lower() == 'n'):
					error("Installation canceled")
		
		if(len(updateList) > 0):
			display("Updating extensions:")
			self.updateExtensions(updateList)
		if(len(installList) > 0 ):
			display("Installing extensions:")
			self.installExtensions(installList)

	def update(self, extensions, optYes):
		#https://extensions.gnome.org/extension-info/?uuid=topIcons@adel.gadllah@gmail.com&shell_version=3.8
		display("Updating ...")

	def remove(self, extensions):
		print ""

	def installExtensions(self, extensions):
		self.downloadExtensions(extensions)
		exStatus = ExtensionStatus()
		for ex in range(len(extensions)):
			name = extensions[ex]['name'].replace(' ', '-').lower()
			display("Installing extension "+name+" version "+str(extensions[ex]['version']))
			
			zipFile = "/tmp/"+extensions[ex]['uuid']+".zip"
			with ZipFile( zipFile , "r") as z:
				z.extractall(Config.installDir+"/"+extensions[ex]['uuid'])
			display(" - Enable extension")
			exStatus.enableExtension(extensions[ex]['uuid'])
			remove(zipFile)	
			

	def updateExtensions(self, extensions):
		self.removeExtensions(extensions)
		self.installExtensions(extensions)

	def removeExtensions(self, extensions):
		for ex in range(len(extensions)):
			exPath = Config.installDir+"/"+extensions[ex]['uuid']
			name = extensions[ex]['name'].replace(' ', '-').lower()
			if(isdir(exPath)):
				rmtree(exPath)
				display("Removing extension "+name+" version "+str(extensions[ex]['version']))

	def downloadExtensions(self, extensions):
		for ex in range(len(extensions)):
			name = extensions[ex]['name'].replace(' ', '-').lower()
			display("Downloading extension "+name+" version "+str(extensions[ex]['version']))
			urlretrieve (Config.apiUrl+extensions[ex]['download_url'], "/tmp/"+extensions[ex]['uuid']+".zip")

	def getInstalledExtensions(self):
		curInstalledExtensions = {}
		for fn in listdir(Config.installDir):
			if(Config.installDir+fn+"/metadata.json"):
				json_data=open(Config.installDir+fn+"/metadata.json")
				extension = load(json_data)
				name = extension['name'].replace(' ', '-').lower() 
				curInstalledExtensions[name] = extension
		return curInstalledExtensions

	def getNewExtensionInfo(self, id):
		f_info = urlopen(Config.apiUrl+"/extension-info/?pk="+str(id)+"&shell_version="+Config.gnomeVersion)
		try:
			return load(f_info)
		except Exception:
			error("Error: With getting the extension!")

	def searchExtension(self, name):
		f_info = urlopen(Config.apiUrl+"/extension-query/?page=1&shell_version="+Config.gnomeVersion+"&search="+name)
		try:
			ex_info = load(f_info)
			if(len(ex_info['extensions']) < 1):
				return None

			if(ex_info['extensions'][0]['name'].replace(' ', '-').lower() == name):
				return self.getNewExtensionInfo(ex_info['extensions'][0]['pk'])
			else:
				return None
		except Exception, e:
			error("Error: With getting the extension!")