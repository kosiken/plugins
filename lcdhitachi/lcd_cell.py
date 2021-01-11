import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gtk, Gdk

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
        self._inactive_color =Gdk.RGBA(red=.92,green=.92,blue=.92,alpha=1) 
        self._active_color =Gdk.RGBA(red=0,green=0,blue=0,alpha=1) 
        self._off_color = Gdk.RGBA(red=0.77,green=0.77,blue=0.77,alpha=1) 
        self._cursor_color = Gdk.RGBA(red=0.0,green=0,blue=0.77,alpha=1) 
        self._value = 0x6c
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
    
        


    
    # 3 1 3 1 3 1 3 1 3

# class LCDInnerPanel(Gtk.Box):
#     def __init__(self) -> None:
#         super().__init__()
#         self._disp_mem = list()


win = Gtk.Window()
box = Gtk.Grid.new()
box.set_row_spacing(4)
box.set_column_spacing(4)
mywid2 = LCDCell()
box.add(mywid2)
mywid2.set_active()
mywid2.set_cursor(True, True)
frame = Gtk.Frame(label="LCD")
mywid = LCDCell()

box.add(mywid)

box.insert_row(1)
mywid3 = LCDCell()
box.attach(mywid3,0,1,1,1)
mywid4 = LCDCell()
box.attach(mywid4,1,1,1,1)
b=Gtk.Box.new(Gtk.Orientation.VERTICAL, 10)
button = Gtk.Button.new_with_label(label="Inc Value")
button2 = Gtk.Button.new_with_label(label="Toggle Blink")
button3 = Gtk.Button.new_with_label(label="Dec Value")
b.add(box)
hbox = Gtk.Box.new(Gtk.Orientation.HORIZONTAL,10)
hbox.add(button3)
hbox.add(button)
hbox.add(button2)
b.add(hbox)
def cl2(button):
    """
    docstring
    """
    
    mywid2.set_cursor(True, not mywid2.cursor_blink)
    pass
def cl3(button):
    """
    docstring
    """
    
    mywid2.set_value(mywid2._value - 1)
    pass
def cl1(button):
    """
    docstring
    """
    
    mywid2.set_value(mywid2._value + 1)
    pass
button3.connect("clicked", cl3)
button2.connect("clicked", cl2)
button.connect("clicked", cl1)
frame.add(b)
win.add(frame)
win.show_all()
win.connect("destroy", Gtk.main_quit)
# Gtk.Timeout.add
Gtk.main()
