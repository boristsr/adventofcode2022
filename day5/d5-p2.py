from typing import List,Dict, Tuple
import typing
import shlex

#inputfile = open('day5/test.txt', 'r')
inputfile = open('day5/input.txt', 'r')
Lines = inputfile.readlines()

num_stacks = len(Lines[0][:]) // 4

stacks: List[List[str]] = []
for i in range(num_stacks):
    stacks.append([])

def read_stack_state(line: str, stack_index: int):
    character_index = stack_index * 4 + 1
    contents = line[character_index]
    return contents

bReachedEndOfStacks = False

while bReachedEndOfStacks == False:
    curr_line = Lines.pop(0)[:-1]
    print(curr_line)
    if len(curr_line) > 0 and curr_line[1] == "1":
        bReachedEndOfStacks = True
        continue

    for i in range(num_stacks):
        stack_contents = read_stack_state(curr_line, i)
        if stack_contents != " ":
            stacks[i].insert(0, stack_contents)

for i in range(num_stacks):
    line = str(i) + ":"
    for j in range(len(stacks[i])):
        line += " " + stacks[i][j]
    print(line)

Lines.pop(0)

for line in Lines:
    print(line.strip())
    line_values = shlex.split(line.strip())
    num_moves = int(line_values[1])
    src_stack_idx = int(line_values[3])-1
    dst_stack_idx = int(line_values[5])-1

    move_stack = stacks[src_stack_idx][-num_moves:]
    stacks[src_stack_idx] = stacks[src_stack_idx][:-num_moves]
    stacks[dst_stack_idx].extend(move_stack)

final_stack_string = ""
for stack_index in range(num_stacks):
    final_stack_string = final_stack_string + stacks[stack_index][-1]

print(final_stack_string)