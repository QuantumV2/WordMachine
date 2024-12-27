
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
        self.debug = True
        self.pc = 0
        self.program = ""
        self.initprogram = ""
        self.charmap = {
            'a': self.do_add,
            'b': self.do_back,
            'c': self.do_clear,
            'd': self.do_decrement,
            'e': self.do_end,
            'f': self.do_fif,
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
            'q': self.do_query,
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
    
    def execute(self, code):
        while self.pc < len(code):

            if self.pc < len(code) - 1 and code[self.pc:self.pc+2] == '//':
                while self.pc < len(code) and code[self.pc] != '\n':
                    self.pc += 1
                continue
                
            if self.pc < len(code) - 1 and code[self.pc:self.pc+2] == '/*':
                while self.pc < len(code) - 1:
                    if code[self.pc:self.pc+2] == '*/':
                        self.pc += 2
                        break
                    self.pc += 1
                continue
            char = code[self.pc]  
            if char.isascii():
                char = char.lower()
            #print(char)
            if char in self.charmap:
                #print("\n", self.stack, self.tape, self.pointer, self.pc, char)
                self.charmap[char]()
            self.pc += 1

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
       pass

    def do_fif(self):
        end_pos = self._find_matching_end( self.pc + 1)
        loop_code = self.program[self.pc + 1:end_pos]
        if self.stack and self.stack.pop() != 0:
            self.pc = 0
            self.execute(loop_code)
        self.pc = end_pos

    def do_get(self):
        if self.stack_alert("GET"): return
        self.stack.pop()

    def do_head(self):
        self.stack.append(self.pointer)

    def do_increment(self):
        self.tape[self.pointer] = self.get_cell(self.pointer) + 1

    def do_jump(self):
        if self.stack_alert("JUMP"): return
        location = self.stack.pop()
        if location >= 0:
            self.pointer = location
        else:
            print("\nAttempt to jump to invalid location")

    def do_keep(self):
        if self.stack_alert("KEEP"): return
        self.tape[self.pointer] = self.stack.pop()
        
    def do_loop(self):
        end_pos = self._find_matching_end(self.pc + 1)
        loop_code = self.program[self.pc + 1:end_pos]
        while self.get_cell(self.pointer) != 0:
            self.pc = 0
            self.program = loop_code
            self.execute(self.program)
            self.program = self.initprogram
        self.pc = end_pos  
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

    def do_query(self):
        if self.stack_alert("QUERY"): return
        location = self.stack.pop()
        if location >= 0:
            self.tape[self.pointer] = self.tape[location]
        else:
            print("\nAttempting to query negative location")


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
        end_pos = self._find_matching_end(self.pc + 1)
        loop_code = self.program[self.pc + 1:end_pos]
        if self.stack:
            count = self.stack.pop()
            self.pc = 0
            self.program = loop_code*count
            self.execute(self.program)
            self.program = self.initprogram
        self.pc = end_pos

    def do_value(self):
        if self.stack_alert("VALUE"): return
        self.stack.append(self.stack[-1])
    
    def do_while(self):
        end_pos = self._find_matching_end( self.pc + 1)
        loop_code = self.program[self.pc + 1:end_pos]
        while self.stack and self.stack.pop() != 0:
            self.pc = 0
            self.program = loop_code
            self.execute(self.program)
            self.program = self.initprogram
        self.pc = end_pos
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

    def _find_matching_end(self, start):

        program = self.program
        nesting = 1
        pos = start
        while pos < len(program):
            if program[pos] in 'lwu': 
                nesting += 1
            elif program[pos] == 'e':
                nesting -= 1
                if nesting == 0:
                    return pos
            pos += 1
        return len(program) 