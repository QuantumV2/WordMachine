import math
import random

def plugin_init(wordmachine):

    def rng(self):
        max_val = self.stack.pop()
        self.stack.append(random.randint(0, max_val))
    
    def rand_float(self):
        self.stack.append(int(random.random() * 100))  
    

    def sine(self):
        x = self.stack.pop()
        result = int(math.sin(x * math.pi / 180) * 100)
        self.stack.append(result)
    
    def cosine(self):
        x = self.stack.pop()
        result = int(math.cos(x * math.pi / 180) * 100)
        self.stack.append(result)
    

    def power(self):
        exponent = self.stack.pop()
        base = self.stack.pop()
        self.stack.append(int(math.pow(base, exponent)))
    
    def sqrt(self):
        x = self.stack.pop()
        self.stack.append(int(math.sqrt(x)))

    def pi(self):
        self.stack.append(int(math.pi * 100))
    
    def e(self):
        self.stack.append(int(math.e * 100))
    

    def abs_val(self):
        x = self.stack.pop()
        self.stack.append(abs(x))
    
    def min_val(self):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(min(a, b))
    
    def max_val(self):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(max(a, b))


    setattr(wordmachine.__class__, 'rng', rng)
    setattr(wordmachine.__class__, 'rand_float', rand_float)
    setattr(wordmachine.__class__, 'sine', sine)
    setattr(wordmachine.__class__, 'cosine', cosine)
    setattr(wordmachine.__class__, 'power', power)
    setattr(wordmachine.__class__, 'sqrt', sqrt)
    setattr(wordmachine.__class__, 'pi', pi)
    setattr(wordmachine.__class__, 'e', e)
    setattr(wordmachine.__class__, 'abs', abs_val)
    setattr(wordmachine.__class__, 'min', min_val)
    setattr(wordmachine.__class__, 'max', max_val)

    wordmachine.charmap['∂'] = wordmachine.rng      # Random int
    wordmachine.charmap['∑'] = wordmachine.rand_float # Random float
    wordmachine.charmap['∫'] = wordmachine.sine     # Sine
    wordmachine.charmap['∮'] = wordmachine.cosine   # Cosine
    wordmachine.charmap['√'] = wordmachine.sqrt     # Square root
    wordmachine.charmap['∏'] = wordmachine.power    # Power
    wordmachine.charmap['π'] = wordmachine.pi       # Pi constant
    wordmachine.charmap['ℯ'] = wordmachine.e        # E constant
    wordmachine.charmap['|'] = wordmachine.abs      # Absolute value
    wordmachine.charmap['↓'] = wordmachine.min      # Minimum
    wordmachine.charmap['↑'] = wordmachine.max      # Maximum