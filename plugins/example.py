def plugin_init(wordmachine):
    #print("hi")
    def star(self):
        print("test")
    
    # Add the method to WordMachine instance
    setattr(wordmachine.__class__, 'star', star)
    
    # Map symbol to the new method
    wordmachine.charmap['⋆'] = wordmachine.star