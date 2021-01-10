import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gdk, Gtk, Pango
from .lcd_driver import LCDDriver

class LCDPanel(Gtk.TextView):
    DEFAULT_FONT = "DS-DIGITAL BOLD 28"

    def __init__(self, namespace={}):
        Gtk.TextView.__init__(self)
        self._driver = LCDDriver(4)

        self.set_margin_top(10)
        self.set_hexpand(False)
        self.set_hexpand(False)
        self.set_buffer(self._driver.get_buffer())
        self.set_size_request(400, 240)
        font_desc = Pango.FontDescription(LCDPanel.DEFAULT_FONT)
        # layout = self.get_widget_layout()
        # font_attr = Pango.attr_letter_spacing_new(letter_spacing=8)
        # layout.set_spacing(10)
        # print(dir(layout))
        self.modify_font(font_desc)
        # self.set_justify(Gtk.Justification.LEFT)


