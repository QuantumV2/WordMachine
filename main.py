import wordmachine
import sys

machine = wordmachine.WordMachine()
machine.debug = False

content = ""
with open(sys.argv[1], "r") as f:
    content = f.read()
machine.execute(content)