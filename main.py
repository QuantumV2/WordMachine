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

    def walk_and_load(directory):
        for item in os.scandir(directory):
            if item.is_file() and item.name.endswith(".py"):
                try:
                    
                    rel_path = os.path.relpath(item.path, "plugins")
                    module_name = os.path.splitext(rel_path.replace(os.sep, "."))[0]
                    
                    spec = importlib.util.spec_from_file_location(module_name, item.path)
                    plugin = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(plugin)

                    if hasattr(plugin, "plugin_init"):
                        plugin.plugin_init(machine)

                except Exception as e:
                    print(f"Failed to load plugin {item.path}: {e}")
            
            elif item.is_dir() and not item.name.startswith("."):
                walk_and_load(item.path)

    walk_and_load("plugins")

if PLUGINS_ENABLED:
    load_plugins()
#print(machine.charmap)
machine.execute(machine.program)