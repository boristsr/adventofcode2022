from typing import List, Tuple, Optional, Set
from os.path import join
import shlex

RIGHT = "R"
LEFT = "L"
DOWN = "D"
UP = "U"

NUM_KNOTS = 10

inputfile = open('day9/test2.txt', 'r')
inputfile = open('day9/input.txt', 'r')
Lines = inputfile.readlines()

# (x,y) positions
knot_positions: List[List[int]] = []
for i in range(NUM_KNOTS):
    knot_positions.append([0,0])
tail_visited_positions: Set[Tuple[int,int]] = set()
#tail_visited_positions.add(tuple(tail_position))

def update_knot(forward_knot: List[int], current_knot: List[int]) -> bool:
    x_diff = forward_knot[0] - current_knot[0]
    y_diff = forward_knot[1] - current_knot[1]
    if abs(x_diff) >= 2 or abs(y_diff) >= 2:
        x_move = min(abs(x_diff), 1)
        if x_diff < 0:
            x_move *= -1
        y_move = min(abs(y_diff), 1)
        if y_diff < 0:
            y_move *= -1
        current_knot[0] += x_move
        current_knot[1] += y_move
        return True
    return False

def move_head(direction: str):
    head_knot = knot_positions[0]
    if direction == RIGHT:
        head_knot[0] += 1
    if direction == LEFT:
        head_knot[0] -= 1
    if direction == UP:
        head_knot[1] += 1
    if direction == DOWN:
        head_knot[1] -= 1
    for i in range(1, len(knot_positions)):
        updated = update_knot(knot_positions[i-1], knot_positions[i])
        if updated == False:
            break
    tail_visited_positions.add(tuple(knot_positions[NUM_KNOTS-1]))

for line in Lines:
    print(line.strip())
    line_symbols = shlex.split(line.strip())
    move_dir = line_symbols[0]
    move_count = int(line_symbols[1])
    while move_count > 0:
        move_count -= 1
        move_head(move_dir)


print(len(tail_visited_positions))
