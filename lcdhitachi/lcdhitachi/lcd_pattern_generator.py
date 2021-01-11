

def get_drawn_pos(val=1):

        arr = [0, 0, 0, 0,0]
        v = val 
        prev = v
        v= val - 16
        if(v>=0):
                arr[0] = 1
                prev = v
                pass
        else:
                v= prev
                pass
        
        v = v - 8
        if(v>=0):
                arr[1] = 1
                prev = v
                pass
        else:
                v = prev  
        
        v = v - 4
        if(v>=0):
                arr[2] = 1
                prev = v
                pass
        else:
                v = prev  

        v = v - 2
        if(v>=0):
                arr[3] = 1
                prev = v
                pass
        else:
                v = prev  
        v = v - 1
        if(v>=0):
                arr[4] = 1
                pass
        else:
                v = val  
        return arr





# print(get_drawn_pos(17))
    



                      
class PatternGenerator():

        # 16 8 4 2 1
        
        char_patterns = [
        "4,4,4,4,0,0,4,0",  # !
        "10,10,10,0,0,0,0,0", # "
        "10,10,31,10,31,10,10", # #
        "4,15,20,14,5,30,4,0",  # $
        "24,25, 2,4,8,19,3,0",  # %
        "12,18,20,8,21,18,13",  # &
        "12,4,8",  # '
        "2,4,8,8,8,4,2",  # (
        "8,4,2,2,2,4,8",  # )
        "0,0,4,21,14,21,4",  # *
        "0,0,4,4,31,4,4",  # +
        "0,0,0,0,12,4,8",  # ,
        "0,0,0,31",  # -
        "0,0,0,0,0,12,12",  # .
        "0,1,2,4,8,16",
        # start 0 - 9 ANCHOR
        "14,17,19,21,25,17,14", # 0
        "4,12,4,4,4,4,14", # 1
        "14,17,1,2,4,8,31", # 2
        "31,2,4,2,1,17,14", # 3
        "2,6,10,18,31,2,2", # 4
        "31,16,30,1,1,17,14", # 5
        "6,8,16,30,17,17,14", # 6
        "31,17,1,2,4,4,4", # 7
        "14,17,17,14,17,17,14", # 8
        "14,17,17,15,1,2,12", # 9
        # end 0 - 9 ANCHOR
        "0,12,12,0,12,12", # :
        "0,12,12,0,12,4,8", # ;
        "2,4,8,16,8,4,2", # <
        "0,0,31,0,31", # =
        "8,4,2,1,2,4,8", # >
        "14,17,1,2,4,0,4", # ?
        "14,17,1,13,21,21,14", # @
        #  start A-Z ANCHOR
        "14,17,17,17,31,17,17", # A
        "30,17,17,30,17,17,30", # B
        "14,17,16,16,16,17,14", # C
        "28,18,17,17,17,18,28", # D
        "31,16,16,30,16,16,31", # E
        "31,16,16,30,16,16,16", # F
        "14,17,16,23,17,17,15", # G
        "17,17,17,31,17,17,17", # H
        "14,4,4,4,4,4,14", # I
        "7,2,2,2,2,18,12", # J
        "17,18,20,24,20,18,17", # K
        "16,16,16,16,16,16,31", # L
        "17,27,21,21,17,17,17", # M
        "17,17,25,21,19,17,17", # N
        "14,17,17,17,17,17,14", # O
        "30,17,17,30,16,16,16", # P
        "14,17,17,17,21,18,13", # Q
        "30,17,17,30,20,18,17", # R
        "15,16,16,14,1,1,30", # S
        "31,4,4,4,4,4,4", # T
        "17,17,17,17,17,17,14", # U
        "17,17,17,17,17,10,4", # V
        "17,17,17,21,21,21,10", # W
        "17,17,10,4,10,17,17", # X
        "17,17,17,10,4,4,4", # Y
        "31,1,2,4,8,16,31", # Z
        # End A - Z ANCHOR
        "28,16,16,16,16,16,28", # [
        "17,10,31,4,31,4,4", # Yen
        "14,2,2,2,2,2,14", # ]
        "4,10,17", # ^
        "0,0,0,0,0,0,31", # _
        "8,4,2", # `
        # start a - z  ANCHOR
        "0,0,14,1,15,17,15", # a
        "16,16,22,25,17,17,30", # b
        "0,0,14,16,16,17,14", # c
        "1,1,13,19,17,17,15", # d
        "0,0,14,17,31,16,14", # e
        "6,9,8,28,8,8,8", # f
        "0,15,17,17,15,1,14", # g
        "16,16,22,25,17,17,17", # h
        "4,0,12,4,4,4,14", # i
        "2,0,6,2,2,18,12", # j
        "16,16,18,20,24,20,18", # k
        "12,4,4,4,4,4,14", # l
        "0,0,26,21,21,17,17", # m
        "0,0,22,25,17,17,17", # n
        "0,0,14,17,17,17,14", # o
        "0,0,30,17,30,16,16", # p
        "0,0,13,19,15,1,1", # q
        "0,0,22,25,16,16,16", # r
        "0,0,14,16,14,1,30", # s
        "8,8,28,8,8,9,6", # t
        "0,0,17,17,17,19,13", # u
        "0,0,17,17,17,10,4", # v
        "0,0,17,21,21,21,10", # w
        "0,0,17,10,4,10,17", # x
        "0,0,17,17,15,1,14", # y
        "0,0,31,2,4,8,31", # z
        # end a - z
        "2,4,4,8,4,4,2", # {
        "4,4,4,4,4,4,4", # |
        "8,4,4,2,4,4,8", # }
        "0,0,0,0,0,0,0",# end
        ]
        @staticmethod
        def render_pattern_to_str(index=0):
                p=""
        
                ret=''

                try:
                        if(index > 92):
                                # print("not in scope")
                                p = PatternGenerator.char_patterns[93]
                        else:
                                p = PatternGenerator.char_patterns[index]
                        pass
                except IndexError as a:
                        for i in range(0, 8):
                                for v in range(0, 5):
                                        ret = ret + ('•')
                                        pass
                                ret = ret+'\n'
                        print(ret)                
                        print(a)
                        return
                
                
                
                p = p.strip()
                arr = p.split(',')
                                         
                arr_len = len(arr)

                for i in range(0, arr_len):
                        # print(i, arr[i])
                        v = int(arr[i])
                        # print(i, arr[i])

                        marr = get_drawn_pos(v)
                        for lion in range(0,5):
                                if(marr[lion]==1):
                                        ret = ret + ('•')
                                        pass
                                else:
                                        ret = ret+' '
                                        pass
                                pass
                        ret = ret+'\n'
                while (arr_len<7):
                        ret= ret+'\n'
                        arr_len+=1
                        pass
                for lion in range(0,5):
                        ret = ret + ('•')
                        pass
        
                print(ret)
        @staticmethod
        def render_pattern_to_matrix(index=0):
                """
                docstring
                """
                p=""
                ret=list()
                try:
                        if(index > 92):
                                # print("not in scope")
                                p = PatternGenerator.char_patterns[93]
                        else:
                                p = PatternGenerator.char_patterns[index]
                        pass
                except IndexError as a:
                        p = PatternGenerator.char_patterns[93]
                        pass

                p = p.strip()
                arr = p.split(',')
                                         
                arr_len = len(arr)
                for i in range(0, arr_len):
                        # print(i, arr[i])
                        v = int(arr[i])
                        m_arr = get_drawn_pos(v)
                        ret.append(m_arr)
                while (len(ret) < 7):
                        ret.append([0,0,0,0])
                return ret      



