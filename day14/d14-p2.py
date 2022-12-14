#Hack to allow utilising a parent directory library
#https://www.geeksforgeeks.org/python-import-from-parent-directory/
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)


from typing import List, Tuple, Optional, Set, Dict
from os.path import join
import shlex
import math
import functools
import json

from utils import math2d
from utils.MathHelpers import Vector

inputfile = open('day14/input.txt', 'r')
#inputfile = open('day14/test.txt', 'r')
in_lines = inputfile.readlines()

lines = []

for in_line in in_lines:
    syms = in_line.strip().split(" -> ")
    points = []
    for sym in syms:
        coords = sym.split(',')
        newpoint = [int(coords[0]), int(coords[1])]
        points.append(newpoint)

    lines.append(points)

AABB = math2d.AxisAlignedBoundingBox2D()
sand_spawn_point = [500,0]
AABB.add_point(sand_spawn_point)

for line in lines:
    for point in line:
        AABB.add_point(point)

AABB_extent = AABB.get_size()
print(AABB_extent)
print(AABB.get_min())
print(AABB.get_max())

EMPTY_CELL = ' '
map = []
for y in range(AABB_extent[1] + 1):
    map.append([EMPTY_CELL] * (AABB_extent[0] + 1))

def draw_map(map):
    for line in map:
        line_str = ""
        for cell in line:
            line_str += cell
        print(line_str)

def transform_coord(coord, AABB):
    min = AABB.get_min()
    return Vector.subtract_vector(coord, min)

def draw_cell(coord, map, char, AABB):
    new_coord = transform_coord(coord, AABB)
    map[new_coord[1]][new_coord[0]] = char

def step_limit(delta, max_step = 1):
    new_delta = min(abs(delta), 1)
    if delta < 0:
        new_delta = -new_delta
    return new_delta

def draw_line(coord_a, coord_b, map, char, AABB):
    delta_vec = Vector.subtract_vector(coord_b, coord_a)
    step = [step_limit(delta_vec[0]), step_limit(delta_vec[1])]
    
    curr_coord = Vector.subtract_vector(coord_a, step)
    while Vector.are_equal(curr_coord, coord_b) == False:
        curr_coord = Vector.add_vector(curr_coord, step)
        draw_cell(curr_coord, map, char, AABB)

#Draw lines
for line_set in lines:
    for i in range(len(line_set) - 1):
        draw_line(line_set[i], line_set[i+1], map, "#", AABB)

#Draw Sand Spawn Point
draw_cell(sand_spawn_point, map, "+", AABB)



def get_cell(coord, map, AABB):
    new_coord = transform_coord(coord, AABB)
    if new_coord[0] < 0 or new_coord[0] >= len(map[0]):
        return False
    if new_coord[1] < 0 or new_coord[1] >= len(map):
        return False
    return map[new_coord[1]][new_coord[0]]

down_vec_step = [0,1]
down_left_vec_step = [-1,1]
down_right_vec_step = [1,1]

def simulate_sand_particle(spawn_coord, map, AABB):
    max_y = AABB.get_max()[1]
    curr_coord = spawn_coord.copy()
    at_rest = False
    out_of_bounds = False
    step = 0
    while curr_coord[1] <= max_y and at_rest == False and out_of_bounds == False:
        step += 1
        down_vec = Vector.add_vector(curr_coord, down_vec_step)
        down_left_vec = Vector.add_vector(curr_coord, down_left_vec_step)
        down_right_vec = Vector.add_vector(curr_coord, down_right_vec_step)

        down_cell = get_cell(down_vec, map, AABB)
        down_left_cell = get_cell(down_left_vec, map, AABB)
        down_right_cell = get_cell(down_right_vec, map, AABB)
        #attempt step down
        if down_cell == EMPTY_CELL or down_cell == False:
            curr_coord = down_vec
            if down_cell == False:
                print("OOB")
                out_of_bounds = True
        #attempt step left
        elif down_left_cell == EMPTY_CELL or down_left_cell == False:
            curr_coord = down_left_vec
            if down_left_cell == False:
                print("OOB")
                out_of_bounds = True
        #attempt step right
        elif down_right_cell == EMPTY_CELL or down_right_cell == False:
            curr_coord = down_right_vec
            if down_right_cell == False:
                print("OOB")
                out_of_bounds = True
        #At rest
        else:
            at_rest = True
        
        #draw_cell(curr_coord, map, str(step), AABB)
        #draw_map(map)

    if at_rest:
        print("at rest")
        draw_cell(curr_coord, map, 'o', AABB)
        return True
    else:
        return False

sand_particles = 0
while simulate_sand_particle(sand_spawn_point, map, AABB):
    sand_particles += 1
    print(sand_particles)
    pass

#Draw Map
draw_map(map)