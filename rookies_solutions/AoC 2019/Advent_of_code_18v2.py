import copy
import re
import heapq
from time import sleep
from collections import deque


def display_board(layers, translations, empty_space):  # xmin,ymax_,xmin=None,ymin,
    # get the minimum and maximum coordinates of display
    xmax, xmin = max([x for x, y in layers[0].keys()]), min([x for x, y in layers[0].keys()])
    ymax, ymin = max([y for x, y in layers[0].keys()]), min([y for x, y in layers[0].keys()])

    # initialise the copy of layers
    board_dict_copy_list = []

    for board_dict in layers:
        # buffer_dict = defaultdict(constant_factory())
        # print(board_dict, xmax, xmin, ymax, ymin)
        # translate by xmin,ymin

        # trim the layers coordinates to start at 0,0
        temp = {((x - xmin, y - ymin)): board_dict[(x, y)] for x, y in board_dict.keys()}
        board_dict_copy_list.append(temp)

    # buffer_dict.update(board_dict_copy)

    # initialise empty display
    display = [[empty_space for i in range(xmax - xmin + 1)] for j in range(ymax - ymin + 1)]
    # print("display size x,y initiated in display", len(display[0]), len(display))

    # iterate layers in order to overlay them on display
    for i, board_dict_copy in enumerate(board_dict_copy_list):
        # iterate over lines in each layer
        for y in range(ymax - ymin, -1, -1):  # reverse to display from top to bottom
            line = []
            # iterate over points in each display
            for x in range(xmax - xmin + 1):
                try:
                    # translate the chars according to translations dictionary
                    char = str([translations[i].get(n, n) for n in [board_dict_copy[(x, y)]]][0])
                    display[y][x] = char
                except KeyError:
                    pass  # char = " "
    # print the display
    for screenline in display:
        print("".join(screenline))
    print("===================================================================")
    return None


