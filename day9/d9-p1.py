from typing import List, Tuple, Optional, Set
from os.path import join
import shlex

RIGHT = "R"
LEFT = "L"
DOWN = "D"
UP = "U"

#inputfile = open('day9/test.txt', 'r')
inputfile = open('day9/input.txt', 'r')
Lines = inputfile.readlines()

# (x,y) positions
head_position: List[int] = [0,0]
tail_position: List[int] = [0,0]
tail_positions: Set[Tuple[int,int]] = set()
tail_positions.add(tuple(tail_position))

def update_tail():
    x_diff = head_position[0] - tail_position[0]
    y_diff = head_position[1] - tail_position[1]
    if abs(x_diff) >= 2 or abs(y_diff) >= 2:
        x_move = min(abs(x_diff), 1)
        if x_diff < 0:
            x_move *= -1
        y_move = min(abs(y_diff), 1)
        if y_diff < 0:
            y_move *= -1
        tail_position[0] += x_move
        tail_position[1] += y_move
    print(f'H: {tuple(head_position)} T: {tuple(tail_position)}')
    tail_positions.add(tuple(tail_position))

# my instinct is that there is some speedup to be had by taking the math shortcut of just counting the difference between start and end position
# - but my counter-instinct says there will still be a similar cost in tracking and evaluating moves to check for cells that were occupied twice
# - This cost could be somewhat mitigated by then counting line intersections, but that's a whole extra step that I couldn't be bothered writing
# so, as with the rest of the challenges, I'm taking the dumb brute force approach
def move_head(direction: str):
    if direction == RIGHT:
        head_position[0] += 1
    if direction == LEFT:
        head_position[0] -= 1
    if direction == UP:
        head_position[1] += 1
    if direction == DOWN:
        head_position[1] -= 1
    update_tail()

for line in Lines:
    print(line.strip())
    line_symbols = shlex.split(line.strip())
    move_dir = line_symbols[0]
    move_count = int(line_symbols[1])
    while move_count > 0:
        move_count -= 1
        move_head(move_dir)


print(len(tail_positions))
