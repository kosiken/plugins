from gi.repository import GObject, Gdk, Gtk, Pango


class LCDPanelBuffer(Gtk.TextBuffer):

    DEFAULT_FONT = "DS-DIGITAL BOLD 28"

    def __init__(self, namespace={}):
        Gtk.Label.__init__(self)
        self.buffer = ""
        self.buffer2 = ""
        self.position = 0
        self._cursor_pos = 0
        self.count = 0
        self.count2 = 0
        self.set_text(self.buffer)
        self._active = False
        self._second_line_active = True
        self._cursor_blink = False
        self._cursor_on = False

    def add_text(self,v=1):
        text = ""+ chr(v)
        print(text)
        if(not self._active):
            return
        if(self.position == 0):
            bufferlen = len(self.buffer)
            if(bufferlen >= self._cursor_pos):
                self.buffer = self.buffer + text
            else:
                temp = list(self.buffer)
                temp[self._cursor_pos] = text
                self.buffer = temp.join()
            self._cursor_pos = self._cursor_pos + 1

        elif(self._second_line_active):
            bufferlen = len(self.buffer2)
            if(bufferlen >= self._cursor_pos):
                self.buffer2 = self.buffer2 + text
            else:
                temp = list(self.buffer2)
                temp[self._cursor_pos] = text
                self.buffer2 = temp.join()
            self._cursor_pos = self._cursor_pos + 1

        row1 = ""
        row2 = ""
        self.count = len(self.buffer)
        self.count2 = len(self.buffer2)
        count = 0
        if(self.count > 16):
            count = self.count - 16
        row1 = self.buffer[count:]
        if(self.count2 > 16):
            count = self.count2 - 16
        row2 = self.buffer2[count:]
        grid = row1 + '\n' + row2
        self.set_text(grid)

    def clear_text(self):
        self.buffer = ""
        self.buffer2 = ""
        self.count = 0
        self.count2 = 0
        self._cursor_pos = 0
        self.position = 0

        self.set_text(self.buffer)

    def set_pos(self, pos=0):
        self.position = pos

    def set_active(self, active):
        self._active = active

    def set_cursor_on(self, cursor_on):
        self._cursor_on = cursor_on
        pass

    def set_cursor_blink(self, cursor_blink):
        self._cursor_blink = cursor_blink
        pass

    def set_cursor_pos(self, cursor_pos):
        self._cursor_pos = cursor_pos
        print(self._cursor_pos)
        pass

    def set_second_line_active(self, line_active=True):
        self._second_line_active = line_active

        pass

    def inc_or_dec_cursor_pos(self, inc=True):
        if(inc):
            buflen = 0
            if(self.position < 1):
                buflen = self.count
            else:
                buflen = self.count2
            if(buflen > self._cursor_pos):
                self._cursor_pos = self._cursor_pos+1
                return True
        else:
            if(self._cursor_pos > 0):
                self._cursor_pos = self._cursor_pos-1
                return True
        return False
