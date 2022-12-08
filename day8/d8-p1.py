from typing import List, Tuple, Optional
from os.path import join
import shlex

#inputfile = open('day8/test.txt', 'r')
inputfile = open('day8/input.txt', 'r')
Lines = inputfile.readlines()

rows: List[List[int]] = []

for line in Lines:
    stripped_line = line.strip()
    new_row: List[int] = []
    for char in stripped_line:
        new_row.append(int(char))
    
    rows.append(new_row)

size_x = len(rows[0])
size_y = len(rows)

#Immediately calculate the outside walls
total_visible = (size_x-1 + size_y-1) * 2

def check_visible(column_idx: int, row_idx: int) -> bool:
    my_height = rows[row_idx][column_idx]
    #check up
    bVisibleUp = True
    for y_minus in range(row_idx):
        new_y = row_idx-(y_minus + 1)
        if rows[new_y][column_idx] >= my_height:
            bVisibleUp = False
    #check down
    bVisibleDown = True
    for y in range(1, size_y - row_idx):
        new_y = row_idx + y
        if rows[new_y][column_idx] >= my_height:
            bVisibleDown = False
    #check left
    bVisibleLeft = True
    for x_minus in range(column_idx):
        new_x = column_idx-(x_minus + 1)
        if rows[row_idx][new_x] >= my_height:
            bVisibleLeft = False
    #check right
    #print(f'Checking right for {column_idx},{row_idx}')
    #print(f'{new_x}')
    bVisibleRight = True
    for x in range(1, size_x - column_idx):
        new_x = column_idx + x
        if rows[row_idx][new_x] >= my_height:
            bVisibleRight = False

    return bVisibleUp or bVisibleDown or bVisibleLeft or bVisibleRight

def print_visibility():
    for y in range(size_y):
        if y == 0 or y == size_y - 1:
            print(["x"]*size_x)
        else:
            line = ["x"]
            for x in range(1, size_x-1):
                if check_visible(x, y) == True:
                    line.append("x")
                else:
                    line.append(" ")
            line.append("x")
            print(line)


#only iterate through the internal cells
for y in range(1, size_y-1):
    for x in range(1, size_x-1):
        #print(f'{x},{y}')
        if check_visible(x, y) == True:
            total_visible += 1

print(f'{size_x},{size_y}')

print(total_visible)