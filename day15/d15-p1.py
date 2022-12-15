from typing import List, Tuple, Optional, Set, Dict
from os.path import join
import shlex
import math

inputfile = open('day15/input.txt', 'r')
height = 2000000
test = True
if test:
    inputfile = open('day15/test.txt', 'r')
    height = 10
Lines = inputfile.readlines()

class Sensor:
    def __init__(self, pos: Tuple[int,int] = (0,0), nearest_beacon: Tuple[int,int] = (0,0)) -> None:
        self.pos: Tuple[int,int] = pos
        self.nearest_beacon: Tuple[int,int] = nearest_beacon

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

def get_excluded_locations(y_target: int, sensors: List[Sensor]) -> Set[Tuple[int,int]]:
    excluded_locations: Set[Tuple[int,int]] = set()
    for sensor in sensors:
        leftover_distance = sensor.get_manhattan_distance() - abs(y_target - sensor.pos[1])
        if leftover_distance >= 0:
            start_pos = (sensor.pos[0], y_target)
            #excluded_locations.add(start_pos)
            #can reach y target, so iterate over reachable tiles
            for i in range(leftover_distance+1):
                pos = (sensor.pos[0] + i, y_target)
                excluded_locations.add(pos)
            for i in range(leftover_distance+1):
                pos = (sensor.pos[0] - i, y_target)
                excluded_locations.add(pos)
    
    for sensor in sensors:
        if sensor.pos in excluded_locations:
            excluded_locations.remove(sensor.pos)
        if sensor.nearest_beacon in excluded_locations:
            excluded_locations.remove(sensor.nearest_beacon)
    return excluded_locations

excluded_locs = get_excluded_locations(height, in_sensors)
print(excluded_locs)
print(len(excluded_locs))
