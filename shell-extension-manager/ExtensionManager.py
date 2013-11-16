from ExtensionIndex import ExtensionIndex
from ExtensionStatus import ExtensionStatus
from Extension 	import Extension
from Config 	import Config
from Utils 		import *
from os 		import listdir

class ExtensionManager:
	installedExtensions = {}

	def __init__(self):
		self.installedExtensions = self.getInstalledExtensions()

	def install(self, extensionNames):
		index 		= ExtensionIndex()
		installList = []
		updateList 	= []
		newest		= []
		
		for ex in range(len(extensionNames)): 
			# get extension info 
			rex = index.getByName(extensionNames[ex])
			if(rex == None):
				error("Error: Extension '"+extensionNames[ex]+"' not found!")

			#check if extensions is already installed
			if(rex.isInstalled()):
				currVersion = self.installedExtensions[extensionNames[ex]].getVersion()
				remVersion	= rex.getVersion()
				#check if currunt extension is older version
				if (currVersion < remVersion):
					updateList.append(rex)
				else:
					newest.append(rex.getName()+" is already the newest version.")
			else:
				installList.append(rex)

		#print out extensions that already is installed with newest version
		for ex in range(len(newest)):
			display(newest[ex])

		self.display(installList, updateList, [])
		
		if(len(updateList) > 0):
			display("Updating extensions:")
			for ex in range(len(updateList)):
				updateList[ex].install()

		if(len(installList) > 0 ):
			display("Installing extensions:")
			for ex in range(len(installList)):
				installList[ex].install()

	def update(self):
		index 			= ExtensionIndex()
		updateList 		= []

		for name in self.installedExtensions:
			extension = index.getByName(name)
			if extension != None:
				if( self.installedExtensions[name].getVersion() <  extension.getVersion()):
					updateList.append(extension)

		self.display([], updateList, [])

		if(len(updateList) > 0):
			display("Updating extensions:")
			for ex in range(len(updateList)):
				updateList[ex].update()

	def remove(self, extensionNames):
		index 		= ExtensionIndex()
		removeList 	= []
		notInstalled= []

		for ex in range( len(extensionNames) ):
			rex = index.getByName(extensionNames[ex])
			if(rex == None):
				error("Error: Extension '"+extensionNames[ex]+"' not found!")
			if(rex.isInstalled()):
				removeList.append(rex)
			else:
				notInstalled.append(rex)

		for ex in range(len(notInstalled)):
			display(notInstalled[ex].getName()+" is not installed")
		
		self.display([],[],removeList)
			
		if(len(removeList) > 0 ):
			display("Removing extensions:")
			for ex in range(len(removeList)):
				removeList[ex].remove()

	def enable(self, name):
		if name in self.installedExtensions:
			index = ExtensionStatus()
			if index.enableExtension(name):
				display("Extension "+name+" enabled")
			else:
				display("Extension "+name+" already enabled")
		else:
			display("Extension "+name+" not installed")

	def disable(self, name):
		if name in self.installedExtensions:
			index = ExtensionStatus()
			if index.disableExtension(name):
				display("Extension "+name+" disabled")
			else:
				display("Extension "+name+" already disabled")
		else:
			display("Extension "+name+" not installed")

	def create(self, file):
		print "create "


	def display(self, installList, updateList, removeList):
		#print out to be removed extensions
		if(len(removeList) > 0 ):
			display("The following extensions will be removed:")
			for ex in range(len(removeList)):
			 	display("   "+removeList[ex].getName()+" version "+removeList[ex].getVersion())

		#print out to be installed extensions
		if(len(installList) > 0 ):
			display("The following extensions will be newly installed:")
			for ex in range(len(installList)):
			 	display("   "+installList[ex].getName()+" version "+installList[ex].getVersion())	

		#print out to be updated extensions
		if(len(updateList) > 0):
			print "The following extensions have an older version and will be updated:"
			versionNotFound = False
			for ex in range(len(updateList)):
				version = self.installedExtensions[ updateList[ex].getName() ].getVersion()
				if version == None: versionNotFound = True
			 	print "   "+updateList[ex].getName()+" "+updateList[ex].getVersion()+" => "+str(version)
			if versionNotFound:
			 	display("Some extensions have no version (None), and will be updated")

		# confirm message
		if(not Config.optYes and (len(installList) > 0 or len(updateList) > 0) or len(removeList) > 0 ):
			inputValid = False
			while (not inputValid):
				inputVar = raw_input("Do you want to continue (Yes/no): ")
				if (inputVar.lower() == 'yes' or inputVar.lower() == 'y' or inputVar == ''):
					inputValid = True
				elif(inputVar.lower() == 'no' or inputVar.lower() == 'n'):
					error("Installation canceled")

	def getInstalledExtensions(self):
		curInstalledExtensions = {}
		#get system wide extension
		for fn in listdir(Config.systemDir):
			json_data=open(Config.systemDir+fn+"/metadata.json")
			extension = Extension(json_data.read())
			curInstalledExtensions[extension.getName()] = extension

		#get user extensions
		for fn in listdir(Config.userDir):
			json_data=open(Config.userDir+fn+"/metadata.json")
			extension = Extension(json_data.read())
			if not extension.getName() in curInstalledExtensions:
				curInstalledExtensions[extension.getName()] = extension

		return curInstalledExtensions