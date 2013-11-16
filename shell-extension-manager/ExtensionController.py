from os 		import getenv
from os.path 	import isfile
from xml.dom 	import minidom
from Config 	import Config
from Utils 		import *
from ExtensionManager import ExtensionManager
from ExtensionShow 		import ExtensionShow
from ExtensionIndex import ExtensionIndex

class ExtensionController:
	
	def __init__(self):	
		self.init()
	
	def init(self):
		# get user and sudo user
		Config.user 	= getenv("USER")
		Config.sudoUser = getenv("SUDO_USER")
		
		# set the install dir
		if(Config.user == 'root'):
			Config.installDir = '/usr/share/gnome-shell/extensions/'
			if(Config.user == "root" and Config.sudoUser != None):
				Config.userDir = '/home/'+Config.sudoUser+'/.local/share/gnome-shell/extensions/'
			else:
				Config.userDir ='/home/root/.local/share/gnome-shell/extensions/'
		else:
			Config.installDir = '/home/'+Config.user+'/.local/share/gnome-shell/extensions/'
			Config.userDir = Config.installDir

		# get Gnome Shell version 
		if(isfile('/usr/share/gnome/gnome-version.xml')):
			xmldoc 	= minidom.parse('/usr/share/gnome/gnome-version.xml')
			platform= xmldoc.getElementsByTagName('platform')
			minor	= xmldoc.getElementsByTagName('minor')
			micro	= xmldoc.getElementsByTagName('micro')
			if(len(platform) > 0 and len(minor) > 0 and len(micro) > 0):
				# check if Gnome shell is installed
				if(platform[0].firstChild.nodeValue != "3"):
					error("Error: Current installed Gnome version is not 3!")
				Config.gnomeVersion = str(platform[0].firstChild.nodeValue)+"."+str(minor[0].firstChild.nodeValue)+"."+str(micro[0].firstChild.nodeValue)
		else:
			error("Error: Could not find Gnome Shell version!") 

	def print_help(self):
		print "Usage: \tshell-extension-manager <command> [<args>]"
		print "\t[-h|--help] [-q|--quiet] [-y|--yes] [-a|--all] [-l|--list]\n"
		print "shell-extension-manager is a command line interface for managing Gnome Shell Extensions."
		print "Run shell-extension-manager with root privilege for system wide actions.\n"
		print "Commands:"
		print "   install\tInstall extension(s) by extension name."
		print "   remove\tRemove extension(s) by extension name"
		print "   update\tUpdate all extensions"
		print "   update-index\tUpdate the index with all available extensions"
		print "   enable\tEnable extension by name"
		print "   disable\tDisable extenion by name"
		print "   show \tShow installed extensions"
		print "   create\tCreate extension install script\n"
		print "Options:"
		print "  -h --help\tThis help text"
		print "  -q --quiet\tNo output except for errors"
		print "  -y --yes\tAssume Yes to all queries and do not prompt"
		print "  -a --active\tOnly show enabled extensions with show command"
		print "  -l --list\tDetailed list of extensions with show command"

	def install(self, args):
		if(Config.user == 'root'):
			display("Installing extensions system wide")
		else:
			display("Installing extensions for user "+Config.user)
		manager = ExtensionManager()
		manager.install(args)

	def remove(self, args):
		if(Config.user == 'root'):
			display("Remove extensions system wide")
		else:
			display("Remove extensions for user "+Config.user)
		manager = ExtensionManager()
		manager.remove(args)

	def update(self, args):
		if(Config.user == 'root'):
			display("Update extensions system wide")
		else:
			display("Update extensions for user "+Config.user)
		manager = ExtensionManager()
		manager.update()

	def updateIndex(self):
		index = ExtensionIndex()
		index.updateIndex()

	def enable(self, args):
		if len(args) < 1: 
			display("no extension given")
			return
		manager = ExtensionManager()
		manager.enable(args[0])

	def disable(self, args):
		if len(args) < 1: 
			display("no extension given")
			return
		manager = ExtensionManager()
		manager.disable(args[0])

	def show(self, args):
		show = ExtensionShow()
		show.show(Config.optList, Config.optActive)

	def create(self, args):
		print "Not implemented yet"