# start the program
# full map
map_str = """#################################################################################
#...........#.............#...#.....#...#...............#.....#.....#....t#.....#
#.#####.###.###.#########.#.#.#.#.###.#.#.#####.#######.#.###.#.###.#.###.#.#.#.#
#..m#.#...#...#...#...#...#.#...#.....#.#.....#...#...#...#...#...#...#...#.#.#.#
###.#.###.###.###.###.#.#######.#######.#######.#.#.#.#####.#####.#####.###.#.#.#
#.#...#...#.#...#...#.#.#.....#.#.......#.....#.#...#.....#.#...#...#.#...#.#.#.#
#.###.#.###.###.###.#.#.#.###.#.#.#####.#.###.###########.#.#.#.###.#.###.#.#.#.#
#.#...#.#.....#.....#.#...#.#.#.#.#.#...#...#...B.........#...#.J.#.#...#.#.#.#.#
#.#.###.###.#########.#####.#.###.#.#.#####.#####################.#.###.#.###.#.#
#.#...#.#...#.........#...#.#...#.#.#.#.#...#.............#...#...#.#...#....v#.#
#.###.#.#.###.#####.#.#.#.#.###.#.#.#.#.#.###.###########.#.#.#.###.#.#########P#
#.#...#.#.....#.#...#...#.#...#...#.#.#.#...#.....#...#...#.#...#w..#.#...#.....#
#V#.###.#.#####.#.#######.#.#.#####.#.#.#.#.#####.#.#.#.###.#####.###.#.#.#.#####
#...#...#.....#.#.#.......#.#.......#.#.#.#.#.....#.#.#.#.#.#...#.#...#.#.#.....#
#####.#######.#.#.#######.###.#####.#.#.#.#.#.#####.#.#.#.#.###.#.#.###.#.#####.#
#...#...#.......#.......#.....#.....#.#.#.#.#...#...#.....#.....#.#.#...#...#...#
#.#.###.###.#######.###.#######.#####.#.#.#N#.#.#########.###.###.#.#.###.###.###
#.#...#...#.#.....#...#.#...#.#.....#...#.#.#.#...#.....#.#...#...#...#.#...#.#.#
#.###.###.###.###.###.#.#.#.#.###.#####.###.#.###.#.###.###.###.###.###D###.#.#.#
#.#.......#...#.#...#.#...#.#.....#...#.#...#.#...#...#.#...#...#.#.#.....#.#...#
#.#######.#.###.###.###.###.#######.#.#.#.###.#.#####.#.#.###.###.#.#.###.#.###.#
#.T.#.....#.#.....#...#...#.........#...#.#...#.....#.#.....#.#...#.#.#...#.....#
###.#.#####.#.#.#########.###############.#########.#.###########.#.#.###########
#.#.#...#...#.#.........#...#.........#.#...#.....#.....#.........#.#...........#
#.#.#####.###.#####.#######.#######.#.#.###.#.###.#######.#####.###.#####.#######
#.#......l#.#.....#.......#.........#...#...#.#.#.#.....#...#.#...#.....#...#...#
#.#########.#.#########.#.#############.#.###.#.#.#.###.###.#.###.#####.#.#.#.#.#
#.....#.....#.#...#...#.#...#.......#..z#.....#.#...#.....#.#...#.......#.#...#.#
#.###.#.###.#.#.#.#.#.###.#.#.###.#.#.###.#####.#####.#####.#.#.#########.#####.#
#...#.#.#.#...#.#.#.#...#.#.#.#...#.#...#.#.........#.....#...#.#...#.....#.....#
###.###.#.#####.#.#.###.#.#.###.#.#####.#.#######.#.#####.#####.#.#.#.#####.###.#
#...#..d#.#...#.#.#...#...#...#.#.#.....#.....#...#.....#.....#...#.#...#q..#.#.#
#.#.#.###.#.#.#.#.###.#######.#.#.#.#########.#.###########.#.#####.#####.###.#.#
#.#.#...#.#.#...#.#...#.........#.#.#...#.#...#...........#.#.....#...#...#...#.#
#.#####.#.#.#####.#.#######.#######.#.###.#.###.#########.#.#####.###.#.#####.#.#
#.......#.#...#...#.#.....#.#.......#...#.#.#.....#.....#.#...#...#...#.....#...#
#.#######.###.###.#.#.###.###.#######.#.#.#.#####.#.#####.###.#####.#######.#####
#.......#...#...#...#.#.#...#.#...#...#.#.#.#...#...#...#...#.....#.#.....#.....#
#######.#.#.###.#####.#.###.#.#.#.#####.#.#.#.#.#####.#.###.#####.#.#.###.#####.#
#.........#...#...........#.....#.............#....c..#.........#.....#.........#
#######################################.@.#######################################
#...........#.........#.C.........#...........#.........#.....................X.#
#Q#########.#.#.#####.#.#########.#.###.#.###.#.#######.#.###############.#####.#
#.#.........#.#...#.#...#.......#.#.#.#.#...#.....#...#.#.....#.#.......#...#...#
#.#####.#########.#.#####.#####.#.#.#.#.###.#######.#.#.#####.#.#.#####.#.###.#.#
#.....#.#.....#...#.....#.#...#.#...#.#.#.#.#...#...#...#.....#.#.#.....#.#u..#.#
#.###.#U#.###.#.#####.###.#.###.#####.#.#.#.###.#.#.#####.#####.#.#.#######.###.#
#j..#.#...#...#.....#.#...#...#.....#.#.#.#.....#.#.#.....#.....#.#.........#...#
###.#.#####.#######.#.#.#####.###.#.#.#.#.#####.#.###.#####.###.#.#####.#######.#
#...#.....#.....#...#.#...#...#...#.#.#.#...#...#.....#.....#...#.#...#.#.....#.#
#######.#.#####.#.###.###.#.#.#.###.#.#.###.#.#########.#####.###.#.#.###.###.###
#.....#.#...#.#.#.#.....#.#.#.#.#.....#.#...#.#.....#...#.....#.#...#.......#...#
#.###.#.###.#.#.#.###.#.#.#.#.#.#######.#.###.###.#.###.#.#####.###########.###.#
#f#.#.#.#...#.#.#...#.#.#b#.#.#.#.......#.#...#...#.#...#.....#...#.....#...#...#
#.#.#.###.###.#.###.#.#.#.#.###.#.#######.#.###.###.#.#######.###.#.###.#####.#.#
#.#.......#...#.#...#.#...#...#...#.....#...#...#.....#...........#.#.#.#.....#.#
#.#########.#.#.#.###.#######.#######.###.###.#.#######.###########.#.#.#.#####.#
#.....#.....#.....#....x....#.......#...#n#...#.#.....#.....#.....#.#.#.F.#...#.#
#.###.#####.###############.###.###.###.#.###.###.###.#######.###.#.#.#####.###.#
#...#.....#.#r..........#.#.....#.#...#.#.....#...#...........#...#.#.#.........#
#.#######.###.#########R#.#######.###.#.#####.#.###.###########.###K#.#.#########
#.#.......#...#....g#...#.........#...#.#.....#.#...#.......#.#.....#.#...#.....#
#.#.#######.#######.#####.#.#######.###.#.#####.#.###.#####.#.#######.###.#.#.###
#.#...#...#...#.....#.....#.......#...#.#...#.#.#.#...#...#.#.#.#...#.....#.#...#
#.###.#.#.###G#.###I#.###########.###.#.###.#.#.#.#.#####.#.#.#.#.#.#.#####.###.#
#k#...#.#...#...#...#.....#s....#.#...#.#...#.#.#.#.......#...#...#.#.#.#...#.L.#
###.#.#.###.#####.#######.#.###O#.#.###.#.###.#.#.#######.#####.###.#.#.#.###.#.#
#..p#.#...#.....#.......#.#.#...#.#.....#.Z...#.#...#...#.#...#.#.#...#.#...#.#.#
#.###.###.###.#########.###.#.###.#####.#######.###.###.#.#.#.#.#.#####.###.#.###
#.#.#...#...#.......#..i#...#...#.#.....#.....#.#.#.....#.#.#...#....a....#.#...#
#.#.###.#.#######.#.#H###.#####.#.#.#####.###.#.#.#.#####.#.#####.#.#######.###.#
#.#.....#.#.....#.#.#.#...#o....#.#.#...#...#...#...#.....#.#...E.#.#......y..#.#
#.#######.#.###.###.#.#S#####.###.#.###.#.#.###.#####W#####.#.#.###.#.#########.#
#.#.......#.#.......#.#.....#.A.#.....#.#.#.#...#...#...#...#.#.#...#.#...#.....#
#.#.#######.#######.#.#####.###.#####.#.###.#.###.#.###.#.###.#.#####.###.#.###.#
#.#...#...#.#.Y.#...#..h....#.#...#.#.#.#...#...#.#.....#.#...#...........#...#.#
#.###.#.#.#.#.#.#############.###.#.#.#.#.###.###.#######.#############.#####.#.#
#...#...#.#...#...........#.......#.#.#.#.#...#...#.....#...#.........#.#.....#.#
#.#.#####.###########.#####.#######.#.#.#.#####.###.#######.#.#######.###.#####.#
#.#.....M...........#e......#...........#.......#.............#...........#.....#
#################################################################################"""

