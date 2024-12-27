# Word Machine 

## Overview

Word Machine is a programming language that operates on an infinite tape and a stack. Each instruction is a single character that performs operations like moving the tape pointer, manipulating stack values, and basic arithmetic.


### Instructions:
a - add: Pop a value from the stack, add it to the current cell on the tape

b - back: Move tape pointer left one cell

c - clear: Set current tape cell to 0

d - decrement: Decrease current tape cell by 1

e - end: End a loop

f - if: Pop a value from the stack, if it's not 0, then run the code between itself and the end instruction

g - get: Pop a value from the stack

h - head: Push the current pointer location to the stack

i - increment: Increase current tape cell by 1

j - jump: Pop a value from the stack and put the pointer there

k - keep: Pop value from stack and store in current tape cell

l - loop: Start loop, repeat if current cell is non-zero

m - move: Move tape pointer right one cell

n - negate: Multiply top stack value by -1

o - output: Output value at current tape position as a number

p - push: Push current cell value onto stack

q - query: Pop a position from the stack, then get the value of the given cell pos and set the current cell to that value

r - rotate: Rotate top 3 stack values (abc -> cab)

s - subtract: Same as add, but subtraction instead

t -  times: Same as add, but multiply

u - until: Pop value N, repeat loop N times

v - value: Duplicate top stack value

w - while: Start while loop if top of stack is non-zero, pops the stack each iteration

x - exchange: Swap top two stack values

y - yield: Output current cell value as a unicode character

z - zero: Push 0 onto stack
