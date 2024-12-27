import wordmachine
import sys
import os
import importlib
from importlib import util

machine = wordmachine.WordMachine()
machine.debug = False


PLUGINS_ENABLED = True

content = ""

with open(sys.argv[1], "r", encoding='utf-8') as f:
    content = f.read()

machine.program = content
machine.initprogram = content

def load_plugins():
    if not os.path.exists("plugins"):
        os.makedirs("plugins") 
        
    for file in os.listdir("plugins"):
        if file.endswith(".py"):
            try:
                spec = importlib.util.spec_from_file_location(file[:-3], f"plugins/{file}")
                plugin = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(plugin)
                
                if hasattr(plugin, "plugin_init"):
                    plugin.plugin_init(machine)
                    
            except Exception as e:
                print(f"Failed to load plugin {file}: {e}")

if PLUGINS_ENABLED:
    load_plugins()
#print(machine.charmap)
machine.execute(machine.program)