map_str1 = """########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################"""
# PREPARATION OF GRAPH
# prepare input
map_str_list = map_str.split("\n")
map_dict = {}
# translate the result to the explored_dict
for y, line in enumerate(map_str_list):
    for x, char in enumerate(line):
        map_dict[(x, y)] = char


class Node:
    def __init__(self, position, value, neighbours):
        self.position = position
        self.value = value
        self.neighbours = neighbours


# get nodes only
print("creating nodes")
nodes_dict = {}
for (x, y) in map_dict:
    if map_dict[(x, y)] == "#":
        continue
    up = (x + 1, y)
    down = (x - 1, y)
    left = (x, y - 1)
    right = (x, y + 1)
    view_poss = [up, down, left, right]

    nodeXY = Node((x, y), map_dict[(x, y)], dict())

    for view_pos in view_poss:
        view_val = map_dict.get(view_pos, "#")
        if view_val != "#":
            nodeXY.neighbours[view_pos] = 1
    # print(nodeXY.position,nodeXY.neighbours)
    nodes_dict[(x, y)] = nodeXY

print("count of nodes", len(nodes_dict))

nodes_map_dict = {x: nodes_dict[x].value for x in nodes_dict}
display_board([nodes_map_dict], [{}], " ")

# shave not meaningful neighbours

