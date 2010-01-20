#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygtk
pygtk.require("2.0")
import gtk

from disk_manager_gtk.windows import MainWindow

if __name__ == '__main__':
    MainWindow().show_all()
    gtk.main()
