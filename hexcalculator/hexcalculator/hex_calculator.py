#
# Copyright 2020 KRC
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#  this list of conditions and the following disclaimer in the documentation
#  and/or other materials provided with the distribution.
#
#
# hex_calculator.py


import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk


class HexCalculator(Gtk.Grid):

    CSS = """
    label {
        color: #f61100;
        font-size: 1.2em
    }
    """
   
    def __init__(self, *args, **kwds):
        """
        docstring
        """

        super().__init__(*args, **kwds)
        self.convert_from = 10
        self.convert_to = 16
        self.convert_from_str = "Decimal"
        self.convert_to_str = "Hexadecimal"       
        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("Enter a number")
        combo1_store = Gtk.ListStore(int, str)
        combo2_store = Gtk.ListStore(int, str)
        base_num = 1

        combo1_store.append([10, "Decimal"])
        combo2_store.append([10, "Decimal"])

       
        for base in ["Binary","Octal","Hexadecimal"]:
            # print(2**base_num)
            combo1_store.append([2**base_num, base])
            combo2_store.append([2**base_num, base])
            if(base_num == 1):
                base_num = base_num + 1
            base_num = base_num + 1

        self.button = Gtk.Button.new_with_label("Convert")
        self.label = Gtk.Label(label="")
        self._style_prov = Gtk.CssProvider()
        style_context = self.label.get_style_context()
        style_context.add_provider(self._style_prov, 999)
        s= HexCalculator.CSS.strip()


        self._style_prov.load_from_data( bytes(s, "utf8"))
        self.combo1 = Gtk.ComboBox.new_with_model_and_entry(combo1_store)
        self.combo2 = Gtk.ComboBox.new_with_model_and_entry(combo2_store)
        self.combo1.set_entry_text_column(1)
        self.combo1.set_active(0)
        self.combo2.set_entry_text_column(1)
        self.combo2.set_active(3)   
        self.combo1.connect("changed", self.on_combo1_changed)
        self.combo2.connect("changed", self.on_combo2_changed)
        self.button.connect("clicked", self.convert_to_num)
        self.set_row_spacing(6)
        self.set_margin_start(10)
        self.set_margin_end(10)
        self.attach(self.entry, 0, 0,1,1)
        self.attach(self.combo1, 0, 1,1,1)
        self.attach(self.combo2, 0, 2,1,1)
        self.attach(self.button, 0, 3,1,1)
        self.attach(self.label, 0, 4,1,1)


    def on_combo1_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            row_id, name = model[tree_iter][:2]
            self.convert_from_str = name
            self.convert_from = row_id
            # print("Selected: ID=%d, name=%s" % (row_id, name))


    def on_combo2_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            row_id, name = model[tree_iter][:2]
            self.convert_to_str = name
            self.convert_to = row_id
            # print("Selected: ID=%d, name=%s" % (row_id, name))


    def convert_to_num(self, button=None):
        text = self.entry.get_text()
        if(len(text) == 0):
            return
        num=0
        try:
            num = int(text, self.convert_from)
        except ValueError as err:
            self.label.set_label(str(err))
            return

        self.entry.set_text(HexCalculator.convert(self.convert_to, num))
        self.label.set_label("")

    @staticmethod
    def convert(to, num):
        ans = ""
        hex_array = ['F', 'E', 'D', 'C', 'B', 'A']
        _num = int(num)
        # print("num: ",to)
        while (_num >= 1):
            m = _num % to
            
            if((to == 16) and (m > 9) ):

                mod = hex_array[15 - m]
            else: mod = str(m)
            # # print("m: ",m)
            ans =  str(mod) + ans
            _num = int(_num / to)
            
        return ans


