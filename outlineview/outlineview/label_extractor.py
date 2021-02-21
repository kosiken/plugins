# k="""
#         ;
#         ; RevStr
#         ; Reverse a string with di and si
#         ;
#         ; by Allison Kosy
#         ; http://kosiken.github.io/
#         ;
#         ; (c) Copyright 2020 krc.
#         ;
#         ; Creation date: Dec/21/2019.
#         ;
#         ; Permission is hereby granted, free of charge, to any person obtaining a copy
#         ; of this software and associated documentation files (the "Software"), to deal
#         ; in the Software without restriction, including without limitation the rights
#         ; to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#         ; copies of the Software, and to permit persons to whom the Software is
#         ; furnished to do so, subject to the following conditions:

#         ; The above copyright notice and this permission notice shall be included in all
#         ; copies or substantial portions of the Software.

#         ; THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#         ; IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#         ; FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#         ; AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#         ; LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#         ; OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#         ; SOFTWARE.    
# ;--------------------------------------------------------------------------------------------

# ;   begin


#         mov sp, 128
#         push cs
#         push cs
#         pop ds
#         pop es

#         mov si, string
#         call rev_str
#         mov si, string2
#         call rev_str
#         jmp end


# rev_str:
#         xor cx, cx
#         mov cl, [si]
#         mov bx, si
#         mov dx, cx
# L1:
#         inc si
#         mov al, [si]
#         push ax 
#         loop L1

#         mov cx, dx
#         mov si, bx

# L2:
#         inc si
#         pop ax 
#         mov [si], al
#         loop L2
#         ret




# string:
#         db 4,"lion"

# string2:
#         db 5,"leway"




# end: 
#         nop

# """

def extract_label(string):
    current_label = ""
    last_label = ""
    labels = []
    b = 0
    lines = 1
    end = len(string) - 1
    s = ""
    index =-1
    count = 0
    if(end<1): return labels

    while(b<=end):
        i = ""
        i= str(string[b])
        if(i == ';'):
            while(i==';' or i != '\n'):
                b = b + 1

                if(b>end):
                    return labels
                i= str(string[b])


            
            
        if(i.isalnum() or i == '.' or i==':'):
            s += i
        l = len(s)
        if( l > 1):
            if(s[-1] == ':'):
                current_label = s[:-1]
                if(s[0]=='.' and (count > 0) ):
                    labels[index]["has_children"] = True
                    labels[index]["children"].append(
                        {
                            "name": last_label + current_label,
                            "has_children": False,
                            "line": lines,
                            "type": 0

                        }
                    )
                    s = ""
                else:
                    last_label = s[:-1]
                    labels.append({
                        "name": last_label,
                        "children": [],
                        "has_children": False,
                        "line": lines,
                        "type": 0
                    })
                    count += 1
                    index += 1
                    s = ""
            elif(s == "equ" or s == "db" or s == "dw" or s=="DB" or s=="DW" or s == "EQU"):
                if(index >= 0 and (labels[index]["type"]< 1)):
                    labels[index]["type"] = 1
                    pass
                pass
            

        
                    

        if(i=='\n' or (i.isspace())):
            s=""

        if(i == '\n'):
            lines += 1

            
            


        b = b + 1






    return labels


# print(extract_label(k))