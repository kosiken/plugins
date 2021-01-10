from gi.repository import GObject, Gdk, Gtk, Pango


class LCDPanel(Gtk.Label):

    DEFAULT_FONT = "DS-DIGITAL BOLD 28"

    def __init__(self, namespace={}):
        Gtk.Label.__init__(self)
        self.buffer = ""
        self.count = 0
        self.set_text(self.buffer)
        font_desc = Pango.FontDescription(LCDPanel.DEFAULT_FONT)
        layout = self.get_layout()
        # font_attr = Pango.attr_letter_spacing_new(letter_spacing=8)
        layout.set_spacing(10)
        # print(dir(layout))
        self.modify_font(font_desc)
        self.set_justify(Gtk.Justification.LEFT)

    def add_text(self, text):
        self.buffer = self.buffer + text
        self.count = self.count + 1
        count = 0
        if(self.count > 16):
            count = self.count - 16
            print("%d" % count)
        self.set_text(self.buffer[count:])

    def clear_text(self):
        self.buffer = ""
        self.count = 0
        self.set_text(self.buffer)
