   # 3 1 3 1 3 1 3 1 3

# class LCDInnerPanel(Gtk.Box):
#     def __init__(self) -> None:
#         super().__init__()
#         self._disp_mem = list()


# win = Gtk.Window()
# box = Gtk.Grid.new()
# box.set_row_spacing(4)
# box.set_column_spacing(4)
# mywid2 = LCDCell()
# box.add(mywid2)
# mywid2.set_active()
# mywid2.set_cursor(True, True)
# frame = Gtk.Frame(label="LCD")
# mywid = LCDCell()

# box.add(mywid)

# box.insert_row(1)
# mywid3 = LCDCell()
# box.attach(mywid3,0,1,1,1)
# mywid4 = LCDCell()
# box.attach(mywid4,1,1,1,1)
# b=Gtk.Box.new(Gtk.Orientation.VERTICAL, 10)
# button = Gtk.Button.new_with_label(label="Inc Value")
# button2 = Gtk.Button.new_with_label(label="Toggle Blink")
# button3 = Gtk.Button.new_with_label(label="Dec Value")
# b.add(box)
# hbox = Gtk.Box.new(Gtk.Orientation.HORIZONTAL,10)
# hbox.add(button3)
# hbox.add(button)
# hbox.add(button2)
# b.add(hbox)
# def cl2(button):
#     """
#     docstring
#     """
    
#     mywid2.set_cursor(True, not mywid2.cursor_blink)
#     pass
# def cl3(button):
#     """
#     docstring
#     """
    
#     mywid2.set_value(mywid2._value - 1)
#     pass
# def cl1(button):
#     """
#     docstring
#     """
    
#     mywid2.set_value(mywid2._value + 1)
#     pass
# button3.connect("clicked", cl3)
# button2.connect("clicked", cl2)
# button.connect("clicked", cl1)
# frame.add(b)
# win.add(frame)
# win.show_all()
# win.connect("destroy", Gtk.main_quit)
# # Gtk.Timeout.add
# Gtk.main()
