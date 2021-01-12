import gi
import time
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, GLib, Gtk, Gdk

from lcdhitachi import PatternGenerator

class LCDCell(Gtk.Misc):
    HEIGHT = (5*8) + 8
    WIDTH = (5*5) + 5

    def __init__(self, *args, **kwds):
        """
        docstring
        """

        super().__init__( *args, **kwds)   
        self.has_cursor = False
        self.cursor_blink = False
        self._is_active = False
        self._blink_on = False
        # self.set_vexpand(False)
        # self.set_hexpand(False)
        self._inactive_color =Gdk.RGBA(red=.70,green=.70,blue=.70,alpha=1) 
        self._active_color =Gdk.RGBA(red=0,green=0,blue=0,alpha=1) 
        self._off_color = Gdk.RGBA(red=0.77,green=0.77,blue=0.77,alpha=1) 
        self._cursor_color = Gdk.RGBA(red=0.0,green=0,blue=0.77,alpha=1) 
        self._value = 93 + 33
        self.set_size_request(LCDCell.WIDTH, LCDCell.HEIGHT)
       
        pass

    def do_get_preferred_size (self, requisition):
        
        requisition.width  = LCDCell.WIDTH
        requisition.height = LCDCell.HEIGHT
    def do_size_allocate(self, a):
        """
        docstring
        """
        a.width = LCDCell.WIDTH
        a.height = LCDCell.HEIGHT
        self.set_allocation(a)
        pass
    def set_value(self, value=93):
        
        self._value = value
        self.queue_draw() 
    def cmp_and_set_val(self, value) -> bool:

        if(self._value == value or value == 0):
            return False
        self.set_value(value)
        return True


    

    def do_draw(self, cr):
        """
        docstring
        """
        bg_color = self._inactive_color
        if(self._is_active):
            bg_color = self._off_color
            pass
       
        cr.set_source_rgba(*list(bg_color))
        cr.paint()
        if(not self._is_active):
            return
        # m_len = len(matrix)
        matrix = PatternGenerator.render_pattern_to_matrix(self._value - 33)
        m_len = len(matrix)
        for i in range(0,m_len):
            b = len(matrix[i])
            for j in range(0,b):

                # cr.move_to(0, 0)
               
                
                if(matrix[i][j ] == 1):
                    
                    cr.set_source_rgba(*list(self._active_color))
                    pass
                else:

                    cr.set_source_rgba(*list(self._off_color))
                    pass
                cr.rectangle(j * 6, i*6, 5, 5)
                cr.fill()
                pass
            pass
        blink_color = self._cursor_color
        
        if(self.cursor_blink and self.has_cursor):
            
                if( not self._blink_on):
                    blink_color = self._off_color
                # print("ll")
                             
                cr.set_source_rgba(*list(blink_color))
                cr.rectangle(0, 7*6, LCDCell.WIDTH, LCDCell.HEIGHT)
                cr.fill()
              
        elif (self.has_cursor):
            # for j in range(0,5):

                             
                cr.set_source_rgba(*list(blink_color))
                cr.rectangle(0, 7*6, LCDCell.WIDTH, LCDCell.HEIGHT)
                cr.fill()            
            # pass
                


                    

        # allocation = self.get_allocation()


        pass
    def set_active(self, active=True):
        """
        docstring
        """
        self._is_active = active
        pass
    def set_cursor(self, has_cursor=True, blink=False):

        self.has_cursor = has_cursor
        if(blink & self.cursor_blink):
            return
        elif (not blink):
          
            self.cursor_blink = blink
            # GObject.Souce.remove(self.to)
            return
        else:
           
            # return
            self.cursor_blink = blink
            self.to = GLib.timeout_add(500, self.toggle_blink)
            
    
        pass
    def toggle_blink(self):
        self._blink_on = not self._blink_on
        
        self.queue_draw()
        return (self.cursor_blink and self.has_cursor)   
    
        


    
