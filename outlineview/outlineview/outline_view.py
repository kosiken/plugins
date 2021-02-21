

import gi

gi.require_version('Gtk', '3.0')
from .label_extractor import extract_label
from gi.repository import Gtk

class OutlineView():
    ICONS = ("emu8086-subroutine", "emu8086-const")

    def __init__(self, grid, code) -> None:
        self.buffer = code.get_buffer()
        self.code = code
        self.tree_store = Gtk.TreeStore(str, int, int)
        self.tree_view = Gtk.TreeView(model=self.tree_store)
        self.select = self.tree_view.get_selection()
        self.select.connect("changed", self.on_tree_selection_changed)
        self.buffer.connect("new-line", self.refresh)
        renderer_text = Gtk.CellRendererText()
        renderer_pic = Gtk.CellRendererPixbuf()

        self.column = Gtk.TreeViewColumn()
        
        self.column.pack_start(renderer_pic, False)
        self.column.pack_end(renderer_text, True)
        self.column.add_attribute(renderer_text, "text", 0)
        self.column.set_cell_data_func(renderer_pic,self.render_pix_buf)
        self.tree_view.append_column(self.column)

        self.button_box = Gtk.ActionBar()
        self.button_refresh = Gtk.Button.new_with_label(label="Refresh")
        self.button_refresh.set_relief(Gtk.ReliefStyle.NONE)
        self.button_refresh.connect("clicked", self.refresh)
        self.button_box.add(self.button_refresh)
        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.scrollable_treelist.set_hexpand(True)
        self.scrollable_treelist.add(self.tree_view)
        grid.attach(self.scrollable_treelist, 0, 0, 3, 10)
        grid.attach_next_to(
                            self.button_box, self.scrollable_treelist,Gtk.PositionType.BOTTOM, 3, 1)
        self.grid = grid
        # self.grid.set_column_homogeneous(True)
        self.grid.set_hexpand(True)
        self.button_box.set_hexpand(True)
        self.button_box.set_vexpand(False)
        # grid.set_row_spacing(6)
        self.grid.set_row_homogeneous(True)
        self.grid.show_all()

    def add_labels(self, labels):
        self.tree_store.clear()
        for label in labels:
            treeiter = self.tree_store.append(
                None, [label["name"], label["line"], label["type"]])
            if(label["has_children"]):
                for child in label["children"]:
                    self.tree_store.append(
                        treeiter, [child["name"], child["line"], child["type"]])

    def update(self, string):
        labels = extract_label(string)
        self.add_labels(labels)

    def render_pix_buf(self, col, renderer, model, iter, data):
        pic = model[iter][2]

        renderer.set_property("icon-name", OutlineView.ICONS[pic])

    def refresh(self, btn):
        start, end = self.buffer.get_bounds()
        self.update(self.buffer.get_text(start, end, False))

    def on_tree_selection_changed(self,selection):
        model, iter = selection.get_selected()
        line = model[iter][1]
        line_iter = self.buffer.get_iter_at_line(line - 1)
        self.code.grab_focus()
        self.buffer.place_cursor(line_iter)
        self.code.scroll_to_view()


    def clean_up(self):
        self.grid.remove(self.scrollable_treelist)
        self.grid.remove(self.button_box)
        





