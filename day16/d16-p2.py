from typing import List, Tuple, Optional, Set, Dict
from os.path import join
import shlex
import math

inputfile = open('day16/input.txt', 'r')
test = False
if test:
    inputfile = open('day16/test.txt', 'r')
Lines = inputfile.readlines()

def parse_valves(in_lines, flow_rates, tunnels):
    for line in in_lines:
        line_split = line.strip().split(";")
        flow_rate = int(line_split[0].split("=")[-1])
        valve_name = shlex.split(line_split[0])[1]
        new_tunnels = shlex.split(line_split[1].replace(",",""))[4:]
        print(f'{valve_name}: {flow_rate}: {new_tunnels}')
        tunnels[valve_name] = new_tunnels
        flow_rates[valve_name] = flow_rate

def reconstruct_path(came_from, current):
    total_path = [current]
    curr_node = current
    while curr_node in came_from:
        curr_node = came_from[curr_node]
        total_path.insert(0, curr_node)
    #print(total_path)
    return total_path

def bfs_path(start, stop, edges):
    pass
    open_nodes = [start]
    came_from: Dict[str, str] = {}
    b_found = False
    while len(open_nodes) > 0 and b_found == False:
        curr_node = open_nodes.pop(0)
        if curr_node == stop:
            b_found = True
            break

        for tunnel in edges[curr_node]:
            if tunnel not in came_from and tunnel != start:
                came_from[tunnel] = curr_node
                if tunnel not in open_nodes:
                        open_nodes.append(tunnel)

    if b_found:
        #print("Found")
        return reconstruct_path(came_from, stop)
    else:
        #print("NOT FOUND")
        return []

def pre_compute_paths(tunnels: Dict[str, List[str]]) -> Dict[str, List[str]]:
    paths: Dict[str, List[str]] = {}
    nodes = list(tunnels.keys())
    for i in range(len(nodes)):
        for j in range(i+1, len(nodes)):
            node_a = nodes[i]
            node_b = nodes[j]
            #build path a->b
            path = bfs_path(node_a, node_b, tunnels)
            #Add both path
            paths[node_a + node_b] = path
            reverse_path = path.copy()
            reverse_path.reverse()
            paths[node_b + node_a] = reverse_path
            pass
    
    return paths


g_flow_rates: Dict[str, int] = {}
g_tunnels: Dict[str, List[str]] = {}
parse_valves(Lines, g_flow_rates, g_tunnels)
g_node_paths: Dict[str, List[str]] = pre_compute_paths(g_tunnels)

def greedy():
    time_left = 30
    curr_node = 'AA'
    open_valves = []
    flow_amount = 0
    all_valves = g_flow_rates.keys()
    good_valves = []
    for key in all_valves:
        if g_flow_rates[key] > 0:
            good_valves.append(key)
    while time_left > 0:
        best_valve = ''
        best_flow_amount = 0
        best_time_cost = 0
        for valve in good_valves:
            if valve in open_valves or valve == curr_node:
                #skip valve, as already open
                continue
            tunnel_key = curr_node + valve
            time_for_valve = (len(g_node_paths[tunnel_key]))
            if time_for_valve > time_left:
                continue
            flow_time = time_left - time_for_valve
            candidate_flow_rate = g_flow_rates[valve] * flow_time
            if candidate_flow_rate > best_flow_amount:
                best_flow_amount = candidate_flow_rate
                best_valve = valve
                best_time_cost = time_for_valve
        if best_valve == '':
            #print(f'No good candidate for curr_node: {curr_node}')
            time_left = 0
            break
        print(f'Stepping to node: {best_valve} with cost of: {best_time_cost}')
        open_valves.append(best_valve)
        flow_amount += best_flow_amount
        curr_node = best_valve
        time_left -= best_time_cost
    return flow_amount

