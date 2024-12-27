def plugin_init(wordmachine):
    def parse_string(self):
        string = ""
        self.pc += 1
        while self.pc < len(self.program) and self.program[self.pc] != '"':
            string += self.program[self.pc]
            self.pc += 1
        
        for char in string[::-1]:
            self.stack.append(ord(char))
            
        self.pc += 1
    
    def parse_number(self):
        num = ""
        self.pc += 1
        
        while self.pc < len(self.program) and self.program[self.pc].isdigit() or self.program[self.pc] == '-':
            num += self.program[self.pc]
            self.pc += 1
        print(num)
        self.stack.append(int(num))

    setattr(wordmachine.__class__, 'parse_string', parse_string)
    setattr(wordmachine.__class__, 'parse_number', parse_number)
    wordmachine.charmap['"'] = wordmachine.parse_string
    wordmachine.charmap['#'] = wordmachine.parse_number