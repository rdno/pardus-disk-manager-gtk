# -*- coding: utf-8 -*-
"""includes disk_manager_gtk's windows

EditWindow - Edit fstab preferences

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

import gobject
import gtk

from disk_manager_gtk.translation import _
from disk_manager_gtk.utils import FS_TYPES, FS_OPTIONS
from disk_manager_gtk.utils import cbox_set_active_value
from disk_manager_gtk.utils import cbox_get_active_value

class EditWindow(gtk.Window):
    """Edit fstab preferences"""
    def __init__(self, device, entry, auto=True):
        """init

        Arguments:
        - `device`: ex: /dev/sda1
        - `entry`: entry object
           ex: (u'/', u'ext4', u'defaults,noatime,user_xattr')
        - `auto`: auto mount
        """
        gtk.Window.__init__(self)
        self._entry = entry
        self._device = device
        self._auto = auto
        self._set_style()
        self._create_ui()
        self._listen_signals()
    def _create_ui(self):
        self._frame = gtk.Frame()
        self._frame.set_label(_("Settings"))

        vbox = gtk.VBox(homogeneous=False,
                        spacing = 5)
        self._frame.add(vbox)

        self._auto_cb = gtk.CheckButton(_("Mount Disk Automatically"))
        vbox.pack_start(self._auto_cb, expand=False)
        self._table = gtk.Table(rows=4, columns = 3)
        vbox.add(self._table)

        self._mp_lb = gtk.Label(_("Mount Point:"))
        self._fs_lb = gtk.Label(_("File System:"))
        self._op_lb = gtk.Label(_("Options:"))
        self._mp_txt = gtk.Entry()
        self._prepare_fs_box()
        self._op_txt = gtk.Entry()
        self._def_op_btn = gtk.Button(_("Default Options"))
        self._ok_btn = gtk.Button(_("OK"))
        self._ca_btn = gtk.Button(_("Cancel"))
        #TODO: add buttons to ui (vbox)
        self._add_all_to_table()
        self._table.show_all()

        hbox = gtk.HBox(homogeneous=False,
                        spacing=5)
        hbox.pack_end(self._ok_btn, expand=False)
        hbox.pack_end(self._ca_btn, expand=False)
        vbox.pack_end(hbox, expand=False)
        self.add(self._frame)
        self._frame.show_all()
        self._fill_ui()
    def _set_style(self):
        self.set_modal(True)
        self.set_title(_("Edit Settings"))
        self.set_default_size(480, 190)
    def _add_all_to_table(self):
        #adds widgets to _table
        self._table.set_row_spacings(5)
        self._table.set_col_spacings(5)
        self._table.attach(self._mp_lb, 0, 1, 0, 1,
                           gtk.SHRINK, gtk.SHRINK)
        self._table.attach(self._mp_txt, 1, 2, 0, 1,
                           gtk.EXPAND|gtk.FILL, gtk.SHRINK)
        self._table.attach(self._fs_lb, 0, 1, 1, 2,
                           gtk.SHRINK, gtk.SHRINK)
        self._table.attach(self._fs_box, 1, 2, 1, 2,
                           gtk.EXPAND|gtk.FILL, gtk.SHRINK)
        self._table.attach(self._op_lb, 0, 1, 2, 3,
                           gtk.SHRINK, gtk.SHRINK)
        self._table.attach(self._op_txt, 1, 2, 2, 3,
                           gtk.EXPAND|gtk.FILL, gtk.SHRINK)
        self._table.attach(self._def_op_btn, 2, 3, 2, 3,
                           gtk.SHRINK, gtk.SHRINK)
    def _fill_ui(self):
        #fill ui with entry
        if not self._entry == None:
            self._mp_txt.set_text(self._entry[0])
            cbox_set_active_value(self._fs_box, self._entry[1])
            self._op_txt.set_text(self._entry[2])
        self._auto_cb.set_active(self._auto)
        self._on_auto_cb(self._auto_cb)
    def _prepare_fs_box(self):
        model = gtk.ListStore(str, str)
        cell = gtk.CellRendererText()
        self._fs_box = gtk.ComboBox(model)
        self._fs_box.pack_start(cell, True)
        self._fs_box.add_attribute(cell, 'text', 0)
        for i in FS_TYPES.keys():
            model.append([FS_TYPES[i], i])
    def _listen_signals(self):
        #listen private signals
        self._auto_cb.connect("clicked", self._on_auto_cb)
        self._ca_btn.connect("clicked", self.quit)
        self._def_op_btn.connect("clicked", self.write_default)
    def write_default(self, widget):
        val = cbox_get_active_value(self._fs_box)
        self._op_txt.set_text(FS_OPTIONS[val])
    def quit(self, widget=None):
        """close window"""
        self.destroy()
    def _on_auto_cb(self, widget):
        self._table.set_sensitive(widget.get_active())
    def on_save(self, func):
        """on ok button clicked

        Arguments:
        - `func`: callback function
        """
        self._ok_btn.connect("clicked", func,
                             {"device":self._device,
                              "get_entry":self.get_data,
                              "quit":self.quit})
    def get_data(self):
        """gets data from ui"""
        if self._auto_cb.get_active():
            r = (unicode(self._mp_txt.get_text()),
                 unicode(cbox_get_active_value(self._fs_box)),
                 unicode(self._op_txt.get_text()))
            if self._entry == r:
                return "same" #if same , do nothing
            return r
        return None

gobject.type_register(EditWindow)

