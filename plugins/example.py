def plugin_init(wordmachine):
    def star(self):
        print("test")
    
    setattr(wordmachine.__class__, 'star', star)
    
    wordmachine.charmap['⋆'] = wordmachine.star