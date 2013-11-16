from Utils 		import *
from gi.repository import Gio,GLib

class ExtensionStatus:

	def enableExtension(self, uuid):
		gsettings = Gio.Settings.new("org.gnome.shell")
		value = gsettings.get_value('enabled-extensions').unpack()
		if(not uuid in value):
			value.append(uuid)
			gsettings.set_value('enabled-extensions', GLib.Variant('as', value))
			return True
		return False

	def disableExtension(self, uuid):
		gsettings = Gio.Settings.new("org.gnome.shell")
		value = gsettings.get_value('enabled-extensions').unpack()
		if(uuid in value):
			value.remove(uuid)
			gsettings.set_value('enabled-extensions', GLib.Variant('as', value))
			return True
		return False

	def activeExtensions(self):
		gsettings = Gio.Settings.new("org.gnome.shell")
		return gsettings.get_value('enabled-extensions').unpack()