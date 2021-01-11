import gi
gi.require_version('Gtk', '3.0')
from gi.repository import  Gtk, Gdk

from lcdhitachi import PatternGenerator

class LCDCell(Gtk.Widget):
    def __init__(self, *args, **kwds):
        """
        docstring
        """
        super().__init__( *args, **kwds)   
        self.has_cursor = False
        self.cursor_blink = False
        self._is_active = False
        self._inactive_color =Gdk.RGBA(red=.92,green=.92,blue=.92,alpha=1) 
        self._active_color =Gdk.RGBA(red=0,green=0,blue=0,alpha=0) 
        self.off_color = Gdk.RGBA(red=0.77,green=0.77,blue=0.77,alpha=0) 
        self._value = 93
        pass



    def do_draw(self, cr):
        """
        docstring
        """
        bg_color = self._inactive_color
        if(self._is_active):
            bg_color = self._active_color
            pass

        pass
    

