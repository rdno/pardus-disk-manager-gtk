#!/usr/bin/python
# -*- coding: utf-8 -*-
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

import pygtk
pygtk.require("2.0")
import gtk

from disk_manager_gtk.translation import _
from disk_manager_gtk import DiskManager

class MainWindow(gtk.Window):
    """Standalone Window for disk manager gtk"""
    def __init__(self):
        """init"""
        gtk.Window.__init__(self)
        self.manager = DiskManager()
        self._set_style()
        self._create_ui()
        self._listen_signals()
    def _set_style(self):
        self.set_title(_("Disk Manager"))
        self.set_default_size(483, 300)
    def _create_ui(self):
        self.add(self.manager)
    def _listen_signals(self):
        self.connect("destroy", gtk.main_quit)
    def run(self, arg):
        """run app
        
        Arguments:
        - `arg`: sys.argv
        """
        self.show_all()
        gtk.main()
    

if __name__ == '__main__':
    import sys
    MainWindow().run(sys.argv)
