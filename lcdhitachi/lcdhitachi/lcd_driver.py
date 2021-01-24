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
# lcd_driver.py


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gtk
import time
from .lcd_cell import LCDCell


class LCDDriver(GObject.Object):
    CLEAR_DISP_TIME = 0
    RETURN_HOME = 152/100
    EMS_TO_SDRAM_ADDR_R_W = 4/100
    READ_BF = 0

    def __init__(self, parent, mode=4):
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
        self._reg_to_write = 0
        self._cursor_position = 0
        self._last_cursor = 0
        self._entry_incr = 1
        self._current_row = 1
        self._cursor_position2 = 0
        self.index = [0, 0]
        self._cursor_on = False
        self._display_on = False
        self._blink = False
        self.first = True
        self._instruction_stack = []
        self._display_shift = 0
        self._mem_addr_pointer = 0
        self._cg_addr_pointer = 0
        self.memory = []
        self.cg_mem = []

        self._font = 5 * 8
        self.rows = 0
        self._function_set = False
        x = 0
        y = 0
        for i in range(0, 32):
            cell = LCDCell()
            # cell.show
            parent.attach(cell, x, y, 1, 1)
            # cell.queue_draw
            x = x + 1
            if(x > 15):
                y = 1
                x = 0
            cell.index = i
            self.cells.append(cell)
            self.cg_mem.append(0)
            self.memory.append(32)
            pass
        for i in range(0, (80 - 32)):
            # self.cells.append(LCDCell())
            self.memory.append(32)
            if(i < (64-32)):
                self.cg_mem.append(0)
            pass
        self._selected_cell = self.cells[0]
        # print(len(self.cg_mem))

    def command_exec(self, param=0):
        # # print(param)

        if(param > 0x7f):
            self.set_ddr_addr(param)
        elif (param > 0x3f):
            self.set_cg_addr(param)
            pass
        elif (param > 0x1f):
            self.function_set(param)
            pass
        elif (param > 0xf):
            self.cursor_or_disp_shift(param)
            pass
        elif (param > 7):
            self.display_on_off(param)
            pass
        elif (param > 3):
            self.entry_mode_set(param)
            pass
        elif (param > 1):
            self.return_home(param)
            pass
        else:
            self.cld()
        # print("rst")
        self.rst()
        pass

    def _set_cursor(self, cursor_pos):
        """
        docstring
        """
        if(cursor_pos < 0):
            self._cursor_position = 0
        elif (cursor_pos > 0xf):
            self._cursor_position = 0xf
            pass
        else:
            self._cursor_position = cursor_pos
        pass

    def rst(self):
        """
        docstring
        """
        self._buffer_recieved = 0
        # self._recieved = 0
        self.recieved = 0
        self.ren = 0
        self.busy_flag = False
        pass

    @staticmethod
    def get_bit(value, bit):
        """
        docstring
        """
        return (value >> bit) & 1

    def cld(self):
        """
        docstring
        """
        if(not self._display_on):
            return
        # print("cld")
        # time.sleep(LCDDriver.CLEAR_DISP_TIME)
        for i in range(0, 80):
            self.memory[i] =32
            pass
        self._cursor_position2 = 0
        self._cursor_position = 0
        self._mem_addr_pointer = 0
        self.index[0] = 0
        self.index[1] = 0
        self._current_row = 1
        self._display_shift=0
        self._entry_incr = 1
        
        for cell in self.cells:
            cell.cmp_and_set_val(32)
            pass
        self._update_cursor()

        pass

    def return_home(self, param=2):
        """
        docstring
        """
        # time.sleep(LCDDriver.RETURN_HOME)
        self._mem_addr_pointer = 0
        self.index[0] = 0
        self._current_row = 1
        self._display_shift = 0
        self.shift_disp()

        # print("r_h")
        pass

    def entry_mode_set(self, param=4):
        """
        docstring
        
        """
        s = param & 1
        i_d = LCDDriver.get_bit(param, 1)
        self._shift = s == 1
        # time.sleep(LCDDriver.EMS_TO_SDRAM_ADDR_R_W)
        if(i_d == 1):
            self._entry_incr = 1
        else:
            self._entry_incr = -1
        # print("e_m_s %x" % param, self._entry_incr, self._shift)
        pass

    def display_on_off(self, param):
        """
        docstring
        """
        b = param & 1
        c = LCDDriver.get_bit(param, 1)
        d = LCDDriver.get_bit(param, 2)
        self._cursor_on = c == 1
        self._display_on = d == 1
        self._blink = b == 1
        # # time.sleep(LCDDriver.EMS_TO_SDRAM_ADDR_R_W)

        if(self._display_on):
            # print("on oooooo",self._blink, self._cursor_on)
            for cell in self.cells:
                cell.set_active()
            self.update_cells()
        # print("do: %x" % param)
        pass

    def cursor_or_disp_shift(self, param):
        """
        docstring
        """
        r_l = LCDDriver.get_bit(param, 2)
        s_c = LCDDriver.get_bit(param, 3)
        prev_shift = self._shift
        self._shift = s_c == 1
        v = self._display_shift
        cursor_pos = self._cursor_position
        if(r_l == 0):
          
            cursor_pos = cursor_pos + 1
            v = v+1
            pass
        else:
            cursor_pos = cursor_pos - 1
            v = v-1
            if(v<0):
                v = 0
            
 
        # self._mem_addr_pointer = v

        # print(v, self._shift)

            # # time.sleep(LCDDriver.EMS_TO_SDRAM_ADDR_R_W)



        if((self._current_row == 1) and cursor_pos>0xf and self.rows == 2):
            self._current_row = 2
            cursor_pos = 0
            
        elif (self.rows == 2 and cursor_pos < 0):
            self._current_row = 1
            cursor_pos = 0xf
            pass
        elif (cursor_pos >0xf):

            cursor_pos = 0xf
            pass

        elif (cursor_pos < 0):
            cursor_pos = 0


            pass
        
        if(self._shift == False):
            self._set_cursor(cursor_pos)
            self.update_cells()
            self.set_index_from_addr(True)
        else:
            max_shift = self.get_max_shift()
            self._display_shift = v
            if(v > max_shift):
                self._display_shift = max_shift

            self.set_index_from_addr()
            self.shift_disp()



        self._shift = prev_shift
        pass

    def get_max_shift(self):
        """
        docstring
        """
        return int(80/(self.rows)) - 16
        pass

    def set_index_from_addr(self, shift=False):
        """
        docstring
        """
        if(self.rows == 1 or self._current_row == 2):
            self.index[0] = self._mem_addr_pointer 
            
            
        else:
            self.index[1] = self._mem_addr_pointer - 0x40
        
        i=self._current_row -1
        if(shift):
            self._display_shift = int(self.index[i]/16) 


  
    def function_set(self, param):
        """
        docstring
        """
        # # time.sleep(LCDDriver.EMS_TO_SDRAM_ADDR_R_W)

        f = LCDDriver.get_bit(param, 2)
        n = LCDDriver.get_bit(param, 3)
        d_l = LCDDriver.get_bit(param, 4)
        self.mode = (d_l * 4)+4
        if(n == 0):
            self._current_row = 1
            if(f == 1):
                self._font = 5 * 10
            else:
                self._font = 5 * 8
            if(self.rows == 2):
                for i in range(16, 32):
                    cell = self.memory[i]
                    cell.cmp_and_set_val(0)
                    if(self._mem_addr_pointer > 0x40):
                        self._mem_addr_pointer = self._mem_addr_pointer - 0x40
            self.rows = 1
            self.shift_disp()
        else:
            if(self.rows == 1):
                for i in self.index:
                    if(i > 39):
                        i = i-39

            self.rows = 2
            self._font = 5 * 8

        self._function_set = True
        # print(self.mode, self.rows)
        pass

    def set_cg_addr(self, param):
        """
        docstring
        """
        # # time.sleep(LCDDriver.EMS_TO_SDRAM_ADDR_R_W)

        addr = param & 0b111111
        self._mem_addr_pointer = addr
        self._reg_to_write = 1
        pass

    def set_ddr_addr(self, param):
        """
        docstring
        """
        # time.sleep(LCDDriver.EMS_TO_SDRAM_ADDR_R_W)
        self._reg_to_write = 0
        addr = param & 0b1111111

        if((self.rows == 1) and (addr < 0x50)):
            self.index[0] = addr
            self._current_row = 1
            self._cursor_position = (param - 0x80) & 0xf

        elif((addr > 0x2f) and (addr < 0x40) or (addr > 0x67)):
            return

        elif(addr < 0x28):
            self._current_row = 1
            self._cursor_position = (param - 0x80) & 0xf
            self.index[0] = addr
        else:
            self._current_row = 2
            self._cursor_position = (param - 0xc0) & 0xf
            self.index[1] = addr - 0x40
        self.resolve_shift()
        if(not self._shift):
            
            self._cursor_position2 = self._cursor_position
        else:
            self._cursor_position = self._last_cursor
        
        self._mem_addr_pointer = addr
        self._last_cursor = self._cursor_position
        self.update_cells()
        pass

    def resolve_shift(self):
        """
        docstring
        """
        offs = self.index[self._current_row - 1]  - 16
        if(offs<0):
            offs = 0
        self._display_shift = offs
            # self._display_shift = 
        # if()
    def read_bf(self):
        """
        docstring
        """
        return self.busy_flag

    def get_val(self, start, stop):
        v = 0
        end = 39
        if(self.rows == 1):
            return self.memory
        if(start > 0x39):
            v = 40
            end = 79
        return self.memory[v:end]

    def shift_disp(self):
        """
        docstring
        """
        arr = self.get_val(0, 0x27)
        offset = self._display_shift

        offset_end = offset+16
        if(offset_end > 39):
            offset_end = 39
        index = 0
        arr = arr[offset:offset_end]
        # print(arr)
        for val in arr:
            if(index > 15):
                break
            cell = self.cells[index]
            cell.cmp_and_set_val(val)
            index = index+1
            pass

        if(self.rows == 1):
            return

        arr = self.get_val(0x40, 0x67)

        arr = arr[offset:offset_end]
        # print(arr)
        index = 0
        for val in arr:
            if(index > 15):
                break
            cell = self.cells[index + 16]
            cell.cmp_and_set_val(val)
            index = index+1
            pass

    def update_cells(self, redraw=True):
        """
        docstring
        """
        s = ""
        # print(self._mem_addr_pointer, self._current_row)
        # self._page_offset = int(self._mem_addr_pointer/16)

        beep = 0
        if(self._shift):
            return self.shift_disp()
        arr = []
        start = self._display_shift
        if(self._current_row == 1):
            arr = self.get_val(0, 0x2f)

        else:
            arr = self.get_val(0x40, 0x67)

        arr = arr[start:(start+16)]

        index = 0
        for val in arr:
            cell = self.cells[index + ((self._current_row - 1)*16)]
            if(val < 0xf):
                the_off = (val&0x7) * 8
                # print(val,self.cg_mem[the_off:(the_off + 8)])
                the_data = self.cg_mem[the_off:(the_off + 8)]
                cell.set_matrix(the_data)
                pass
            else:
                cell.cmp_and_set_val(val)
            index = index+1
            pass
        self._update_cursor()
        index = 0

    def _update_cursor(self):

        index = 0

        # time.sleep(0.2)
        for i in range(0, 16):

            # s=s+ chr(self.memory[i])
            # s = s + ' '
            cell = self.cells[index + ((self._current_row - 1)*16)]

            if(self._cursor_position == index):
                if((self._selected_cell.index != cell.index) or self.first):
                    if(not self.first):
                        self._selected_cell.set_cursor(False, False)
                    cell.set_cursor(self._cursor_on, self._blink)
                self._selected_cell = cell

            index = index+1
            if(self.first):
                self.first = False


            pass
        # l.reverse()
        # # print(l)
        pass

    def resolve_mem_pointer(self):
        if (self._mem_addr_pointer < 0):
            self._mem_addr_pointer = 0
            return

        if(self.rows == 1):
            if(self._mem_addr_pointer > 0x40):
                self._mem_addr_pointer = 0x40

        elif (self._current_row == 1):
            if(self._mem_addr_pointer > 0x2f):
                self._mem_addr_pointer = 0x2f
        elif (self._mem_addr_pointer > 0x67):
            self._mem_addr_pointer = 0x67
            pass

    def write_to_cg_ram(self, value):
        """
        docstring
        """
        # print(self.cg_mem[0:self._mem_addr_pointer+1])
        self.cg_mem[self._mem_addr_pointer] = value
        self._mem_addr_pointer = self._entry_incr + self._mem_addr_pointer
        if(self._mem_addr_pointer<0):
            self._mem_addr_pointer = 0
        elif (self._mem_addr_pointer > 63):
            self._mem_addr_pointer = 63
            pass
        pass

    def write_data(self, data):
        """
        docstring
        """
        # # print("ppp",data)
        # return
        if(not self._function_set):
            return
        # print("reg to write", self._reg_to_write)

        if(self._reg_to_write == 1):
            self.write_to_cg_ram(data)
            self.rst()
            return


        self._last_cursor = self._cursor_position
        index = self.index[self._current_row-1]

        if((index > 39) and (self.rows == 2) or (index > 79)):
            return

        if(self._current_row == 1):

            self.memory[index] = data
        else:
            # print(self._shift, self._cursor_position, self.index,self._display_shift)
            self.memory[40 + index] = data

        self._mem_addr_pointer = self._entry_incr + self._mem_addr_pointer

        index = index + self._entry_incr
        if(index < 0):
            index = 0
        if((index > 39) and (self.rows == 2)):
            index = 39
        elif ((index > 79)):
            index = 39

            pass
        
        self.index[self._current_row - 1] = index

        self._cursor_position2 = self._entry_incr + self._cursor_position2
        self.resolve_mem_pointer()

        if(self._cursor_position2 < 0):
            self._cursor_position2 = 0
            


        elif (self._cursor_position2 > 0xf):

            self._cursor_position2 = 0xf
            pass
        

        _display_shift = self._display_shift
        if(self._shift):
            _display_shift = _display_shift + self._entry_incr

            self._cursor_position = self._last_cursor
            pass
        else:
            self._cursor_position = self._cursor_position2
        

        if (_display_shift < 0):
                _display_shift = 0
                pass


        if ((self.rows > 1) and (_display_shift > (39 - 16))):
            _display_shift = 39 - 16

        elif (_display_shift > (79 - 16)):
            _display_shift = 39 - 16    

        self._display_shift = _display_shift    
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
        # print("rc", param1,param2)
        if(self.mode == 4):
            self.recieve4(param1)
        else:
            # print("err")
            self.recieve8(param1, param2)
        pass

    def recieve4(self, ins):
        """
        docstring
        """

        # print("mem: self.m %x" % self._mem_addr_pointer)
        v = int(ins)
        ins_real = 0x3f & v
        self.rs = ins_real >> 5
        prev_ren = self.ren
        self.ren = (ins_real >> 4) & 1
        # # print(prev_ren, ' ',self.rs)
        can_rec = False
        can_rec = (prev_ren == 1 and self.ren == 0)
        if(not can_rec):
            return
        # print(prev_ren, ' ', self.rs)

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
        self.busy_flag = True

        if(self.rs == 1):
            # print("cmd")
            self.command_exec(self._buffer_recieved)
        else:
            # print("data")
            self.write_data(self._buffer_recieved)

        pass

    def set_waiting(self):
        """
        docstring
        """

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
        can_rec = (prev_ren == 1 and self.ren == 0)
        if((not can_rec) or self.busy_flag):
            return
        self._buffer_recieved = v1
        if(self.rs == 1):
            self.command_exec(v1)
        else:
            self.write_data(v1)
        pass

    def clear_out(self, parent):
        """
        docstring
        """
        for cell in self.cells:
            cell.set_cursor(False, False)
            # # time.sleep(0.5)
            parent.remove(cell)
        pass

    def shift_disp_by_val(self, val, shift=True):
        """
        docstring
        """
        _display_shift = self._display_shift
        if(shift):
            _display_shift = _display_shift + val

            # self._cursor_position = self._last_cursor
            pass
        else:
            return
        

        if (_display_shift < 0):
                _display_shift = 0
                pass


        if ((self.rows > 1) and (_display_shift > (39 - 16))):
            _display_shift = 39 - 16

        elif (_display_shift > (79 - 16)):
            _display_shift = 39 - 16    

        if(_display_shift == self._display_shift):
            return
        self._display_shift = _display_shift 
        self.shift_disp()
        
        pass
