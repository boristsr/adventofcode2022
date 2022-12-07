from typing import List,Dict, Tuple
import typing
import shlex

inputfile = open('day6/test.txt', 'r')
#inputfile = open('day6/input.txt', 'r')
Lines = inputfile.readlines()

def are_all_unique(message: str) -> bool:
    char_set = set()
    for char in message:
        char_set.add(char)
    
    if len(char_set) == 4:
        return True
    return False

def find_start(message: str) -> int:
    for i in range(4, len(message)):
        #print(f'range = {i-4}: {i}')
        message_slice = message[i-4:i]
        #print(f'{len(message_slice)}: {message_slice}')
        if are_all_unique(message_slice):
            return i
    return -1

for line in Lines:
    stripped_line = line.strip()
    if stripped_line == "":
        continue

    print(find_start(line))
