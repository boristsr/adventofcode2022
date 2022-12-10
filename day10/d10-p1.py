from typing import List, Tuple, Optional, Set, Dict
from os.path import join
import shlex

#inputfile = open('day10/test.txt', 'r')
#inputfile = open('day10/test-small.txt', 'r')
inputfile = open('day10/input.txt', 'r')
Lines = inputfile.readlines()

class Processor:
    instruction_cost: Dict[str, int] = {
        "addx": 2,
        "noop": 1
    }

    def __init__(self) -> None:
        self.register_x: int = 1
        self.instructions: List[Tuple[str,Optional[int]]] = []
        self.current_op: Tuple[str,Optional[int]] = ("noop",0)
        self.current_op_cycles_remaining: int = 0
        self.cycle_count = 0
        self.signal_strength = 0

    def execute_op(self):
        if self.current_op[0] == "addx":
            #print(f'executing op: {self.current_op[0]}, arg: {self.current_op[1]}')
            self.register_x += self.current_op[1]
        if self.current_op[0] == "noop":
            #print(f'executing op: {self.current_op[0]}')
            pass

    def tick_processor(self):
        #self.print_state()
        self.update_signal_strength()
        if self.current_op_cycles_remaining > 0:
            self.current_op_cycles_remaining -= 1
        if self.current_op_cycles_remaining == 0:
            self.execute_op()
        self.cycle_count += 1
    
    def print_state(self):
        print(f'Cycle: {self.cycle_count}, op: {self.current_op[0]}, register_x: {self.register_x}')

    def update_signal_strength(self):
        if self.cycle_count == 19:
            print("UPDATING SIGNAL")
            self.print_state()
            self.signal_strength = (self.cycle_count + 1) * self.register_x
            print(self.signal_strength)
        elif (self.cycle_count - 19) % 40 == 0:
            print("UPDATING SIGNAL")
            self.print_state()
            self.signal_strength += (self.cycle_count + 1) * self.register_x
            print(self.signal_strength)

    def tick_processor_till_complete(self):
        while self.current_op_cycles_remaining > 0 or len(self.instructions) > 0:
            if self.current_op_cycles_remaining == 0 and len(self.instructions) > 0:
                self.current_op = self.instructions.pop(0)
                self.current_op_cycles_remaining = Processor.instruction_cost[self.current_op[0]]
            self.tick_processor()

cpu = Processor()

for line in Lines:
    line_symbols = shlex.split(line.strip())
    new_instruction = [line_symbols[0]]
    if line_symbols[0] == "addx":
        new_instruction.append(int(line_symbols[1]))
    cpu.instructions.append(tuple(new_instruction))

cpu.tick_processor_till_complete()

print(cpu.cycle_count)
cpu.print_state()
