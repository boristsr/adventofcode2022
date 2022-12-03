from typing import List,Dict
import typing

def get_item_priority(item: str) -> int:
    item_code = ord(item)
    #a = 97, z = 122
    if item_code >= 97 and item_code <= 122:
        return item_code - 96
    #A = 65, Z = 90
    if item_code >= 65 and item_code <= 90:
        return item_code - 64 + 26
    return 0

def build_set(items: str) -> typing.Set[int]:
    new_set: typing.Set[str] = set()
    for item in items:
        item_priority = get_item_priority(item)
        new_set.add(item)

    return new_set

#inputfile = open('day3/test.txt', 'r')
inputfile = open('day3/input.txt', 'r')
Lines = inputfile.readlines()

total_score = 0

for line in Lines:
    stripped_line = line.strip()
    num_items_per_compartment = len(stripped_line) // 2
    left_compartment = stripped_line[:num_items_per_compartment]
    right_compartment = stripped_line[num_items_per_compartment:]
    left_set = build_set(left_compartment)
    right_set = build_set(right_compartment)

    common_items = left_set.intersection(right_set)
    for item in common_items:
        total_score += get_item_priority(item)
    #print(f'{len(left_compartment)} : {len(right_compartment)}')
    
print(total_score)