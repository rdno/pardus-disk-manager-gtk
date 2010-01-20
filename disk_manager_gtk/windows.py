#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Disk Manager gtk Windows Module

BaseWindow - Base Window for disk manager gtk
MainWindow - Standalone Window for disk manager gtk

"""

from disk_manager_gtk.translation import _
from disk_manager_gtk.widgets import MainWidget

import gobject
import gtk

class MainWindow(gtk.Window):
    """Standalone Window for disk manager gtk"""
    def __init__(self):
        """init"""
        gtk.Window.__init__(self)
        self.container = MainWidget()
        self._set_style()
        self._create_ui()
        self._listen_signals()
    def _set_style(self):
        self.set_title(_("Disk Manager"))
        self.set_default_size(483, 300)
    def _create_ui(self):
        self.add(self.container)
    def _listen_signals(self):
        self.connect("destroy", gtk.main_quit)

gobject.type_register(MainWindow)
