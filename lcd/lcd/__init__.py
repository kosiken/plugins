# gtkemu8086
# Copyright 2020 KRC
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# lcdplugin
# LcdPlugin class
#


from .lcd_panel import LCDPanel
from gi.repository import GObject, Gtk, Peas, PeasGtk 


class LcdPlugin(GObject.Object, Peas.Activatable):
    """
    LcdPlugin 
    """

    object = GObject.Property(type=GObject.Object)

    def __init__(self):
        GObject.Object.__init__(self)

    def do_activate(self):
        window = self.object
        print("added")
        self.panel = LCDPanel()
        self.panel2 = LCDPanel()

        self.box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 10)
        self.box.set_margin_start(10)
        self.box.set_margin_end(10)

        self.panel2.add_text("")
        self.panel.add_text("")
        self.box.add(self.panel)
        self.box.add(self.panel2)
        self.box.show_all()
        window.add(self.box)
        win = window.get_property("runner")
        win.connect("interrupt", self.__mycb)
        win.connect("exec_stopped", self.__clear_lcd)

    def __mycb(self, runner, n):
        s = str(n)
        m = s.upper()
        self.panel.add_text(m)
        # self.panel2.add_text(m)

    def __clear_lcd(self, runner):
        """
        clears the lcd
        """
        self.panel2.clear_text()
        self.panel.clear_text()

    def do_deactivate(self):
        window = self.object
        self.box.remove(self.panel)
        self.box.remove(self.panel2)

        # print(dir(window))
        window.remove(self.box)
