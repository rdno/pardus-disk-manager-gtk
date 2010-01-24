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
from asma.addon import AsmaAddon
from disk_manager_gtk import DiskManager
from disk_manager_gtk.translation import _
class DiskManagerAddon(AsmaAddon):
    """Disk Manager Asma addon"""
    def __init__(self):
        """init the variables"""
        super(DiskManagerAddon, self).__init__()
        self._uuid = "9aaeab69-8fad-458f-878a-09277be0a6ec"
        self._icon_name = "drive-harddisk"
        self._label = _("Disk Manager")
        self._widget = DiskManager
