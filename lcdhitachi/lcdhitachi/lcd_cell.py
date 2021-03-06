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
# lcd_cell.py




import gi

gi.require_version('Gtk', '3.0')

from .lcd_pattern_generator import PatternGenerator
from gi.repository import GLib, Gtk, Gdk



class LCDCell(Gtk.Image):
    #  We inherit image because the bare GtkBin
    # was proving to be a pain in the keyboard
    """
    Renders a single lcd cell

    """
    HEIGHT = (5*8) + 2
    WIDTH = (5*5) + 2

    def __init__(self, *args, **kwds):
        """
        init
        """

        super().__init__(*args, **kwds)
        

        self.has_cursor = False # Whether to show cursor

        self.cursor_blink = False # Whether to blink cursor 
        self._is_active = False
        self._blink_on = False
        self._font = 0
        self.index = 0
        self._matrix = []
        # self.set_vexpand(False)
        # self.set_hexpand(False)
        self._inactive_color = Gdk.RGBA(red=.60, green=.60, blue=.60, alpha=1)
        self._active_color = Gdk.RGBA(red=0, green=0, blue=0, alpha=1)
        self._off_color = Gdk.RGBA(red=0.65, green=0.65, blue=0.65, alpha=1)
        self._cursor_color = Gdk.RGBA(red=0.0, green=0, blue=0.77, alpha=1)
        self._value =  32
        self.set_size_request(LCDCell.WIDTH, LCDCell.HEIGHT)

        pass

    def do_get_preferred_size(self, requisition):

        requisition.width = LCDCell.WIDTH
        requisition.height = LCDCell.HEIGHT

    def do_size_allocate(self, a):
        """
        docstring
        """
        a.width = LCDCell.WIDTH
        a.height = LCDCell.HEIGHT
        self.set_allocation(a)
        pass

    def set_value(self, value=93):

        self._value = value
        self.queue_draw()

    def cmp_and_set_val(self, value) -> bool:
        v = value
        prev = self._matrix
        force=False
        if(len(prev)> 1):
            self._matrix =[]
            force = True
            


        self._matrix =[]
        if(value == 0):
            v = 93 + 32
        if(self._value == v and not force):
            return False
        self.set_value(v)
        return True

    def do_draw(self, cr):
        """
        docstring
        """
        bg_color = self._inactive_color
        if(self._is_active):
            bg_color = self._off_color
            pass
        # # print('lol')
        cr.set_source_rgba(*list(bg_color))
        cr.paint()
        if(not self._is_active):
            return
        # m_len = len(matrix)
        matrix = self._matrix
        if(len(matrix)>0):
            matrix = PatternGenerator.render_from_data(matrix)
        
        else:
            matrix =  PatternGenerator.render_pattern_to_matrix(self._value - 32)

        
        m_len = len(matrix)
        for i in range(0, m_len):
            b = len(matrix[i])
            for j in range(0, b):

                # cr.move_to(0, 0)

                if(matrix[i][j] == 1):

                    cr.set_source_rgba(*list(self._active_color))
                    pass
                else:

                    cr.set_source_rgba(*list(self._off_color))
                    pass
                cr.rectangle(j * 5, ((i+self._font)*5)+1, 5, 5)
                cr.fill()
                pass
            pass
        blink_color = self._cursor_color

        if(self.cursor_blink and self.has_cursor):

            if(not self._blink_on):
                blink_color = self._off_color
            # # print("ll")

            cr.set_source_rgba(*list(blink_color))
            cr.rectangle(0, (1+(7+self._font)*5)+1,
                         LCDCell.WIDTH, 5)
            cr.fill()

        elif (self.has_cursor):
            # for j in range(0,5):

            cr.set_source_rgba(*list(blink_color))
            cr.rectangle(0, (1+(7+self._font)*5)+1,
                         LCDCell.WIDTH, 5)
            cr.fill()
            # pass

        # allocation = self.get_allocation()

        pass

    def set_active(self, active=True):
        """
        docstring
        """
        self._is_active = active
        # print("cell %d active"%self.index)
        pass

    def set_cursor(self, has_cursor=True, blink=False):

        self.has_cursor = has_cursor
        # print("cell, ", self.index,has_cursor, blink)
        # print("ionic")
        if(blink == self.cursor_blink):
            return
        elif (not blink):

            self.cursor_blink = blink
            # GObject.Souce.remove(self.to)
            return
        else:

            # return
            self.cursor_blink = blink

            self.to = GLib.timeout_add(500, self.toggle_blink)

        pass

    def toggle_blink(self):
        self._blink_on = not self._blink_on

        self.queue_draw()
        return (self.cursor_blink and self.has_cursor)
    def set_matrix(self, arr):
        """
        docstring
        """
        self._matrix = arr
        pass

