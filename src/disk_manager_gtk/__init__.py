# -*- coding: utf-8 -*-
"""Disk Manager gtk Main Module

DiskManager - Main widget of disk manager gtk

"""
#
# Rıdvan Örsvuran (C) 2010
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

__all__ = ["translation", "widgets", "windows", "backend",
           "DiskManager"]

import gtk
import gobject

from dbus.mainloop.glib import DBusGMainLoop

from disk_manager_gtk.backend import Interface
from disk_manager_gtk.translation import _
from disk_manager_gtk.widgets import DiskItem
from disk_manager_gtk.windows import EditWindow
from disk_manager_gtk.utils import get_disks


class DiskManager(gtk.ScrolledWindow):
    """Main widget of disk manager gtk"""
    def __init__(self):
        """init"""
        gtk.ScrolledWindow.__init__(self)
        self._dbus_loop()
        self._vbox = gtk.VBox(spacing=5)
        self.iface = Interface()
        self.iface.listenSignals(self.listen_comar)
        self._set_style()
        self._create_ui()
    def _dbus_loop(self):
        #runs dbus main loop
        DBusGMainLoop(set_as_default = True)
    def _set_style(self):
        self.set_shadow_type(gtk.SHADOW_IN)
        self.set_policy(gtk.POLICY_NEVER,
                        gtk.POLICY_AUTOMATIC)
    def _create_ui(self):
        #creates ui
        self.add_with_viewport(self._vbox)
        self.items = get_disks(self.iface)
        for i in self.items.keys():
            item = DiskItem(i, self.items[i]["mount"])
            item.listen_signals(self.on_disk_item)
            self._add_item(item)
    def _add_item(self, item):
        #adds item to vbox
        self._vbox.pack_start(item, expand=False)
    def on_disk_item(self, widget, data):
        action = data["action"]
        if action == "toggle":
            if data["mount"] is not None:
                self._try_to("umount", data)
            else:
                if data["name"] in self.iface.entryList():
                    path = self.iface.getEntry(data["name"])[0]
                    self._try_to("mount", data, path)
                else:
                    self.open_edit_window(data["name"], None)
        elif action == "edit":
            short = self.items[data["name"]]["entry"]
            entry = None
            if not short  == None:
                entry = self.iface.getEntry(short)
            self.open_edit_window(data["name"], entry)
    def open_edit_window(self, device, entry):
        """opens EditWindow"""
        w = EditWindow(device, entry)
        w.on_save(self.on_options_save)
        w.show()
    def on_options_save(self, widget, data):
        data["entry"] = data["get_entry"]()
        data["quit"]()
        if not data["entry"] == "same": # if same, do nothing
            if data["entry"] == None:
                self._try_to("removeEntry", data)
            else:
                self._try_to("addEntry",  data)
    def _try_to(self, func, data, path=""):
        #try to (mount | umount | removeEntry | addEntry)
        try:
            if func == "mount":
                self.iface.mount(data["name"], path)
            elif func == "umount":
                self.iface.umount(data["name"])
            elif func == "removeEntry":
                self.iface.removeEntry(data["device"])
            elif func == "addEntry":
                self.iface.addEntry(data["device"],
                                    data["entry"][0],
                                    data["entry"][1],
                                    data["entry"][2])
            #widget.set_mode(func == "mount", path)
        except Exception, e:
            if "Comar.PolicyKit" in e._dbus_error_name:
                self.open_error_dialog(_("Access Denied"))
            else:
                self.open_error_dialog(unicode(e))
            if (func == "mount") | (func == "umount"):
                widget = data["widget"]
                widget.set_mode(not func == "mount")
    def open_error_dialog(self, text):
        dialog = gtk.MessageDialog(type=gtk.MESSAGE_ERROR,
                                   buttons=gtk.BUTTONS_OK,
                                   message_format=text)
        dialog.run()
        dialog.destroy()
    def listen_comar(self, package, signal, args):
        """listen comar signals

        Arguments:
        - `package`: ex : mudur
        - `signal` : ex: changed
        - `args`: extra arguments
        """
        print ">", package, signal, args

gobject.type_register(DiskManager)

