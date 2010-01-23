# -*- coding: utf-8 -*-
"""includes disk_manager_gtk's widgets

DiskItem - disk item container

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

import gtk
import gobject

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
    def set_mode(self, mode, mount_path=""):
        """sets mounted True or False
        
        Arguments:
        - `mode`: True | False
        - `mount_path`: ex: /media/xxx 
        """
        if mode:
            self._mount = mount_path
        else:
            self._mount = None
        self._set_mounted()
    def listen_signals(self, func):
        """listen signals 
        
        Arguments:
        - `func`: callback function
        """
        self.check_btn.connect("clicked", func,
                               {"action":"toggle",
                                "name":self._name,
                                "mount":self._mount,
                                "widget":self})
        self.edit_btn.connect("clicked", func,
                              {"action":"edit",
                               "name":self._name,
                               "mount":self._mount,
                               "widget":self})
