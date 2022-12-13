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
    
pairs = get_pairs(Lines)

IN_ORDER = 0
OUT_ORDER = 1
CONTINUE_COMPARE = 2

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
    while len(list_a) > 0 and len(list_b) > 0:
        item_a = list_a.pop(0)
        item_b = list_b.pop(0)
        result = compare_items(item_a, item_b)
        if result != CONTINUE_COMPARE:
            return result

    if len(list_a) == 0 and len(list_b) > 0:
        return IN_ORDER
    if len(list_a) > 0 and len(list_b) == 0:
        return OUT_ORDER

    return CONTINUE_COMPARE

correct_order_count = 0
correct_sum = 0
for i, pair in enumerate(pairs):
    if compare_lists(pair[0],pair[1]) == IN_ORDER:
        correct_order_count += 1
        correct_sum += i + 1

print(correct_order_count)
print(correct_sum)

