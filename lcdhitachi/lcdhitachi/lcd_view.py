import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gdk, Gtk, Pango

class LCDWidget(Gtk.Grid):
    def __init__(self):
        """
        docstring
        """
        Gtk.Grid.__init__(self)
        self.buffer = ""
        self.buffer2 = ""
        self.data_reg = 0
        self.mem = tuple(get_empty_array())
        pass



def get_empty_array():
    l = [0 for i in range(0,32)]
    return l