class LCDDriver(GObject.Object):
    CLEAR_DISP_TIME = 0
    RETURN_HOME = 152/100
    EMS_TO_SDRAM_ADDR_R_W = 4/100
    READ_BF = 0


    def __init__(self, mode=4):
        GObject.Object.__init__(self)
        self.rs = 0
        self.ren = 0
        self.recieved = 0
        self.mode = mode
        self._shift = False
        self._buffer_recieved = 0
        self.busy_flag = False
        self.cells = []
        self._instruction_stack = []
        self._page_offset = 0
        self._cursor_position = 0
        self._last_cursor = 0
        self._entry_incr = 1
        self._current_row = 1
        self.index = 0
        self._cursor_on = False
        self._display_on = False
        self._blink = False
        self._instruction_stack = []
        self._mem_addr_pointer = 0
        self._cg_addr_pointer = 0
        self.memory = []
        self._cg_ram_ptr = 0
        self.n_dl = 2
        
        for i in range(0,32):
            self.cells.append(LCDCell()) 

            self.memory.append(0)            
            pass
        for i in range(0,(80 - 32)):
            # self.cells.append(LCDCell()) 
            self.memory.append(0)            
            pass
    
    def command_exec(self, param=0):
        # print(param)

        if(param>0x7f):
            self.set_ddr_addr(param)
        elif (param>0x3f):
            self.set_cg_addr(param)
            pass
        elif (param>0x1f):
            self.function_set(param)
            pass
        elif (param>0xf):
            self.cursor_or_disp_shift(param)
            pass
        elif (param>7):
            self.display_on_off(param)
            pass
        elif (param>3):
            self.entry_mode_set(param)
            pass
        elif (param>1):
            self.return_home(param)
            pass 
        else:
            self.cld() 
        print("rst")
        self.rst()

    def rst(self):
        """
        docstring
        """
        self._buffer_recieved = 0
        # self._recieved = 0
        self.recieved = 0
        self.ren = 0
        self.busy_flag= False 
        pass
 


    @staticmethod
    def get_bit(value, bit):
        """
        docstring
        """
        return  (value >> bit) & 1
        
    def cld(self):
        """
        docstring
        """
        print("cld")
        time.sleep(LCDDriver.CLEAR_DISP_TIME)
        for i in range(0,80):
            self.memory[i] = 0
            pass
        self._cursor_position=0
        self._mem_addr_pointer=0
        self.index=0
        self._current_row=0


        pass

    def return_home(self, param=2):
        """
        docstring
        """
        time.sleep(LCDDriver.RETURN_HOME)
        self._mem_addr_pointer = 0
        self.index=0

        print("r_h")
        pass
    def entry_mode_set(self, param=4):
        """
        docstring
        """
        s= param&1
        i_d = LCDDriver.get_bit(param,1)
        self._shift = s == 1
        time.sleep(LCDDriver.EMS_TO_SDRAM_ADDR_R_W)
        if(i_d == 1):
            self._entry_incr = 1
        else:
            self._entry_incr = -1
        print("e_m_s %x"%param, self._entry_incr, self._shift)
        pass
    def display_on_off(self, param):
        """
        docstring
        """
        b = param&1
        c = LCDDriver.get_bit(param,1)
        d = LCDDriver.get_bit(param,2)
        self._cursor_on = c == 1
        self._display_on = d == 1
        self._blink = b == 1
        time.sleep(LCDDriver.EMS_TO_SDRAM_ADDR_R_W)

        if(self._display_on):
            for cell in self.cells:
                cell.set_active()
            self.update_cells()
        print("do: %x"%param)
        pass

    def cursor_or_disp_shift(self, param):
        """
        docstring
        """
        r_l = LCDDriver.get_bit(param,2)
        s_c = LCDDriver.get_bit(param,3)
        if(not (r_l or s_c)):
            pass

        time.sleep(LCDDriver.EMS_TO_SDRAM_ADDR_R_W)

        pass
    def function_set(self, param):
        """
        docstring
        """
        time.sleep(LCDDriver.EMS_TO_SDRAM_ADDR_R_W)

        f = LCDDriver.get_bit(param,2)
        n = LCDDriver.get_bit(param,3) 
        d_l = LCDDriver.get_bit(param,4)
        self.mode = (d_l * 4)+4
        if(d_l==0):
            self.rows = 1
        print(param)
        pass

    def set_cg_addr(self, param):
        """
        docstring
        """
        time.sleep(LCDDriver.EMS_TO_SDRAM_ADDR_R_W)

        addr = param & 0b111111
        self._cg_addr_pointer = addr
        pass
    def set_ddr_addr(self, param):
        """
        docstring
        """
        time.sleep(LCDDriver.EMS_TO_SDRAM_ADDR_R_W)

        addr = param & 0b1111111
        self._mem_addr_pointer = addr
       
        for cell in self.cells:
            cell.set_cursor(False,False)
        if(addr < 0x28):
            self._current_row = 1
            self._cursor_position = (param - 0x80) & 0xf
        else:
            self._current_row = 2
            self._cursor_position = (param - 0xc0) & 0xf
        if(self._shift):
            self._cursor_position = self._last_cursor
        self.update_cells()
        self._last_cursor = self._cursor_position
        pass
    def read_bf(self):
        """
        docstring
        """
        return self.busy_flag

    def get_val(self, start, stop):
        v=0
        end = 39
        if(start > 0x39):
            v = 40
            end = 79
        return self.memory[v:end]

    def shift_disp(self):
        """
        docstring
        """
        arr= self.get_val(0,0x27)
        off1 = 0
        off2 = self._mem_addr_pointer
        if(self._mem_addr_pointer > 0x40):
            off2 = self._mem_addr_pointer - 0x40
        arr = self.get_val(0,0x27)
        arr = arr[off1:off2]
        li = len(arr)
        mo=li - 16
        if(mo<0):
            mo =0
        arr = arr[mo:]
        index = 0
        for val in arr:
            cell = self.cells[index]
            cell.cmp_and_set_val(val)
            index = index+1
            pass
        index = 0
        arr = self.get_val(0x40,0x67)
        arr = arr[off1:off2]
        li = len(arr)
        mo=li - 16
        if(mo<0):
            mo =0
        arr = arr[mo:]
        index = 0
        for val in arr:
            cell = self.cells[index + ((1)*16)]
            cell.cmp_and_set_val(val)
            index = index+1
            pass
        index = 0


    def update_cells(self, redraw=True):
        """
        docstring
        """
        s=""
        print(self._mem_addr_pointer, self._current_row)
        # self._page_offset = int(self._mem_addr_pointer/16)
     
        beep =0
        if(self._shift):
            return self.shift_disp()
        start = self._mem_addr_pointer - 1

        offset = 0
        off1 = 0
        off2 = self._mem_addr_pointer
        
        if(self._mem_addr_pointer>63):
            offset = 0x40
            off2 = self._mem_addr_pointer - 0x40
            
            
        offset2 = offset + 0x27

        arr = self.get_val(offset,self._mem_addr_pointer)

        arr = arr[off1:off2]
        li = len(arr)
        mo=li - 16
        if(mo<0):
            mo =0
        arr = arr[mo:]
        print(arr, mo,self._mem_addr_pointer)
        

       
        l = dict()
        
        start = 0
        beep = start + 16    
        index = 0
        for val in arr:
            cell = self.cells[index + ((self._current_row - 1)*16)]
            cell.cmp_and_set_val(val)
            index = index+1
            pass
        index = 0
        for i in range( start,beep):
            if(i>79):
                break
            # s=s+ chr(self.memory[i])
            # s = s + ' '
            cell = self.cells[index + ((self._current_row - 1)*16)]
            
 
            if(self._cursor_position == index):

                cell.set_cursor(self._cursor_on, self._blink)
            else:
                cell.set_cursor(False, False)
           
            # print(i,' ', self.memory[i])
            # l[str(i)] = self.memory[i]
            index= index+1
            pass
        # l.reverse()
        # print(l)
        pass
    def write_data(self, data):
        """
        docstring
        """
        # print("ppp",data)
        # return
        self._last_cursor = self._cursor_position
        if(self.index>39):
            return
        if(self._current_row == 1):
            self.memory[self.index] = data
        else:
            self.memory[40+self.index] = data
            pass
        self._mem_addr_pointer = self._entry_incr + self._mem_addr_pointer
        self.index=self.index + self._entry_incr
        self._cursor_position = self._entry_incr +self._cursor_position
        if(self._mem_addr_pointer>0x67):
            self._mem_addr_pointer=0x67
        elif (self._mem_addr_pointer < 0):
            self._mem_addr_pointer = 0
            pass

        
        if(self._cursor_position < 0):
            self._cursor_position = 0xf
            
        elif (self._cursor_position >0xf):
            self._cursor_position = 0xf
        if(self._shift):
            self._cursor_position=self._last_cursor
            pass
        self.update_cells()
        self.rst()
        pass
    def _check_inc_dec_offset(self, inc=True):
        """
        docstring
        """
        if(inc):
            if(self._page_offset < 65):
                self._page_offset = self._page_offset + 1
            return
        if(self._page_offset > 0):
            self._page_offset = self._page_offset - 1
        pass

    def recieve(self, param1, param2):
        """
        docstring
        """
        if(self.mode == 4):
            self.recieve4(param1)
        else:
            self.recieve8(param1, param2)
        pass
    def recieve4(self, ins):
        """
        docstring
        """
        v = int(ins)
        ins_real = 0x3f & v
        self.rs = ins_real >> 5
        prev_ren = self.ren
        self.ren = (ins_real >> 4) & 1
        # print(prev_ren, ' ',self.rs)
        can_rec = False
        can_rec = (prev_ren == 1 and self.ren==0 )
        if(not can_rec):
            return
        print(prev_ren, ' ',self.rs)

 

        if(self.recieved < 1):
            self._buffer_recieved = ins_real & 0b1111
            # self._is_waiting = True
            self.recieved = 1
            return

        elif(self.recieved == 1):
            nibble = ins_real & 0b1111
            byte = self._buffer_recieved << 4
            byte = byte | nibble            
            self._buffer_recieved = byte
            
            self.recieved = 2
        if(self.busy_flag):
            return
        self.busy_flag= True

        if(self.rs == 1):
            
            self.command_exec(self._buffer_recieved)
        else:
            
            self.write_data(self._buffer_recieved)        

        pass
    def set_waiting(self):
        """
        docstring
        """
        print("swooin")
        self.busy_flag = not self.busy_flag
        pass    

    def recieve8(self, ins, flags):
        """
        docstring
        """
        v1 = int(ins)
        v = int(flags)
        ins_real = v
        self.rs = (ins_real >> 1) & 1
        prev_ren = self.ren
        self.ren = (ins_real) & 1
        can_rec = (prev_ren == 1 and self.ren==0 )
        if((not can_rec) or self.busy_flag):
            return
        self._buffer_recieved = v1
        if(self.rs == 1):
            self.command_exec(v1)
        else:
            self.write_data(v1)



        pass



