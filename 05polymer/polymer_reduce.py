import sys
import numpy as np

with open(sys.argv[1]) as f:
    line = f.readline().strip()

def reduce(string):
    for i in range(len(string)-1):
        if string[i] == string[i+1].swapcase():
            string = string[:i] + string[i+2:]
            break
    return(string)

def full_reduce(string):
    old = string
    new = reduce(string)
    while old != new:
        old, new = new, reduce(new)
    return old

print(len(full_reduce(line)))
