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
        
    # def do_activate(self):
    #     window = self.object

    #     window.add(self.frame)
    #     win = window.get_property("runner")
    #     win.connect("interrupt", self.__mycb)


    # def __mycb(self, runner, n):
    #     cmd = int(n)
    #     # panel = self.panel
    #     # panel._driver.recieve4(cmd)
    #     # print("%x"%cmd)
    #     pass
    def deactivate(self):
        # self._driver.clear_out(self)
        self.box.remove(self)
        self.frame.remove(self.box)
        # window = self.object#   
        # window.remove(self.frame) #      m = s.upp l
