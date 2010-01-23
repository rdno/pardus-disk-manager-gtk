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




