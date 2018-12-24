import sys
import numpy as np

with open(sys.argv[1]) as f:
    line = f.readline().strip()

def reduce(string):
    length = len(string) - 1
    i = 0
    while i < length:
        if string[i] == string[i+1].swapcase():
            string = string[:i] + string[i+2:]
            length -= 2
        else:
            i += 1
    return(string)

def full_reduce(string):
    old = string
    new = reduce(string)
    while old != new:
        old, new = new, reduce(new)
    return old

print(len(full_reduce(line)))

def remove_char(string, c):
    i = 0
    while i < len(string):
        if string[i] == c or string[i].swapcase() == c:
            string = string[:i] + string[i+1:]
        else:
            i += 1
    return string


min_reduction = len(line)
for c in range(ord('a'),ord('z')):
    reduced_length = len(full_reduce(remove_char(line, chr(c))))
    if reduced_length < min_reduction:
        min_reduction = reduced_length
    print(chr(c))

print(min_reduction)