starting_count = 0
while len(nodes_dict) != starting_count:
    print("shaving bridges")
    starting_count = len(nodes_dict)
    nodes_dict_list = [x for x in nodes_dict]
    for pos in nodes_dict_list:
        nodeXY = nodes_dict[pos]
        # print(nodeXY)
        # print(len(nodeXY.neighbours))
        if nodeXY.value == "." and len(nodeXY.neighbours) == 2:
            neighbour1, neighbour2 = [x for x in nodeXY.neighbours]
            # print(neighbours)
            # nodeXY1 = nodeXY.neighbours
            # nodeXY2 - nodeXY.neighbuors
            # get current status of the relationships
            distance1 = nodeXY.neighbours[neighbour1]
            distance2 = nodeXY.neighbours[neighbour2]

            nodes_dict[neighbour1].neighbours.pop(pos, None)
            nodes_dict[neighbour2].neighbours.pop(pos, None)

            nodes_dict[neighbour2].neighbours[neighbour1] = distance1 + distance2
            nodes_dict[neighbour1].neighbours[neighbour2] = distance1 + distance2
            nodes_dict.pop(pos, None)

    print("count of meaningful nodes", len(nodes_dict))

    #
    # exit(0)
    # nodes_map_dict = {x: nodes_dict[x].value for x in nodes_dict}
    # display_board([nodes_map_dict], [{}], " ")

    # shave dead ends
    print("shaving dead ends")
    nodes_dict_list = [x for x in nodes_dict]
    for pos in nodes_dict_list:
        nodeXY = nodes_dict[pos]
        # print(nodeXY)
        # print(len(nodeXY.neighbours))
        if nodeXY.value == "." and len(nodeXY.neighbours) == 1:
            neighbour1, = [x for x in nodeXY.neighbours]
            # print(neighbours)
            # nodeXY1 = nodeXY.neighbours
            # nodeXY2 - nodeXY.neighbuors
            # get current status of the relationships
            distance1 = nodeXY.neighbours[neighbour1]
            # distance2 = nodeXY.neighbours[neighbour2]

            nodes_dict[neighbour1].neighbours.pop(pos, None)
            # nodes_dict[neighbour2].neighbours.pop(pos, None)

            # nodes_dict[neighbour2].neighbours[neighbour1] = distance1 + distance2
            # nodes_dict[neighbour1].neighbours[neighbour2] = distance1 + distance2
            nodes_dict.pop(pos, None)
    print("count of meaningful nodes", len(nodes_dict))

    # for key,nodeXY in nodes_dict.items():
    #      #if nodeXY.value == ".":
    #      print(nodeXY.value,key,len(nodeXY.neighbours),nodeXY.neighbours)

    # shave T-junctions and crossroads
    print("shave T junctions and everything that is not key or Gate")

    nodes_dict_list = [x for x in nodes_dict]
    for pos in nodes_dict_list:
        nodeXY = nodes_dict[pos]
        if nodeXY.value == "." and len(nodeXY.neighbours) > 1:
            # print("============================================")
            # print(pos, "calling my neighbours")
            # print("   ", nodeXY.neighbours)
            for neighbour1 in nodeXY.neighbours:
                for neighbour2 in nodeXY.neighbours:
                    if pos in [neighbour1, neighbour2]:
                        print("hey I am my own neighbour", pos)
                        exit(1)
                    if neighbour2 != neighbour1:
                        # print("giving contact info to ", neighbour1, "and", neighbour2)
                        # print("their contact books" )
                        # print("   ",nodes_dict[neighbour1].neighbours)
                        # print("   ",nodes_dict[neighbour2].neighbours)
                        # get current status of the relationships
                        distance1 = nodeXY.neighbours[neighbour1]
                        distance2 = nodeXY.neighbours[neighbour2]

                        distance3_1 = nodes_dict[neighbour1].neighbours.get(neighbour2, 10000000)
                        # print("They have already distance of", distance3_1)
                        distance3_2 = nodes_dict[neighbour2].neighbours.get(neighbour1, 10000000)

                        if distance3_1 != distance3_2:
                            print("incosistency ! node relationship not symmetrical between", neighbour1, neighbour2)
                            exit(1)
                        if distance3_2 > distance1 + distance2:
                            nodes_dict[neighbour2].neighbours[neighbour1] = distance1 + distance2
                            nodes_dict[neighbour1].neighbours[neighbour2] = distance1 + distance2

                        nodes_dict[neighbour1].neighbours.pop(pos, None)
                        nodes_dict[neighbour2].neighbours.pop(pos, None)

                        # print("After update their contact books")
                        # print("   ", nodes_dict[neighbour1].neighbours)
                        # print("   ", nodes_dict[neighbour2].neighbours)

            # print(pos, "signing of")
            nodes_dict.pop(pos, None)
    print("count of meaningful nodes", len(nodes_dict))

# print nodes and thei relationships
# for key,nodeXY in nodes_dict.items():
#      #if nodeXY.value == ".":
#      print(nodeXY.value,key,len(nodeXY.neighbours),nodeXY.neighbours)

