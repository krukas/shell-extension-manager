from ExtensionStatus import ExtensionStatus
from json 		import loads, load
from Config 	import Config
from Utils 		import *
from urllib 	import urlopen, urlretrieve
from zipfile 	import ZipFile
from os 		import listdir, remove
from os.path 	import isdir
from shutil	 	import rmtree

class Extension:
	data = {}
	
	def __init__(self, jsonExInfo):
		# get json string and convert to object
		try:
			if type(jsonExInfo) == dict:
				self.data = jsonExInfo
			else:
				self.data = loads(jsonExInfo)
		except Exception:
			error("Could not import Extension info")

	def get(self, key):
		if key in self.data:
			return str( self.data[key] )
		return None

	def getName(self):
		return self.get('name').replace(' ', '-').lower()

	def getVersion(self):
		return self.get('version')

	def getUuid(self):
		return self.get('uuid')

	def getDescription(self):
		return self.get('description')

	def isInstalled(self):
		installed = False
		if self.getName() == None:
			error("Error: no extension data")

		if(isdir( Config.systemDir+self.getUuid() ) ):
			installed = True
		if(isdir( Config.userDir+self.getUuid() ) ):
			installed = True
		return installed		

	def getDownloadUrl(self):
		f_info = urlopen(Config.apiUrl+"/extension-info/?uuid="+self.getUuid()+"&shell_version="+Config.gnomeVersion)
		try:
			ex_info = load(f_info)
			return ex_info['download_url']
		except Exception, e: 
			print e
			error("Error: With downloading the extension!")

	def remove(self):
		#disable extension
		exStatus = ExtensionStatus()
		exStatus.disableExtension( self.getUuid() )
		if( isdir( Config.systemDir+self.getUuid() ) ):
			if Config.user == "root":
				rmtree(Config.systemDir+self.getUuid())
				display("Removing extension "+self.getName()+" system wide")
			else:
				display("Cant remove extension "+self.getName()+" system wide, require root privileges (sudo)")
		if(isdir( Config.userDir+self.getUuid() ) ):
			rmtree(Config.userDir+self.getUuid())
			display("Removing extension "+self.getName()+" for user")
	
	def update(self):
		if(Config.user == 'root' and isdir( Config.systemDir+self.getUuid() )):
			display("Update extension "+self.getName()+" system wide")
			Config.installDir = Config.systemDir
			self.install()

		if Config.user != 'root' and isdir( Config.systemDir+self.getUuid() ):
			display("Cant update extension "+self.getName()+" system wide, require root privileges (sudo)")
		
		if isdir( Config.userDir+self.getUuid() ):
			display("Update extension "+self.getName()+" for user") 
			Config.installDir = Config.userDir
			self.install()

	def install(self):
		if self.getName() == None:
			error("Error: no extension data")
		
		display("Installing extension "+self.getName()+" version "+self.getVersion())
		zipFile = "/tmp/"+self.getUuid()+".zip"
		installDir = Config.installDir+self.getUuid()

		#remove old extension
		self.remove()

		#Download extension
		display( " * downloading")
		urlretrieve (Config.apiUrl+self.getDownloadUrl(), zipFile)			

		#install extension
		display(" * unpacking ...")
		with ZipFile( zipFile , "r") as z:
				z.extractall(installDir)

		#enable extension
		display(" * enable extension ")
		exStatus = ExtensionStatus()
		exStatus.enableExtension( self.getUuid() )

		#Cleanup
		remove( zipFile )
