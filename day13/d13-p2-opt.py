from typing import List, Tuple, Optional, Set, Dict
from os.path import join
import shlex
import math
import functools
import json

inputfile = open('day13/input.txt', 'r')
#inputfile = open('day13/test.txt', 'r')
Lines = inputfile.readlines()

pairs = []

def get_pairs(Lines):
    new_pairs = []
    while len(Lines) >= 2:
        line_a = Lines.pop(0).strip()
        line_b = Lines.pop(0).strip()
        #discard new line
        if len(Lines) > 0:
            Lines.pop(0)
        line_a_json = "{" + f'"data":{line_a}' + "}"
        line_b_json = "{" + f'"data":{line_b}' + "}"
        line_a_decoded = json.loads(line_a_json)["data"]
        line_b_decoded = json.loads(line_b_json)["data"]
        new_pair = [line_a_decoded, line_b_decoded]
        new_pairs.append(new_pair)
    
    return new_pairs

IN_ORDER = -1
OUT_ORDER = 1
CONTINUE_COMPARE = 0

def compare_items(item_a, item_b):
    #check pure ints
    if isinstance(item_a, int) and isinstance(item_b, int):
        if item_a < item_b:
            return IN_ORDER
        if item_a > item_b:
            return OUT_ORDER
    #check 2 arrays
    elif isinstance(item_a, list) and isinstance(item_b, list):
        result = compare_lists(item_a, item_b)
        if result != CONTINUE_COMPARE:
            return result
    #check array and single int
    else:
        it_a = item_a
        it_b = item_b
        if isinstance(item_a, int):
            it_a = [item_a]
        if isinstance(item_b, int):
            it_b = [item_b]
        result = compare_lists(it_a, it_b)
        if result != CONTINUE_COMPARE:
            return result

    return CONTINUE_COMPARE

def compare_lists(list_a, list_b):
    num_compares = min(len(list_a), len(list_b))
    
    for i in range(num_compares):
        item_a = list_a[i]
        item_b = list_b[i]
        result = compare_items(item_a, item_b)
        if result != CONTINUE_COMPARE:
            return result

    if len(list_a) < len(list_b):
        return IN_ORDER
    if len(list_a) > len(list_b):
        return OUT_ORDER

    return CONTINUE_COMPARE

pairs = get_pairs(Lines)
#insert divider packets
divider_a = [[2]]
divider_b = [[6]]

big_list = []
for pair in pairs:
    big_list.extend(pair)

#add all elements less than [[2]]
da_idx = sum(compare_lists(p, [[2]]) < 0 for p in big_list)
#Add all elements less than [[6]] + 1 for the first divider
db_idx = sum(compare_lists(p, [[6]]) < 0 for p in big_list) + 1

print((da_idx + 1) * (db_idx + 1))
