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
# hexcalculator


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Peas,GObject

from .hex_calculator import HexCalculator

class HexCalculatorPlugin(GObject.Object, Peas.Activatable):
 
    object = GObject.Property(type=GObject.Object)

    def __init__(self):
        GObject.Object.__init__(self)
        
    def do_activate(self):
        window = self.object
        
        self.hex_calculator = HexCalculator()
        self.frame = Gtk.Frame(label="Hex Calculator")
        self.frame.add(self.hex_calculator)
        window.attach(self.frame, 0,1,1,1)
        self.frame.show_all()

    def do_deactivate(self):
        window = self.object
        window.remove(self.frame)



