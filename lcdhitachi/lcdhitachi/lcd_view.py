#
# Copyright 2020 KRC
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#  this list of conditions and the following disclaimer in the documentation
#  and/or other materials provided with the distribution.
#
#
# lcd_view.py



import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Peas,GObject
from .lcd_driver import LCDDriver
class LCDWidget(Gtk.Grid):
 

 
    def __init__(self):
        """
        docstring
        """
        Gtk.Grid.__init__(self)

        self.set_row_spacing(4)

        self.set_column_spacing(4)
        
        self.frame = Gtk.Frame(label="LCD")
        self.box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 10)
        self.box.set_margin_start(10)
        self.box.set_margin_end(10)
        self.box.add(self)
        self.frame.add(self.box)
        self.show_all()
        self.box.show_all()
        
        pass

    def get_me(self):
        """
        docstring
        """
        return self.frame


    def deactivate(self):

        self.box.remove(self)
        self.frame.remove(self.box)