# print map
# nodes_map_dict = {x: nodes_dict[x].value for x in nodes_dict}
# display_board([map_dict, nodes_map_dict], [{".": " ", "#": " "}, {}], " ")

# rekey the dictionaries, nodes and neighbours
translation_of_node_keys = {key: val.value if val.value != "." else str(key[0]) + str(key[1]) for key, val in
                            nodes_dict.items()}


def trans_dict_keys(dict, trans):
    """replaces dictionary keys based on provided dictionary in format oldkey:newkey
       doesn't preserve order of dictionary"""
    for oldkey, newkey in trans.items():
        try:
            dict[newkey] = dict.pop(oldkey)
        except KeyError:
            pass
    return dict


# rekey the node dict
nodes_dict = trans_dict_keys(nodes_dict, translation_of_node_keys)
# rekey the neighbours
for key, node in nodes_dict.items():
    node.neighbours = trans_dict_keys(node.neighbours, translation_of_node_keys)

print("NODES AND THEIR NEIGHBOURS:")
for x in nodes_dict:
    print(nodes_dict[x].value, nodes_dict[x].neighbours)

print("===================================================================")

print(r"""Executing Dijkstra
  ________  .___     ____.____  __.  ______________________________    _____
  \______ \ |   |   |    |    |/ _| /   _____/\__    ___/\______   \  /  _  \
   |    |  \|   |   |    |      <   \_____  \   |    |    |       _/ /  /_\  \
   |    `   \   /\__|    |    |  \  /        \  |    |    |    |   \/    |    \
  /_______  /___\________|____|__ \/_______  /  |____|    |____|_  /\____|__  /
          \/                     \/        \/                    \/         \/
""")

# parq = [(1,"a"),(2,"A"),(1,"b"),(2,"C")]

qu = deque([("@", 0, "", {"@"})])
states = {}

silent = True

all_keys = frozenset({x for x in nodes_dict if re.match(r"[a-z]", str(x))}.union({"@"}))

while True:

    # try to pop off the first in que
    try:
        pack = qu.popleft()
    except IndexError:  # if empty end execution
        break
    # unpack at node
    node, distance, origin, keychain = pack

    if not silent: print("I am at",node,"with",keychain)

    keyset = (node, frozenset(keychain))




    # if there is already another path to this set of keys
    if keyset in states.keys():
        cur_distance, cur_origin = states[keyset] # get the direction and distance of the original path

        if not silent: print("I have such estimate")
        if not silent: print(keyset, (cur_distance, cur_origin))

        # if the new distance is smaller than current estimate for given set of keys - change the estimate
        if distance < cur_distance:

            if not silent: print("I bring better estimate")
            if not silent: print(keyset,(distance,origin))

            states[keyset] = (distance, origin)
            # how to update the value upstream, with terminating??
            # continue # new path to this keystate and place was found. great  rest can be reused
        else:
            continue  # if this is not the shortest path then terminate
    else:  # if keyset is not present already add it with the distance and origin
        states[keyset] = (distance, origin)


    # if all the keys are here then terminate sent then terminate here
    if keychain == all_keys:
        states[keyset] = (distance, origin)
        continue

    # send packs to neighbours
    for neighbour, dist_to in nodes_dict[node].neighbours.items():

        # terminate if the gate is closed
        if neighbour.isupper() and neighbour.lower() not in keychain:
            pass
        else:
            next_pack = (neighbour, dist_to + distance, node, keychain.union({neighbour.lower()}))
            qu.append(next_pack)
    # print(len(qu))
    # input("Enter to continue")



#print(sorted(all_keys))
output = [(k[0], x) for k, x in states.items() if k[1] == all_keys]
print(output)

lengths = [x[0] for k, x in states.items() if k[1] == all_keys]

print("min path to all keys according to algorithm above is:", min(lengths))
print()
exit(0)

print("trying to retrace path")



# print(states)
# info stored on by position, keychain set, distance, from which direction
# at the end the route is folded to get the route
# parq = [("a",1),("A",2),("b",1),("C",1)]
# parq = [4,5,6,234,1,2,34]

# heapq.heappush(parq, 11)
# print(heapq.heappop(parq))

# add to awaiting nodes at the end when key is unlocked
# in parity queue first should go the keys (a,b,c....) then normal nodes and doors


# parity queue tuple (case, distance, id )
# parq = [(0, 0 ,"@")]
# parq = [(0, "@","")]
# heapq.heapify(parq)

