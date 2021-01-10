from gi.repository import GObject
from .lcd_panel_buffer import LCDPanelBuffer
import time
from threading import Timer
# Event object used to send signals from one thread to another
 
 

class LCDDriver(GObject.Object):
    def __init__(self, mode=8):
        GObject.Object.__init__(self)
        self.rs = 0
        self.ren = 0
        self.recieved = 0
        self.mode = mode
        self._text_buffer = LCDPanelBuffer()
        self._buffer_recieved = 0
        self._is_waiting = False

    def recieve_command(self):
        # print(cmd)
        self.recieved = 0
        cmd = self._buffer_recieved
        self._buffer_recieved = 0
        self.recieved =0
        if (cmd == 0xf):
            # LCD ON, Cursor ON, Cursor blinking ON
            self._text_buffer.set_active(True)
            self._text_buffer.set_cursor_on(True)
            self._text_buffer.set_cursor_blink(True)
            pass

        
        elif (cmd == 1):
            # Clear screen
            self._text_buffer.clear_text()
            pass
        elif (cmd == 2):
            # Return home

            self._text_buffer.set_cursor_pos(0)
            pass
        elif (cmd == 4):
            # Decrement cursor
            self._text_buffer.inc_or_dec_cursor_pos(False)
            pass
        elif (cmd == 6):
            # Increment cursor
            self._text_buffer.inc_or_dec_cursor_pos()
            pass
        elif (cmd == 0xe):
            # Display ON ,Cursor blinking OFF
            self._text_buffer.set_active(True)
            pass
        elif (cmd >= 0x80 and cmd <= (0x90)):
            # Force cursor to the beginning of  1st line 
            # or offset cmd - 0x80
            self._text_buffer.set_pos(0)
            print(cmd - 0x80)
            self._text_buffer.set_cursor_pos(cmd - 0x80)
            pass
        elif (cmd >= 0xc0 and cmd <= (0xd0)):
            # Force cursor to the beginning of  2nd line
            # or offset cmd - 0xc0
            self._text_buffer.set_pos(1)
            self._text_buffer.set_cursor_pos(cmd - 0xc0)
            pass   
        elif (cmd == 0x3c):
            # Activate second line
            self._text_buffer.set_second_line_active()
            pass 
        elif (cmd == 0x8):
            # Display OFF, Cursor OFF            
            self._text_buffer.set_active(False)
            self._text_buffer.set_cursor_on(False)
            pass


        pass

    def recieve4(self, ins):
        ins_real = 0x3f & ins
        self.rs = ins_real >> 5
        self.ren = (ins_real >> 4) & 1
        
        if(self._is_waiting):
            return
        print("lion here rc4")
        if(self.recieved < 1):
            self._buffer_recieved = ins_real & 0b1111
            self._is_waiting = True
            self.recieved = 1
            Timer(0.2, self.set_waiting).start()
            # sself.
            return
        elif(self.recieved == 1):
            nibble = ins_real & 0b1111
            byte = self._buffer_recieved << 4
            byte = byte | nibble
            self._buffer_recieved = byte
            self._is_waiting = True
            self.recieved = 2
            Timer(0.2, self.set_waiting).start()

        if(self.rs == 1):
            self.recieve_command()
            return
            pass
       
        else:
            self._text_buffer.add_text(self._buffer_recieved)
            self._buffer_recieved = 0
            self.recieved =0
            pass
        print("ooin")



    def set_waiting(self):
        """
        docstring
        """
        print("swooin")
        self._is_waiting = not self._is_waiting
        pass
    def get_buffer(self):
        """
        docstring
        """
        return self._text_buffer
        pass
            # self._buffer_recieved = 

def wait(obj):
    Timer(0.2, obj.set_waiting)
    