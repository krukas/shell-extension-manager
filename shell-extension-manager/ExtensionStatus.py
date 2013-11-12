from Utils 		import *
from gi.repository import Gio,GLib

class ExtensionStatus:
	def enable(self, name):
		print "enable"

	def disable(self, name):
		print "disable"

	def enableExtension(self, uuid):
		gsettings = Gio.Settings.new("org.gnome.shell")
		value = gsettings.get_value('enabled-extensions').unpack()
		if(not uuid in value):
			value.append(uuid)
			gsettings.set_value('enabled-extensions', GLib.Variant('as', value))

	def disableExtension(self, uuid):
		print "disable"