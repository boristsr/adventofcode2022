from typing import List, Tuple, Optional, Set, Dict
from os.path import join
import shlex
import math

inputfile = open('day11/input.txt', 'r')
#inputfile = open('day11/test.txt', 'r')
Lines = inputfile.readlines()

class Monkey():
    def __init__(self) -> None:
        self.lines: List[str] = []
        self.line_syms: List[List[str]] = []
        self.items: List[int] = []
        self.operation: List[str] = []
        self.test_op: List[str] = []
        self.true_dst: int = -1
        self.false_dst: int = -1
        self.inspection_count = 0
    
    def print_monkey(self):
        for line in self.lines:
            print(f'\t{line.strip()}')
        
        print(self.id)
        print(self.items)
        print(self.operation)
        print(self.test_op)
        print(self.true_dst)
        print(self.false_dst)

    def print_items(self):
        item_str = ""
        for item in self.items:
            item_str += str(item) + ", "
        print(f'{self.id}: {item_str}')
    
    def setup(self):
        for line in self.lines:
            self.line_syms.append(shlex.split(line.strip().replace(":", "").replace(",","")))

        self.id = int(self.line_syms[0][1])
        self.items = [int(x) for x in self.line_syms[1][2:]]
        self.operation = self.line_syms[2][3:]
        self.test_op = self.line_syms[3][1:]
        self.true_dst = int(self.line_syms[4][-1])
        self.false_dst = int(self.line_syms[5][-1])

    def get_operand(self, item, operand_val):
        operand = None
        if operand_val == "old":
            operand = item
        else:
            operand = int(operand_val)
        return operand

    def inspect(self, item):
        self.inspection_count += 1
        operand_a = self.get_operand(item, self.operation[0])
        operand_b = self.get_operand(item, self.operation[2])
        op_result = 0
        if self.operation[1] == "+":
            op_result = operand_a + operand_b
        elif self.operation[1] == "*":
            op_result = operand_a * operand_b
        elif self.operation[1] == "/":
            op_result = operand_a / operand_b
        elif self.operation[1] == "-":
            op_result = operand_a - operand_b
        
        return op_result
        
    def test(self, item):
        if self.test_op[0] == "divisible":
            divisible = item % int(self.test_op[-1])
            return divisible == 0
        print("UNKNOWN TEST")
        return True

    def throw_item(self, item, test_result, monkeys):
        dst_monkey = self.true_dst
        if test_result == False:
            dst_monkey = self.false_dst
        monkeys[dst_monkey].catch_item(item)

    def catch_item(self, item):
        self.items.append(item)

    def process_items(self, monkeys: List[Optional['Monkey']], lcm):
        while len(self.items) > 0:
            item = self.items.pop(0)
            #inspect (operation)
            new_item = self.inspect(item)
            #reduce worry level (floor(worry/3))
            new_item = new_item % lcm
            #new_item = new_item / 3
            #test
            test_result = self.test(new_item)
            #throw
            self.throw_item(new_item, test_result, monkeys)

monkeys: List[Monkey] = []

while len(Lines) > 0:
    nm = Monkey()
    nm.lines = Lines[:6]
    nm.setup()
    monkeys.append(nm)
    Lines = Lines[7:]

lcm_factors = []
for m in monkeys:
    lcm_factors.append(int(m.test_op[-1]))

lcm = math.lcm(*lcm_factors)

NUM_ROUNDS = 10000

def run_rounds(rounds):
    for i in range(rounds):
        for m in monkeys:
            m.process_items(monkeys, lcm)

    inspection_counts = []

    for m in monkeys:
        inspection_counts.append(m.inspection_count)

    inspection_counts.sort()
    print(inspection_counts)

    monkey_business = inspection_counts[-1] * inspection_counts[-2]

    print(monkey_business)

run_rounds(NUM_ROUNDS)

exit()

import cProfile
import re
cProfile.run(f'run_rounds({NUM_ROUNDS})')