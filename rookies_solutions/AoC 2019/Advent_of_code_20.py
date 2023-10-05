import re
# import copy
# from collections import Counter
from collections import defaultdict
# from collections import OrderedDict
# import numpy as np
# from collections import deque
# import math
import itertools
# import time
# from operator import itemgetter
# from functools import reduce
import networkx as nx
# from matplotlib import pyplot as plt
# import pandas as pd
# import easygui
# import os
import math
import copy
from pathlib import PureWindowsPath
from collections import deque
# import matplotlib
import matplotlib.pyplot as plt
import numpy as np

test = 0
day = 20
year = 2019
if test:
    with open(f'Inputs/{year}-{day} - test.txt') as file:  # read input
        input_list = file.read()#.split("\n")
else:
    with open(f'Inputs/{year}-{day}.txt') as file:  # read input
        input_list = file.read()#.split("\n")

# input_list = [int(x) for x in input_list.split(",")]


torus_map = """         A           
         A           
  #######.#########  
  #######.........#  
  #######.#######.#  
  #######.#######.#  
  #######.#######.#  
  #####  B    ###.#  
BC...##  C    ###.#  
  ##.##       ###.#  
  ##...DE  F  ###.#  
  #####    G  ###.#  
  #########.#####.#  
DE..#######...###.#  
  #.#########.###.#  
FG..#########.....#  
  ###########.#####  
             Z       
             Z       
"""
torus_map = input_list

# translate the result to the explored_dict
map_dict = defaultdict(str)
for y, line in enumerate(torus_map.split("\n")):
    for x, char in enumerate(line):
        map_dict[x+(1j*y)] = char

directions = [1, -1, -1j, 1j]

list_of_positions = list(map_dict.keys())
for k in list_of_positions: # iterate over positions
    v = map_dict[k]
    if re.match("^[A-Z]$", v):   # if letter look for portals

        for direction in directions:
            #print(v,map_dict[k+direction])
            if re.match("^[A-Z]$", map_dict[k+direction]) and re.match("\.", map_dict[k+2*direction]):
                print(v, map_dict[k+direction], map_dict[k+2*direction])

                map_dict[k + 2 * direction] = "".join(sorted([map_dict[k], map_dict[k + direction]]))
                map_dict[k + direction] = " "
                map_dict[k] = " "

portals = dict()
for k in list_of_positions:  # iterate over positions
    v = map_dict[k]



nodes = dict()
for k in list_of_positions:
    v = map_dict[k]
    if v == "." or re.match("^[A-Z]{2}$",v):
        nodes[k]=[]
        for direction in directions:
            neighbour_val = map_dict[k + direction]

            if neighbour_val == ".":
                nodes[k].append(k+direction)
            elif re.match("^[A-Z]{2}$",neighbour_val):
                print("neighbour is a portal")
                nodes[k].append(k + direction)

# bridge over portals
portals = {k: v for k,v in map_dict.items() if re.match("^[A-Z]{2}$", v)}

for key1, portal1 in portals.items():
    for key2, portal2 in portals.items():
        if portal1 == portal2 and key1 != key2:
            nodes[key1].append(key2)

g = nx.Graph()

for pos,neighbours in nodes.items():
    for tar in neighbours:
        g.add_edge(pos,tar)
#
# for key1, portal1 in portals.items():
#     if portal1 not in ["AA","ZZ"]:
#         for n in nodes[key1]:
#             if n not in portals:
#                 g = nx.contracted_nodes(g, n, key1)

start, = {key for key,value in portals.items() if value == "AA"}
end, = {key for key,value in portals.items() if value == "ZZ"}
print(start,end)

print(nx.shortest_path_length(g, source=start, target=end))


# dipslay the resulting graph
if test:
    g2 = nx.spring_layout(g, iterations=600)
    # path_edges = list(zip(path, path[1:]))
    # nx.draw_networkx_nodes(g,pos=g2,nodelist=path,node_color='r')
    # nx.draw_networkx_edges(g, pos=g2, edgelist=path_edges, edge_color='r', width=10)
    # nx.draw(g, pos=g2, with_labels=True, font_weight='bold')
    nx.draw(g, with_labels=True, font_weight='bold')
    plt.show()

exit(0)




portals_inv = defaultdict(list)
for k,v in portals.items():
    portals_inv[v].append(k)

print(portals_inv)
exit(0)
for portal in portals:
    bridge = {k: v for k, v in map_dict.items() if re.match(portal, v)}
    print(bridge)

for k,v in portals.items():
    pass



exit(0)
for k,neighbours in nodes.items():
    if re.match("^[A-Z]{2}$", map_dict[k]):
        print("match")
        portals[k] = neighbours[0]

print(nodes)





