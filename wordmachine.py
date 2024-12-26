
class LoopType:
    NORMAL = 'l'  
    WHILE = 'w'
    UNTIL = 'u'





def clamp(n, min, max): 
    if n < min: 
        return min
    elif n > max: 
        return max
    else: 
        return n 

class WordMachine:
    def stack_alert(self, name):
        if len(self.stack) <= 0:
            print(f"\nSTACK EMPTY, AT INSTRUCTION {name}")
            return True
        return False

    def __init__(self):
        self.tape = {0: 0}
        self.stack = []
        self.loop_stack = []
        self.pointer = 0
        self.running = False
        self.debug = False
        self.charmap = {
            'a': self.do_add,
            'b': self.do_back,
            'c': self.do_clear,
            'd': self.do_decrement,
            'e': self.do_end,
            'f': self.do_forward,
            'g': self.do_get,
            'h': self.do_head,
            'i': self.do_increment,
            'j': self.do_jump,
            'k': self.do_keep,
            'l': self.do_loop,
            'm': self.do_move,
            'n': self.do_negate,
            'o': self.do_output,
            'p': self.do_push,
            'q': self.do_qsquare,
            'r': self.do_rotate,
            's': self.do_subtract,
            't': self.do_times,
            'u': self.do_until,
            'v': self.do_value,
            'w': self.do_while,
            'x': self.do_xchange,
            'y': self.do_yield,
            'z': self.do_zero,   

        }
        pass
    
    def execute(self, code: str):
        i = 0
        self.running = True
        while i < len(code):
            if i < len(code) - 1 and code[i:i+2] == '//':
                while i < len(code) and code[i] != '\n':
                    i += 1
                continue
                
            if i < len(code) - 1 and code[i:i+2] == '/*':
                while i < len(code) - 1:
                    if code[i:i+2] == '*/':
                        i += 2
                        break
                    i += 1
                continue
            char = code[i].lower()  
            if char in self.charmap:
                if self.debug:
                    print("\n", self.stack, self.tape, self.pointer)
                self.charmap[char]()
            i += 1
            if not self.running:
                break


    def ensure_cell_exists(self, index):
        if index not in self.tape:
            self.tape[index] = 0

    def get_cell(self, index):
        return self.tape.get(index, 0) 

    def do_add(self):
        if self.stack_alert("ADD"): return
        self.tape[self.pointer] = self.stack.pop() + self.get_cell(self.pointer)
        
    def do_back(self):
        if self.pointer > 0:
            self.pointer -= 1

    def do_clear(self):
        self.tape[self.pointer] = 0

    def do_decrement(self):
        self.tape[self.pointer] = self.get_cell(self.pointer) - 1
        
    def do_end(self):
        if len(self.loop_stack) > 0:
            loop_type, pos, *extra = self.loop_stack[-1]
            
            if loop_type == LoopType.NORMAL:
                if self.get_cell(self.pointer) != 0:
                    return pos
            elif loop_type == LoopType.WHILE:
                if len(self.stack) > 0 and self.stack[-1] != 0:
                    return pos
            elif loop_type == LoopType.UNTIL:
                count = extra[0]
                if count > 1:
                    self.loop_stack[-1] = (loop_type, pos, count - 1)
                    return pos
                    
            self.loop_stack.pop() 

    def do_forward(self): #alias
        self.do_move()

    def do_get(self):
        if self.stack_alert("GET"): return
        self.stack.pop()

    def do_head(self):
        self.stack.append(self.pointer)

    def do_increment(self):
        self.tape[self.pointer] = self.get_cell(self.pointer) + 1

    def do_jump(self):
        if self.stack_alert("JUMP"): return
        self.pointer = self.stack.pop()

    def do_keep(self):
        if self.stack_alert("KEEP"): return
        self.tape[self.pointer] = self.stack.pop()
        
    def do_loop(self):
        self.loop_stack.append((LoopType.NORMAL, self.pointer))

    def do_move(self):
        self.pointer += 1

    def do_negate(self):
        if self.stack_alert("NEGATE"): return
        val = self.stack.pop()
        val *= -1
        self.stack.append(val)

    def do_output(self):
        print(self.get_cell(self.pointer), end='')

    def do_push(self):
        self.stack.append(self.get_cell(self.pointer))
    def do_qsquare(self):
        if self.stack_alert("SQUARE"): return
        val = self.stack.pop()
        val *= val
        self.stack.append(val)

    def do_rotate(self):
        if len(self.stack) >= 3:
            a = self.stack.pop()
            b = self.stack.pop()
            c = self.stack.pop()
            self.stack.append(b)
            self.stack.append(c)
            self.stack.append(a)

    def do_subtract(self):
        if self.stack_alert("SUBTRACT"): return
        self.tape[self.pointer] = self.get_cell(self.pointer) - self.stack.pop()

    def do_times(self):
        if self.stack_alert("TIMES"): return
        #print("\nHey", self.get_cell(self.pointer) * self.stack[-1], self.get_cell(self.pointer), self.stack[-1])
        self.tape[self.pointer] = self.get_cell(self.pointer) * self.stack.pop()

    def do_until(self):
        if self.stack_alert("UNTIL"): return
        count = self.stack.pop()
        self.loop_stack.append((LoopType.UNTIL, self.pointer, count))

    def do_value(self):
        if self.stack_alert("VALUE"): return
        self.stack.append(self.stack[-1])
    
    def do_while(self):
        if self.stack_alert("WHILE"): return
        if self.stack.pop() != 0:
            self.loop_stack.append((LoopType.WHILE, self.pointer))

    def do_xchange(self):
        if len(self.stack) >= 2:
            a = self.stack.pop()
            b = self.stack.pop()
            self.stack.append(b)
            self.stack.append(a)
    
    def do_yield(self):
        print(chr(clamp(self.get_cell(self.pointer), 0, 0x10ffff)), end='')

    def do_zero(self):
        self.stack.append(0)