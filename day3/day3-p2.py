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

groups = []
current_group = []
for line in Lines:
    current_group.append(line.strip())
    if len(current_group) >= 3:
        groups.append(current_group)
        current_group = []

for group in groups:
    e1 = build_set(group[0])
    e2 = build_set(group[1])
    e3 = build_set(group[2])

    common_items = e1.intersection(e2).intersection(e3)
    for item in common_items:
        total_score += get_item_priority(item)
    
print(total_score)