drv = LCDDriver()
win = Gtk.Window()
box = Gtk.Grid.new()
box.set_row_spacing(4)
x = 0
y = 0
box.set_column_spacing(4)
for cell in drv.cells:
    # cell.set_active()

    box.attach(cell,x,y,1,1)
    x = x + 1
    if(x>15):
        y = 1
        x = 0
drv.cells[0].set_cursor(True, True)
frame = Gtk.Frame(label="LCD")
# for i in "lions are comming to town":

    # drv.write_data(ord(i))
# drv.update_cells()
class mincr():
    def __init__(self) -> None:
        self.index = 0

    def inc_index(self):
        self.index = self.index + 1

incr = mincr()
# bou===
msg = "lions are comming to town"
m_l = len(msg)
def cl1(button):
    """
    docstring
    """
    es=""
    c = entry.get_text()
    c= c.split(',')
    c.reverse()
    s =c.pop()
    c.reverse()
    p = len(c) - 1
    for st in c:

        es= es+st
        if(p>0):
             es = es+','
        p = p -1
    entry.set_text(es)
    drv.recieve(int(s.strip(), base=16),0)

    # v = int(c,base=16)
    # drv.recieve(v,0)
    # print(v)
    # index = incr.index
    # if(index == m_l):
    #     return False
    
    # char = msg[index]
    # # drv.write_data(ord(char))
    # # drv.update_cells()
    # incr.inc_index()
    

    
    
    pass
b=Gtk.Box.new(Gtk.Orientation.VERTICAL, 10)
button = Gtk.Button.new_with_label(label="Putc")
button2 = Gtk.Button.new_with_label(label="Toggle Blink") 
button3 = Gtk.Button.new_with_label(label="Dec Value")
b.add(box)
entry = Gtk.Entry()
b.add(entry)
hbox = Gtk.Box.new(Gtk.Orientation.HORIZONTAL,10)
hbox.add(button3)
hbox.add(button)
hbox.add(button2)
button.connect("clicked", cl1)
b.add(hbox)
frame.add(b)
win.add(frame)
win.show_all()
win.connect("destroy", Gtk.main_quit)
# Gtk.Timeout.add
Gtk.main()

