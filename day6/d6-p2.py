from typing import List,Dict, Tuple
import typing
import shlex

#inputfile = open('day6/test.txt', 'r')
#inputfile = open('day6/test2.txt', 'r')
inputfile = open('day6/input.txt', 'r')
Lines = inputfile.readlines()

def are_all_unique(message: str) -> bool:
    char_set = set()
    for char in message:
        char_set.add(char)
    
    if len(char_set) == len(message):
        return True
    return False

def find_start(message: str, num_unique: int) -> int:
    for i in range(num_unique, len(message)):
        #print(f'range = {i-4}: {i}')
        message_slice = message[i-num_unique:i]
        #print(f'{len(message_slice)}: {message_slice}')
        if are_all_unique(message_slice):
            return i
    return -1

for line in Lines:
    stripped_line = line.strip()
    if stripped_line == "":
        continue

    print(find_start(line, 14))
