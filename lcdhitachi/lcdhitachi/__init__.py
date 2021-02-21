


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
        window = self.object
        win = window.get_property("window")
        self.bottom_box = win.get_bottom_bar()
        self.label = Gtk.Label(label="LCD (Mode = 4; Port = 199)")
        self.label.show()
        self.bottom_box.add(self.label)
        self.panel = LCDWidget()
        self._driver  = LCDDriver(self.panel)
        self.mbox = self.panel.get_me()
        self.frame = Gtk.Expander(label="LCD")
        
        self.box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 10)
        self.button_box = Gtk.ButtonBox.new(Gtk.Orientation.HORIZONTAL)
        button = Gtk.Button.new_with_label(label="Clear LCD")
        button2 = Gtk.Button.new_with_label(label="Scroll Left")
        button3 = Gtk.Button.new_with_label(label="Scroll Right")    
        self.buttons = [button2, button,button3]    
        for btn in self.buttons:
            self.button_box.add(btn)
            pass

        self.box.add(self.mbox)
        self.box.add(self.button_box)
        
        self.box.set_margin_start(6)
        self.frame.add(self.box)
        self.frame.show_all()
        window.attach(self.frame, 0,0,1,1)
        win = self.object.get_property("runner")
        button.connect("clicked", self.cls)
        button2.connect("clicked", self.scroll_disp, -1)
        button3.connect("clicked", self.scroll_disp, 1)
        win.connect("interrupt", self.__mycb)
        # print("baseline row %d"%window.get_baseline_row())


    def __mycb(self, runner, n):
        cmd = int(n)
        # panel = self.panel
        # panel._driver.recieve4(cmd)
        self._driver.recieve(cmd, 0)
        pass

    def cls(self, box):
        # print('ll',repr(box))
        self._driver.cld()
        pass

    def do_deactivate(self):
        self._driver.clear_out(self.panel)
        self.panel.deactivate()
        for btn in self.buttons:
            self.button_box.remove(btn)
        window = self.object
        self.box.remove(self.mbox)
        window.remove(self.frame)
        self.bottom_box.remove(self.label)

    def scroll_disp(self, button, val):
        """
        docstring
        """
        self._driver.shift_disp_by_val(val)