parq = {"@": (0, "")}
# heapq.heapify(parq)
# nodes still to be explored
# nodeq = [(100000,int(node.isupper()),node) for node in nodes_dict if node != "@" and not re.match(r"[A-Z]", node)]
# nodeq = [(100000,node) for node in nodes_dict if node != "@" and not re.match(r"[A-Z]", node)]
nodeq = []  # and not re.match(r"[A-Z]", node)]
heapq.heapify(nodeq)
print(parq, nodeq)

pos = "@"
target = "m"

i = 0
while i < 10:
    for neighbour, distance in nodes_dict[pos].neighbours.items():
        # print(parq.get(neighbour, 1000000))
        # print(distance+parq[pos][0])
        if parq.get(neighbour, (1000000, ""))[0] >= distance + parq[pos][0]:
            parq[neighbour] = (distance + parq[pos][0], pos)
            heapq.heappush(nodeq, neighbour)
    pos = heapq.heappop(nodeq)
    i += 1
print(parq)
exit(0)


# selected = start
# distances = {x: 1000 for x in nodes_dict}
# distances[start] = 0
# print(distances)

class Route:
    def __init__(self, ini_trace, ini_distance, ini_target, ini_origin):
        self.target = ini_target
        self.trace = ini_trace
        self.distance = ini_distance
        self.origin = ini_origin
        self.trace_set = [x for x in self.trace if re.match(r"[a-zA-Z]", str(x))]

    def __str__(self):
        return "O:" + str(self.origin) + " T:" + str(self.target) + " D:" + str(self.distance) + " Trace:" + str(
            self.trace) + " Trace_set:" + str(self.trace_set)


class routing_table:
    def __init__(self, dictionary_of_routes, owner):
        self.routes = dictionary_of_routes
        self.owner = owner

    def update_routing_table(self, new_routing_table):
        # for route_i in self.routes:
        # print(route_i.target)

        for target_key, route_itm in new_routing_table.routes.items():

            new_route = copy.deepcopy(route_itm)
            route_to_sender = copy.deepcopy(self.routes[new_routing_table.owner])

            new_route.trace.extend(route_to_sender.trace)
            new_route.distance += route_to_sender.distance
            new_route.origin = self.owner

            if target_key in self.routes:

                if self.routes[target_key].distance > new_route.distance:
                    self.routes[target_key] = new_route

            else:
                self.routes[target_key] = new_route


# BELLMAN-FORD ALGORITHM
# first initialise the routing tables
for node_key, node_value in nodes_dict.items():
    # node_t = nodes_dict[nodeXY]
    node_value.routing = routing_table(
        {x: Route([x], node_value.neighbours[x], x, node_key) for x in node_value.neighbours}, node_key)

    # print the initial routes
    # for route_key, route_value in node_value.routing.routes.items():
    #    print(route_value)

counter = 0
summation1 = 0
for routing_table_value in [nodes_dict[y].routing for y in nodes_dict]:
    # print(routing_table_t)
    for route_key, route_value in routing_table_value.routes.items():
        summation1 += route_value.distance
print(counter, summation1)

while True:  # main loop of the routing algorithm

    for node_key, node_value in nodes_dict.items():  # go through the nodes
        # node_t = nodes_dict[node_t] # get the value hiding behind the key
        table_to_share = node_value.routing
        for neighbour_key, neighbour_value in node_value.neighbours.items():  #
            # print(neighbour_k)
            # send routing table
            nodes_dict[neighbour_key].routing.update_routing_table(table_to_share)

    summation2 = 0
    for routing_table_t in [nodes_dict[y].routing for y in nodes_dict]:
        # print(routing_table_t)
        for route_t in routing_table_t.routes:
            summation2 += routing_table_t.routes[route_t].distance

    counter += 1
    print(counter, summation2)
    if summation1 == summation2:
        break
    summation1 = summation2

translation_of_node_keys = {key: val.value if val.value != "." else key for key, val in nodes_dict.items()}


# print(translation_of_node_keys)


def trans_dict_keys(dict, trans):
    """replaces dictionary keys based on provided dictionary in format oldkey:newkey
       doesn't preserve order of dictionary"""
    for oldkey, newkey in trans.items():
        try:
            dict[newkey] = dict.pop(oldkey)
        except KeyError:
            pass
    return dict


