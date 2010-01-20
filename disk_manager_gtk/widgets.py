#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Disk Manager gtk widgets module

DiskItem - disk item container
"""

import gtk
import gobject

from dbus.mainloop.glib import DBusGMainLoop

from disk_manager_gtk.backend import Interface
from disk_manager_gtk.translation import _

class DiskItem(gtk.Table):
    """disk item container"""

    def __init__(self, name, mount):
        """init
        
        Arguments:
        - `name` : ex: /dev/xxx
        - `mount`: mount point
        """
        gtk.Table.__init__(self, rows=2, columns=4)
        self._name = name
        self._mount = mount
        self._create_ui()
    def _create_ui(self):
        # creates ui
        self.check_btn = gtk.CheckButton()

        self._name_lb = gtk.Label()
        self._name_lb.set_alignment(0.0, 0.5)
        self._name_lb.set_markup("<b>"+self._name+"</b>")
        
        self._info = gtk.Label()
        self._info.set_alignment(0.0, 0.5)

        self._set_mounted()

        self.edit_btn = gtk.Button(_("Edit"))

        self.attach(self.check_btn, 0, 1, 0, 2,

                    gtk.SHRINK, gtk.SHRINK)
        #TODO:self.attach(icon goes here, 1, 2, 0, 2,
        #           gtk.SHRINK, gtk.SHRINK)
        self.attach(self._name_lb, 2, 3, 0, 1,
                    gtk.EXPAND|gtk.FILL, gtk.SHRINK)
        self.attach(self._info, 2, 3, 1, 2,
                    gtk.EXPAND|gtk.FILL, gtk.SHRINK)
        self.attach(self.edit_btn, 3, 4, 0, 2,
                    gtk.SHRINK, gtk.SHRINK)
    def _set_mounted(self):
        if self._mount is not None:
            self._info.set_text(_("Mounted at %s") % self._mount)
            self.check_btn.set_active(True)
        else:
            self._info.set_text("")
            self.check_btn.set_active(False)
    def listen_signals(self, func):
        """listen signals 
        
        Arguments:
        - `func`: callback function
        """
        self.check_btn.connect("pressed", func,
                               {"action":"toggle",
                                "name":self._name,
                                "mount":self._mount})
        self.edit_btn.connect("clicked", func,
                              {"action":"edit",
                               "name":self._name,
                               "mount":self._mount})
    

class MainWidget(gtk.ScrolledWindow):
    """Main widgets of disk manager"""
    def __init__(self):
        """init"""
        gtk.ScrolledWindow.__init__(self)
        self._dbus_loop()
        self._vbox = gtk.VBox(spacing=5)
        self.iface = Interface()
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
        items = self._get_list()
        for i in items.keys():
            item = DiskItem(i, items[i]["mount"])
            item.listen_signals(self.on_disk_item)
            self._add_item(item)
    def _get_list(self):
        #returns disk items like:
        # {'/dev/xxx':{mount:'/', 'entry':True}}
        items = {}
        for device in self.iface.deviceList():
            for part in self.iface.partitionList(device):
                items[part] = {"mount":None, "entry":False}
        for entry in self.iface.entryList():
            if entry.startswith("/dev"):
                items[entry]["entry"] = True
            elif entry.startswith("LABEL="):
                entry = self.iface.getDeviceByLabel(entry.split("=")[1])
        for device, path  in self.iface.mountList():
            items[device]["mount"] = path
        return items
    def _add_item(self, item):
        #adds item to vbox
        self._vbox.pack_start(item, expand=False)
    def on_disk_item(self, widget, data):
        action = data["action"]
        if action == "toggle":
            if data["mount"] is not None:
                self.iface.umount(data["name"])
            else:
                if data["name"] in self.iface.entryList():
                    path = self.iface.getEntry(data["name"])[0]
                    self.iface.mount(data["name"], path)
                else:
                    print "TODO:mount device not in entry list"
        elif action == "edit":
            print "TODO:edit"

gobject.type_register(MainWidget)
