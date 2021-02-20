import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk


class OutlineView():
    def __init__(self, code) -> None:
        self.buffer = code.get_buffer()
        self.code = code
        self.tree_store

        pass