class bnb_node:
    def __init__(self, name = "", parent = None) -> None:
        self.parent = parent
        self.cost = 0
        self.name = name
    
    def calc_cost(self, node_paths):
        if self.cost != 0:
            return self.cost
        curr_node = self
        cost = 0
        while curr_node is not None:
            prev_node = curr_node.parent
            if prev_node == None:
                break
            path_name = curr_node.name+prev_node.name
            cost += len(node_paths[path_name])
            curr_node = prev_node
        self.cost = cost
        return cost
    
    def calc_path(self, node_paths):
        curr_node = self
        path = [curr_node.name]
        while curr_node is not None:
            prev_node = curr_node.parent
            curr_node = prev_node
            if curr_node == None:
                continue
            path.append(prev_node.name)
        path.reverse()
        return path

def calc_path_time(path: List[str]) -> int:
    path_time = 0
    for i in range(len(path) - 1):
        node_a = path[i]
        node_b = path[i+1]
        path_name = node_a+node_b
        time_for_valve = (len(g_node_paths[path_name]))
        path_time += time_for_valve
    return path_time

def calc_path_flow_amount(path: List[str], time=26) -> int:
    total_flow_amount = 0
    time_left = time
    for i in range(len(path) - 1):
        node_a = path[i]
        node_b = path[i+1]
        path_name = node_a+node_b
        time_for_valve = (len(g_node_paths[path_name]))
        time_left -= time_for_valve
        flow_time = time_left
        flow_amount = g_flow_rates[node_b] * flow_time
        total_flow_amount += flow_amount
    return total_flow_amount

def agent_process(time, good_valves):
    curr_node = 'AA'
    start_node = bnb_node('AA')
    node_queue = [start_node]
    best_path_node = None
    best_flow_amount = 0
    while len(node_queue) > 0:

        #Next node to work on 
        curr_node = node_queue.pop(0)
        curr_path = curr_node.calc_path(g_node_paths)
        #print(f'{curr_path} : {calc_path_flow_amount(curr_path, time)}')

        ####Eval Best Path
        if curr_node.parent != '':
            curr_node_flow_amount = calc_path_flow_amount(curr_path, time);
            if curr_node_flow_amount > best_flow_amount:
                best_flow_amount = curr_node_flow_amount
                best_path_node = curr_node
        
        ##### Generate nodes for this path
        time_left = time - calc_path_time(curr_path)
        for valve in good_valves:
            if valve == curr_node.name:
                continue
            if valve in curr_path:
                continue
            node_a = curr_node.name
            node_b = valve
            path_name = node_a+node_b
            if len(g_node_paths[path_name]) < time_left:
                node_queue.append(bnb_node(node_b, curr_node))
        
    return best_path_node.calc_path(g_node_paths)


#Was going to be branch and bound, but theres currently now bounding calculations
def branch_and_bound():
    time = 26
    all_valves = g_flow_rates.keys()
    good_valves = []
    for key in all_valves:
        if g_flow_rates[key] > 0:
            good_valves.append(key)

    best_human_path = agent_process(time, good_valves)
    human_flow = calc_path_flow_amount(best_human_path, time)

    for valve in best_human_path:
        g_flow_rates[valve] = 0
    
    good_valves = []
    for key in all_valves:
        if g_flow_rates[key] > 0:
            good_valves.append(key)

    print("Elephant")
    best_elephant_path = agent_process(time, good_valves)
    elephant_flow = calc_path_flow_amount(best_elephant_path, time)

    #This solution processes the human path and then the elephant path, which is most definitely not general, but it worked on my input.
    print(elephant_flow + human_flow)

    #print(calc_path_time(best_path))
    #print(best_path)
    #print(best_flow_amount)

def print_good_valve_paths():
    all_valves = g_flow_rates.keys()
    good_valves = ['AA']
    for key in all_valves:
        if g_flow_rates[key] > 0:
            good_valves.append(key)
    
    for i in range(len(good_valves)):
        for j in range(i+1, len(good_valves)):
            path = good_valves[i]+good_valves[j]
            print(f'{path}: {len(g_node_paths[path])}')

branch_and_bound()