class Node_v2:
    def __init__(self, node_v1, nodes_dict):
        self.value = node_v1.value
        self.position = node_v1
        neighbours = {}
        self.id = translation_of_node_keys[node_v1.position]
        # print(self.id)
        # translate neighbours with function
        neighbours = trans_dict_keys(node_v1.neighbours, translation_of_node_keys)
        # below old way
        # for neighbour in node_v1.neighbours:
        #     if nodes_dict[neighbour].value != ".":
        #         new_nkey = nodes_dict[neighbour].value
        #         neighbours[new_nkey] = node_v1.neighbours[neighbour]
        #     else:
        #         neighbours[neighbour] = node_v1.neighbours[neighbour]

        self.neighbours = neighbours

        routes_t = {}

        # translate route names
        for key, route in node_v1.routing.routes.items():
            # prune self targeting routes

            if route.target != route.origin:
                route.trace = [translation_of_node_keys[x] for x in route.trace][-1::-1]
                route.target = translation_of_node_keys[route.target]
                route.origin = translation_of_node_keys[route.origin]
                route.trace_set = {z for z in route.trace if re.match(r"[a-zA-Z]|@", str(z))}
                route.trace = [z for z in route.trace if re.match(r"[a-zA-Z]|@", str(z))]
                routes_t[translation_of_node_keys.get(key, key)] = route

                # print(route)

        self.routes = routes_t


nodes_v2 = {}
for key, node in nodes_dict.items():
    # check node key vs value
    if node.position != key:
        print("invalid Node_v1", key, node.position)
        exit(1)
    if node.value != ".":
        new_key = node.value
    else:
        new_key = node.position

    nodes_v2[new_key] = Node_v2(node, nodes_dict)

# the hard part
# heuristic route choosing: FAILED
# algorithm get the longest passable route

silent1 = False
# initialise zmienne
keychain = {"@"}
sexpos = "@"  # simulated explorer position
distance = 0
travel = ["@"]

# all keys set
all_keys = {x for x in nodes_v2 if re.match(r"[a-z]", str(x))}

while False:
    # copy map fragment
    routes_for_anal = copy.deepcopy(nodes_v2[sexpos].routes)

    # report state
    if not silent1:
        print("====================================")
        print("I am at:", sexpos)
        print("I have following keys", keychain)

    # look at the map and filter only valid targets
    available_routes = []
    for target, route in routes_for_anal.items():
        if re.match(r"[a-z]|@", str(target)):
            index_block = len(route.trace)
            # before = copy.deepcopy(route)    #print(route)
            for i, x in enumerate(route.trace):
                if str(x).isupper() and str(x) not in keychain:
                    index_block = i
                    break
            route.trace = route.trace[:index_block]
            try:
                check = route.trace[-1] == route.target
            except IndexError:
                check = False
            if check:
                available_routes.append(route)


    # print(available_routes)
    # print(available_routes[0].trace)

    # sort by number of unclaimed keys in routes
    def unclaimed_keys(route1, keychain1):
        return len(set(route1.trace) - set({x.lower() for x in keychain1}))


    available_routes.sort(key=lambda x: unclaimed_keys(x, keychain), reverse=True)
    # print(available_routes)

    # print the available routes
    if not silent1:
        print("available routes")
        for i, x in enumerate(available_routes):
            print("    ", i, x)

    # ['@', 'a', 'b', 'd', 'e', 'd', 'f']
    manual_input = 0
    # choose next route
    if manual_input and not silent1:
        target_index = int(input("please choose target"))
        chosen_route = available_routes[target_index]
    else:
        chosen_route = available_routes[0]

    # moving

    distance += chosen_route.distance
    travel.append(chosen_route.target)
    keychain.update([x.upper() for x in chosen_route.trace if x in all_keys])
    sexpos = chosen_route.target

    if not silent1:
        print("going to:", chosen_route.target)
        print("distance:", distance)

    # break condition
    if not all_keys - {x.lower() for x in keychain}:
        # print("all_keys gathered")
        break

# print(travel)
# print(distance)

print([x for x in nodes_v2])

# dump nodes not containing keys

nodes_v3 = {key: item for key, item in nodes_v2.items() if re.match("^[a-z]$|@", str(key))}
print([x for x in nodes_v3])

for node in nodes_v3.values():
    print([x for x in node.routes])
    node.routes = {key: item for key, item in node.routes.items() if re.match("^[a-z]$|@", str(key))}
    pass

