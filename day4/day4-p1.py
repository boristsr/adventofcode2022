from typing import List,Dict, Tuple
import typing

def range_contains_range(range_a: Tuple[int, ...], range_b: Tuple[int, ...]) -> bool:
    if range_a[0] <= range_b[0] and range_a[1] >= range_b[1]:
        return True

    if range_b[0] <= range_a[0] and range_b[1] >= range_a[1]:
        return True
    return False

#inputfile = open('day4/test.txt', 'r')
inputfile = open('day4/input.txt', 'r')
Lines = inputfile.readlines()

pairs: List[List[Tuple[int, ...]]] = []

for line in Lines:
    stripped_line = line.strip()
    sides = stripped_line.split(",")
    left: Tuple[int, ...] = tuple([int(x) for x in sides[0].split("-")])
    right: Tuple[int, ...] = tuple([int(x) for x in sides[1].split("-")])
    pairs.append([left, right])

total_count = 0

for pair in pairs:
    if range_contains_range(pair[0], pair[1]) == True:
        total_count += 1
    
print(str(total_count))