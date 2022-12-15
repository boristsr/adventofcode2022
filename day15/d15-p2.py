from typing import List, Tuple, Optional, Set, Dict
from os.path import join
import shlex
import math

inputfile = open('day15/input.txt', 'r')
height = 2000000
max_dimension = 4000000
test = False
if test:
    inputfile = open('day15/test.txt', 'r')
    height = 10
    max_dimension = 20
Lines = inputfile.readlines()

class Sensor:
    def __init__(self, pos: Tuple[int,int] = (0,0), nearest_beacon: Tuple[int,int] = (0,0)) -> None:
        self.pos: Tuple[int,int] = pos
        self.nearest_beacon: Tuple[int,int] = nearest_beacon
        self.distance = self.get_manhattan_distance()

    def get_manhattan_distance(self):
        return abs(self.pos[0] - self.nearest_beacon[0]) + abs(self.pos[1] - self.nearest_beacon[1])

in_sensors: List[Sensor] = []

for line in Lines:
    location_strs = line.strip().split(":")
    sensor_syms = location_strs[0].strip().replace(",","").split(" ")
    sensor_x = int(sensor_syms[2].split("=")[1])
    sensor_y = int(sensor_syms[3].split("=")[1])
    sensor_pos = (sensor_x, sensor_y)

    beacon_syms = location_strs[1].strip().replace(",","").split(" ")
    beacon_x = int(beacon_syms[4].split("=")[1])
    beacon_y = int(beacon_syms[5].split("=")[1])
    beacon_pos = (beacon_x, beacon_y)

    in_sensors.append(Sensor(sensor_pos, beacon_pos))
    print(f'Sensor: {sensor_pos} beacon: {beacon_pos}')

def range_overlaps(range_a: Tuple[int, ...], range_b: Tuple[int, ...]) -> bool:
    #Range b starts within range a
    if range_a[0] <= range_b[0] and range_a[1] >= range_b[0]:
        return True

    #Range b ends within range a
    if range_a[0] <= range_b[1] and range_a[1] >= range_b[1]:
        return True

    #Range a starts within range b
    if range_b[0] <= range_a[0] and range_b[1] >= range_a[0]:
        return True

    #Range a ends within range b
    if range_b[0] <= range_a[1] and range_b[1] >= range_a[1]:
        return True
    return False

def combine_lines(lines):
    new_lines = lines
    bmerged = True
    while bmerged == True:
        bmerged = False
        newer_lines = []
        line_a = new_lines.pop(0)
        while len(new_lines) > 0:
            line_b = new_lines.pop(0)
            if range_overlaps(line_a, line_b):
                line_a = (min(line_a[0], line_b[0]), max(line_a[1], line_b[1]))
                bmerged = True
            else:
                newer_lines.append(line_b)
        newer_lines.append(line_a)
        new_lines = newer_lines

    return new_lines

def get_excluded_locations(y_target: int, sensors: List[Sensor]) -> Set[Tuple[int,int]]:
    lines = []
    for sensor in sensors:
        leftover_distance = sensor.distance - abs(y_target - sensor.pos[1])
        if leftover_distance >= 0:
            #start_pos = (sensor.pos[0], y_target)
            #can reach y target, so iterate over reachable tiles
            max_x = min(sensor.pos[0] + leftover_distance, max_dimension)
            min_x = max(sensor.pos[0] - leftover_distance, 0)
            line = (min_x, max_x)
            lines.append(line)

    #print("=============================")
    #print(lines)
    lines = combine_lines(lines)
    if len(lines) > 1:
        return lines
    else:
        pass
        #print(lines)
    
    return None

valid_index_set: Set[int] = set()
for i in range(0,max_dimension):
    valid_index_set.add(i)

#excluded_locs = get_excluded_locations(height, in_sensors)
#print(excluded_locs[1])

#remaining = valid_index_set.difference(excluded_locs[1])
#print(remaining)

def solve():
    for i in range(0, max_dimension + 1):
        excluded_lines = get_excluded_locations(i, in_sensors)
        if excluded_lines is not None:
            print(excluded_lines)
            max_start = max(excluded_lines[0][0],excluded_lines[1][0])
            min_end = min(excluded_lines[0][1],excluded_lines[1][1])
            print(f'({min_end + 1},{i})')
            tuning_freq = (min_end + 1) * 4000000 + i
            print(tuning_freq)
            break

solve()
print("Done")

#import cProfile
#import re
#cProfile.run(f'solve()')