for key1, node in nodes_v3.items():
    print(key1)
    for key, route in node.routes.items():
        print(route)
        route.trace_set = {x for x in route.trace_set if re.match("^[a-zA-Z]$|@", str(x))}

    # node.routes = {key:item for key, item in  node.routes.items() if re.match("^[a-z]$|@", str(key))}

silent1 = True
# initialise zmienne
keychain = {"@"}  # will contain only lowercase
sexpos = "@"  # simulated explorer position
distance = 0
travel = ["@"]

all_keys_l = all_keys
all_keys_u = {x.upper() for x in all_keys}


# print(all_keys_u, all_keys_l)

# min_distance_so_far = 100000


# use recursion
def search_for_keys(keychain_i, route_i, nodes_i, all_keys_i, recursion_lvl, dist):
    global min_distance_so_far
    # print(recursion_lvl)
    dist = dist + route_i.distance
    if dist >= min_distance_so_far:
        return 100000
    # new_keychain
    keychain_i = keychain_i.union(route_i.trace_set)
    open_doors_i = {x.upper() for x in keychain_i}

    # print("my shiny new keychain", keychain_i)

    # check if visited all the nodes if yes return last distance travelled
    # print(all_keys_i - keychain_i)
    if not all_keys_i - keychain_i:
        print("at the end with", dist, recursion_lvl)
        if dist < min_distance_so_far:
            min_distance_so_far = dist
        return route_i.distance

    # launch search along all other routes.
    # Only those that offer new keys while, having no locked doors
    distances_i = [100000]
    # print(distances_i)

    for key, next_route in nodes_i[route_i.target].routes.items():
        # print(key, next_route)
        if re.match("^[a-x]$", str(key)):  # only those that target keys
            left_objects = next_route.trace_set - open_doors_i - keychain_i  # not visited objects
            left_doors = {x for x in left_objects if x.isupper()}  # doors not possible to open yet
            left_keys = {x for x in left_objects if x.islower()}  # keys on route not in keychain
            if left_keys and not left_doors:
                # launching
                # print("launching again to",next_route.target)
                distances_i.append(
                    search_for_keys(keychain_i, next_route, nodes_i, all_keys_i, recursion_lvl + 1, dist))
    # print("returning")
    return min(distances_i) + route_i.distance
    # return the minimum while adding distance traveled to this poin
    # distances_inner = [100000]
    # if all_keys_l - keychain_l_i:
    #     print("nodes left", all_keys_l-keychain_l_i)
    #     # print("i am going further in")
    #     for target_i, next_route in nodes_v2[route_i.target].routes.items():
    #         # print("aiming at",target)
    #         # print(route.trace_set-keychain_u-keychain_l)
    #         # sleep(0.5)
    #         # print(target not in keychain_l_i and next_route.trace_set-keychain_u_i-keychain_l_i)
    #         if target_i not in keychain_l_i and next_route.trace_set - keychain_u_i - keychain_l_i:
    #             #sleep(0.5)
    #             #print("going to '", target_i, "' to get", next_route.trace_set - keychain_u_i - keychain_l_i)
    #             distances_inner.append(search_for_keys(copy.copy(keychain_u_i), copy.copy(keychain_l_i), next_route))
    #     #print(distances_inner)
    #     #print("returning", min(distances_inner) + route_i.distance)
    #
    #     return min(distances_inner) + route_i.distance
    #     # pass # here launch next level of recursion
    # else:  # if all keys are collected
    #
    #     print("collected all keys")
    #     print("my keychain as proof", keychain_l_i)
    #     print("returning", route_i.distance)
    #     return route_i.distance
    #
    # # for route in nodes_v2:
    # # nodes_v2[origin].route


silent1 = True
# initialise zmienne
keychain_l = {"@"}  # will contain only lowercase
keychain_u = {"@"}
sexpos = "@"  # simulated explorer position
distance = 0
travel = ["@"]

route_to_entry = Route(ini_trace=[], ini_distance=0, ini_target="@", ini_origin="#")
print("\n TRYING THE RECURSION")

min_distance_so_far = 100000
distance = search_for_keys(keychain, route_to_entry, nodes_v2, all_keys, 1, 0)
print(distance)
exit(0)

distances = [100000]
for key, route in nodes_v2['@'].routes.items():
    keychain = {"@"}  # will contain only lowercase
    if re.match(r"[a-z]", str(key)):
        print(key)
        distances.append(search_for_keys(keychain, route, nodes_v2, all_keys))
    distance = min(distances) + route.distance
print(distances)
print(distance)
