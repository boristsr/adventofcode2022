from typing import List, Tuple, Optional, Set, Dict
from os.path import join
import shlex
import math
import functools

inputfile = open('day12/input.txt', 'r')
#inputfile = open('day12/test.txt', 'r')
Lines = inputfile.readlines()

map: List[List[int]] = []

pos: List[int] = [0,0]

start_loc: Tuple[int, int] = (0,0)
end_loc: Tuple[int, int] = (0,0)

for line in Lines:
    stripped_line = line.strip()
    row: List[int] = []
    for char in stripped_line:
        if char == "S":
            #start
            start_loc = tuple(pos)
            row.append(0)
        elif char == "E":
            #start
            end_loc = tuple(pos)
            row.append(25)
        else:
            row.append(ord(char) - ord("a"))
        pos[0] += 1
    map.append(row)
    pos[1] += 1
    pos[0] = 0

pos = [0,0]

def heuristic(node: Tuple[int, int]) -> int:
    return 1

def reconstruct_path(came_from, current):
    total_path = [current]
    curr_node = current
    while curr_node in came_from:
        curr_node = came_from[curr_node]
        total_path.insert(0, curr_node)
    return total_path

def is_valid_neighbor(current, neighbor, came_from):
    curr_height = map[current[1]][current[0]]
    new_neighbor_height = map[neighbor[1]][neighbor[0]]
    height_diff = new_neighbor_height - curr_height
    if height_diff > 1:
        return False
    
    #Has this neighbor already been traversed?
    if neighbor in came_from.values():
        return False
    
    return True

def get_valid_neighbors(position, came_from):
    neighbors = []
    #Sideways neighbors
    if position[0] > 0:
        new_neighbor = (position[0]-1, position[1])
        if is_valid_neighbor(position, new_neighbor, came_from):
            neighbors.append(new_neighbor)
    if position[0] < len(map[0]) - 1:
        new_neighbor = (position[0]+1, position[1])
        if is_valid_neighbor(position, new_neighbor, came_from):
            neighbors.append(new_neighbor)
    
    #vertical neighbors
    if position[1] > 0:
        new_neighbor = (position[0], position[1]-1)
        if is_valid_neighbor(position, new_neighbor, came_from):
            neighbors.append(new_neighbor)
    if position[1] < len(map) - 1:
        new_neighbor = (position[0], position[1]+1)
        if is_valid_neighbor(position, new_neighbor, came_from):
            neighbors.append(new_neighbor)

    return neighbors

def weight(current, neighbor):
    return 1

def a_star(start, goal, h):
    open_set = []
    open_set.append(start)
    came_from = {}
    g_score = {}
    g_score[start] = 0
    
    f_score = {}
    f_score[start] = heuristic(start)

    search_steps = 0
    while len(open_set) > 0:
        search_steps += 1
        current = open_set.pop(0)
        if current == goal:
            print(f'Reconstructing path after {search_steps} search steps')
            return reconstruct_path(came_from, current)
        
        #open_set.remove(current)
        #for each neighbor
        neighbors = get_valid_neighbors(current, came_from)

        for neighbor in neighbors:
            tentative_gscore = g_score[current] + weight(current, neighbor)
            if tentative_gscore not in g_score or tentative_gscore < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_gscore
                f_score[neighbor] = tentative_gscore + heuristic(neighbor)
                if neighbor not in open_set:
                    open_set.append(neighbor)

    print(f'Failed to find a path after {search_steps} search steps')
    return []
    

#print(get_neighbors((0,0)))
#print(get_neighbors((1,1)))
#print(get_neighbors((6,3)))
#print(get_neighbors((7,4)))

print("Starting Location: " + str(start_loc))
print("Goal Location: " + str(end_loc))

shortest_path = 300000000

num_starting_points = 0
num_valid_paths = 0

for y in range(len(map)):
    for x in range(len(map[0])):
        start_loc = (x,y)
        if map[y][x] == 0:
            num_starting_points += 1
            path = a_star(start_loc, end_loc, heuristic)
            if len(path) != 0:
                num_valid_paths += 1
            if len(path) < shortest_path and len(path) != 0:
                shortest_path = len(path)

print("Total Steps Taken: " + str(shortest_path-1))
print("Num Starting Points: " + str(num_starting_points))
print("Num Valid Paths: " + str(num_valid_paths))
#print(path)