#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Disk Manager gtk Windows Module

BaseWindow - Base Window for disk manager gtk
MainWindow - Standalone Window for disk manager gtk

"""

from disk_manager_gtk.translation import _
from disk_manager_gtk.widgets import DiskItem

import gobject
import gtk

class BaseWindow(gtk.Window):
    """Base Window for disk manager gtk"""
    def __init__(self):
        """init"""
        gtk.Window.__init__(self)
        self._set_style()
        self._create_ui()
        self._listen_signals()
    def _set_style(self):
        """sets title and default size etc."""
        pass
    def _create_ui(self):
        """creates ui elements"""
        pass
    def _listen_signals(self):
        """listens signals"""
        pass

gobject.type_register(BaseWindow)

class MainWindow(BaseWindow):
    """Standalone Window for disk manager gtk"""

    def __init__(self, iface):
        """init
        
        Arguments:
        - `iface`: comar interface
        """
        BaseWindow.__init__(self)
        self.iface = iface
    def _set_style(self):
        self.set_title(_("Disk Manager"))
        self.set_default_size(483, 300)
    def _create_ui(self):
        self._container = gtk.ScrolledWindow()
        self._container.set_shadow_type(gtk.SHADOW_IN)
        self._container.set_policy(gtk.POLICY_NEVER,
                                   gtk.POLICY_AUTOMATIC)
        self.add(self._container)
        self.vbox = gtk.VBox(spacing=5)
        self._container.add_with_viewport(self.vbox)
        for i in range(3):
            self.vbox.pack_start(DiskItem("dummy"),
                                 expand=False)
    def _listen_signals(self):
        self.connect("destroy", gtk.main_quit)

gobject.type_register(MainWindow)
