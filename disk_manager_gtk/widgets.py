#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Disk Manager gtk widgets module

DiskItem - disk item container
"""

from disk_manager_gtk.translation import _

import gtk
import gobject

class DiskItem(gtk.Table):
    """disk item container"""

    def __init__(self, props):
        """init
        
        Arguments:
        - `props`: properties
        """
        gtk.Table.__init__(self, rows=2, columns=4)
        self._props = props
        self._create_ui()
    def _create_ui(self):
        # creates ui
        self.check_btn = gtk.CheckButton()

        self._name = gtk.Label("Lorem Ipsum")
        self._name.set_alignment(0.0, 0.5)
        
        self._info = gtk.Label("dolor sit amet")
        self._info.set_alignment(0.0, 0.5)

        self.edit_btn = gtk.Button(_("Edit"))

        self.attach(self.check_btn, 0, 1, 0, 2,
                    gtk.SHRINK, gtk.SHRINK)
        #TODO:self.attach(icon goes here, 1, 2, 0, 2,
        #           gtk.SHRINK, gtk.SHRINK)
        self.attach(self._name, 2, 3, 0, 1,
                    gtk.EXPAND|gtk.FILL, gtk.SHRINK)
        self.attach(self._info, 2, 3, 1, 2,
                    gtk.EXPAND|gtk.FILL, gtk.SHRINK)
        self.attach(self.edit_btn, 3, 4, 0, 2,
                    gtk.SHRINK, gtk.SHRINK)
