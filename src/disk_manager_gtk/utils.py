# -*- coding: utf-8 -*-
"""Some useful variables anfd functions
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

import subprocess

import gtk
import gobject

FS_TYPES = {
    "ext2": "Extended 2",
    "ext3": "Extended 3",
    "ext4": "Extended 4",
    "reiserfs": "Reiser FS",
    "xfs": "XFS",
    "ntfs-3g": "NTFS",
    "vfat": "Fat 16/32",
    "swap": "swap",
}

FS_OPTIONS = {
    "vfat": "quiet,shortname=mixed,dmask=007,fmask=117,utf8,gid=6",
    "ext2": "noatime",
    "ext3": "noatime",
    "ext4": "noatime",
    "ntfs-3g": "dmask=007,fmask=117,locale=tr_TR.UTF-8,gid=6",
    "reiserfs": "noatime",
    "xfs": "noatime",
    "swap": "sw, defaults",
}

def cbox_set_active_value(combobox, value):
    """sets value's index active
    model like [user_text, value]
    Arguments:
    - `combobox`: gtk.ComboBox
    - `value`: value to select
    """
    model = combobox.get_model()
    for i, row in enumerate(model):
        if row[1] == value:
            combobox.set_active(i)
def cbox_get_active_value(combobox):
    """gets active value from combobox
    model like [user_text, value]
    Arguments:
    - `combobox`: gtk.ComboBox
    """
    model = combobox.get_model()
    active = combobox.get_active()
    if active < 0:
        return None
    return model[active][1]

def get_disks(iface):
    """returns disk dict like:
    {
      {'/dev/xxx':{mount:'/', entry:/dev/xxx}},
      {'/dev/xxy':{mount:'/media/xxy', entry:None}},
      {'/dev/xyy':{mount:None entry:None}}
    }

    Arguments:
    - `iface`: Interface()
    """
    disks = {}

    def set_disk(disk, mount=None, entry=None):
        if not disk in disks:
            disks[disk] = {"mount":None, "entry":None}
        if mount:
            disks[disk]["mount"] = mount
        if entry:
            disks[disk]["entry"] = entry

    for device in iface.deviceList():
        for part in iface.partitionList(device):
            set_disk(part)
    for entry in iface.entryList():
        if entry.startswith("/dev"):
            set_disk(entry, entry=entry)
        elif entry.startswith("LABEL="):
            set_disk(iface.getDeviceByLabel(entry.split("=")[1]),
                     entry=entry)
    for device, path in iface.mountList():
        set_disk(device,
                 mount=path)

    return disks

def get_icon(name, size=32, flags=0):
    """gets icon from gtk.IconTheme return Pixbuf

    Arguments:
    - `name`: icon name
    - `size`: icon size
    - `flags`: the flags modifying the behavior of the icon lookup
    """
    it = gtk.icon_theme_get_for_screen(gtk.gdk.Screen())
    try:
        return it.load_icon(name, size, flags)
    except gobject.GError, e:
        open_error_dialog(unicode(e))

def open_error_dialog(text):
    """opens a gtk error dialog"""
    dialog = gtk.MessageDialog(type=gtk.MESSAGE_ERROR,
                               buttons=gtk.BUTTONS_OK,
                               message_format=text)
    dialog.run()
    dialog.destroy()

def getFSType(device):
    cmd = "/sbin/blkid -s TYPE -o value %s" % device
    proc = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    return proc.communicate()[0].strip()
def get_default_entry(device):
    fs_type = getFSType(device)
    return ('', fs_type, FS_OPTIONS[fs_type])
