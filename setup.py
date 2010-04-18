#!/usr/bin/python
# -*- coding: utf-8 -*-
from setuptools import setup

data_files = [
    ("share/applications", ["data/disk-manager-gtk.desktop"])
]

setup(name="pardus-disk-manager-gtk",
      version="0.2",
      package_dir={"":"src"},
      packages = ["disk_manager_gtk", "asma.addons"],
      scripts = ["src/disk-manager-gtk.py"],
      description= "Pardus Disk Manager's gtk port",
      author="Rıdvan Örsvuran",
      author_email="flasherdn@gmail.com",
      data_files=data_files
)
