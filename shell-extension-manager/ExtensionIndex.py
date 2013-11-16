#!/usr/bin/env python
from Extension 	import Extension
from Config 	import Config
from Utils 		import *
from urllib 	import urlopen
from json 		import load, dumps
from os 		import remove
from os.path	import dirname, realpath
from os.path 	import isfile
from re 		import compile

class ExtensionIndex:
	indexFile 		= ""
	extensionsIndex = {}
	numberOfPages 	= 1
	updated 		= False

	def __init__(self):
		self.indexFile = str(dirname( realpath(__file__) ))+"/index.json"
		if( not isfile( self.indexFile )):
			display("Downloading extensions index")
			self.updateIndex()
		self.loadIndex()

	def loadIndex(self):
		if(isfile(self.indexFile)):
			f = open(self.indexFile,'r')
			self.extensionsIndex = load(f)

	def getByName(self, name):
		if(name in self.extensionsIndex):
			extension = self.extensionsIndex[name]
			extension['name'] = name
			return Extension(extension)

	def search(self, search):
		search = str(search).replace('-', '|').lower()
		results = []
		for (name, value) in self.extensionsIndex.items():
			re = compile(search)
			match = re.match(name)
			if match != None:
				extension = value
				extension['name'] = name
				results.append( Extension(extension) )
		return results

	def updateIndex(self):
		if self.updated: return
		
		#Get System main Version
		system_version = Config.gnomeVersion.split('.')
		if len(system_version) > 2: system_version.pop(2)
		system_version = '.'.join(system_version)
		
		index = {} 
		page = 1;
		while page <= self.numberOfPages:
			extensions = self.getPage(page)
			display("Getting page "+str(page)+" from "+str(self.numberOfPages) )
			for ex in range(len(extensions)):
				name = str(extensions[ex]['name']).replace(' ', '-').lower()
				exinfo = {}
				
				#get extension version
				versions = extensions[ex]['shell_version_map']
				for (version, value) in versions.items():
					ex_version = version.split('.')
					if len(ex_version) > 2: ex_version.pop(2)
					ex_version = '.'.join(ex_version)
					if system_version == ex_version:
						exinfo['version'] = versions[version]['version']
						break
				
				exinfo['uuid'] = extensions[ex]['uuid']
				exinfo['description'] =  extensions[ex]['description']
				index[name] = exinfo
			page += 1

		#remove old index file
		if(isfile(self.indexFile)):
			remove(self.indexFile)

		json_index = dumps(index)
		f = open(self.indexFile,'w')
		f.write(json_index)
		f.close()
		self.updated = True

	def getPage(self, pageNumber):
		f_page = urlopen(Config.apiUrl+"/extension-query/?page="+str(pageNumber)+"&shell_version="+Config.gnomeVersion)
		try:
			ex_page = load(f_page)
			self.numberOfPages = ex_page['numpages']
			return ex_page['extensions']
		except Exception, e:
			error("Error: With getting the extensions list!")
