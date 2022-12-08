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

def calculate_visibility_score(column_idx: int, row_idx: int) -> int:
    my_height = rows[row_idx][column_idx]
    #check up
    num_vis_up = 0
    for y_minus in range(row_idx):
        new_y = row_idx-(y_minus + 1)
        num_vis_up += 1
        if rows[new_y][column_idx] >= my_height:
            break
    #check down
    num_vis_down = 0
    for y in range(1, size_y - row_idx):
        new_y = row_idx + y
        num_vis_down += 1
        if rows[new_y][column_idx] >= my_height:
            break
    #check left
    num_vis_left = 0
    for x_minus in range(column_idx):
        new_x = column_idx-(x_minus + 1)
        num_vis_left += 1
        if rows[row_idx][new_x] >= my_height:
            break
    #check right
    #print(f'Checking right for {column_idx},{row_idx}')
    #print(f'{new_x}')
    num_vis_right = 0
    for x in range(1, size_x - column_idx):
        new_x = column_idx + x
        num_vis_right += 1
        if rows[row_idx][new_x] >= my_height:
            break

    return num_vis_right * num_vis_left * num_vis_down * num_vis_up

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

max_vis_score = 0

#only iterate through the internal cells
for y in range(1, size_y-1):
    for x in range(1, size_x-1):
        #print(f'{x},{y}')
        curr_vis_score = calculate_visibility_score(x, y)
        if curr_vis_score > max_vis_score:
            max_vis_score = curr_vis_score

print(f'{size_x},{size_y}')

print(max_vis_score)