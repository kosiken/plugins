import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Peas,GObject

from .outline_view import OutlineView

class OutlineViewPlugin(GObject.Object, Peas.Activatable):

    object = GObject.Property(type=GObject.Object)

    def __init__(self):
        GObject.Object.__init__(self)

    def do_activate(self):
        
        window = self.object.get_property("window")
        code = window.get_code()
        grid = window.get_stack()
        self.frame =Gtk.Expander(label="Outline")
        self.g = Gtk.Grid()
        grid.attach(self.frame, 0,0,1,1)
        # print(repr(window),repr(code))
        button2 = Gtk.Button.new_with_label(label="Close")
        button2.set_relief(Gtk.ReliefStyle.NONE)
        button2.connect("clicked", self.close_cb)
        self.outline_view = OutlineView(self.g, code)
        self.outline_view.button_box.add(button2)
        self.frame.add(self.g)
        self.grid = grid
        self.frame.set_margin_top(10)
        window.apply_css_to_widget(self.outline_view.tree_view)
      # window.apply_css_to_widget(self.outline_view.button_box)
        

        self.grid.show_all()
        
    def close_cb(self, button):
        self.frame.set_expanded(False)

    def do_deactivate(self):
        self.outline_view.clean_up()
        self.grid.remove(self.frame)
        self.grid.hide()