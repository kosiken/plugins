


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Peas,GObject
from .lcd_view import LCDWidget
from .lcd_pattern_generator import PatternGenerator
from .lcd_driver import LCDDriver
from .lcd_cell import LCDCell

class LcdHitachiPlugin(GObject.Object, Peas.Activatable):
 
    object = GObject.Property(type=GObject.Object)

    def __init__(self):
        GObject.Object.__init__(self)
        
    def do_activate(self):
        window = self.object.get_property("v_box")
        print(repr(window))
        self.panel = LCDWidget()
        self._driver  = LCDDriver(self.panel)
        self.frame = self.panel.get_me()
        self.frame.show_all()
        self.box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 10)
        self.button_box = Gtk.ButtonBox.new(Gtk.Orientation.HORIZONTAL)
        button = Gtk.Button.new_with_label(label="Clear LCD")
        button2 = Gtk.Button.new_with_label(label="Scroll Left")
        button3 = Gtk.Button.new_with_label(label="Scroll Right")    
        self.buttons = [button2, button,button3]    
        for btn in self.buttons:
            self.button_box.add(btn)
            pass

        self.box.add(self.frame)
        self.box.add(self.button_box)
        self.box.show_all()
        window.add(self.box)
        win = self.object.get_property("runner")
        button.connect("clicked", self.cls)
        win.connect("interrupt", self.__mycb)


    def __mycb(self, runner, n):
        cmd = int(n)
        # panel = self.panel
        # panel._driver.recieve4(cmd)
        self._driver.recieve(cmd, 0)
        pass

    def cls(self, box):
        print('ll',repr(box))
        self._driver.cld()
        pass

    def do_deactivate(self):
        self._driver.clear_out(self.panel)
        self.panel.deactivate()
        for btn in self.buttons:
            self.button_box.remove(btn)
        window = self.object.get_property("v_box")
        self.box.remove(self.frame)
        window.remove(self.box)
