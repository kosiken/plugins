import gi
gi.require_version('Gtk', '3.0')
from gi.repository import  Gtk
from lcd import LCDPanel

win = Gtk.Window()
box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 10)
frame = Gtk.Frame(label="LCD")

box2 = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 10)
panel =LCDPanel()
box.add(panel)
entry = Gtk.Entry()
box.add(entry)
button = Gtk.Button.new_with_label(label="send 0x06")
box2.add(button)
button2 = Gtk.Button.new_with_label(label="send")
box2.add(button2)
def cl1(button):
    """
    docstring
    """
    
    panel._driver.recieve4(0x6)
    pass
def cl2(button):
    """
    docstring
    """
    # panel._driver.recieve4(0xf)
    cmd = (int(entry.get_text()))
    print(cmd)
    panel._driver.recieve4(cmd)
    pass
button.connect("clicked", cl1)
button2.connect("clicked", cl2)



box.add(box2)

box2.show_all()
frame.add(box)
win.add(frame)
win.show_all()
win.connect("destroy", Gtk.main_quit)
Gtk.main()