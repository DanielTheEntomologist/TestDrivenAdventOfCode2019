import copy
import re
from time import sleep


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


class Node:
    def __init__(self, position, value, neighbours=None):
        self.value = value
        self.position = position
        self.routing = None
        if neighbours == None:
            self.neighbours = {}
        else:
            self.neighbours = neighbours


# start the program
# full map
map_str1 = """#########################################
#...........#.............#...#.....#...#
#.#####.###.###.#########.#.#.#.#.###.#.#
#..m#.#...#...#...#...#...#.#...#.....#.#
###.#.###.###.###.###.#.#######.#######.#
#.#...#...#.#...#...#.#.#.....#.#.......#
#.###.#.###.###.###.#.#.#.###.#.#.#####.#
#.#...#.#.....#.....#.#...#.#.#.#.#.#...#
#.#.###.###.#########.#####.#.###.#.#.###
#.#...#.#...#.........#...#.#...#.#.#.#.#
#.###.#.#.###.#####.#.#.#.#.###.#.#.#.#.#
#.#...#.#.....#.#...#...#.#...#...#.#.#.#
#V#.###.#.#####.#.#######.#.#.#####.#.#.#
#...#...#.....#.#.#.......#.#.......#.#.#
#####.#######.#.#.#######.###.#####.#.#.#
#...#...#.......#.......#.....#.....#.#.#
#.#.###.###.#######.###.#######.#####.#.#
#.#...#...#.#.....#...#.#...#.#.....#...#
#.###.###.###.###.###.#.#.#.#.###.#####.#
#.#.......#...#.#...#.#...#.#.....#...#.#
#.#######.#.###.###.###.###.#######.#.#.#
#.T.#.....#.#.....#...#...#.........#...#
###.#.#####.#.#.#########.###############
#.#.#...#...#.#.........#...#.........#.#
#.#.#####.###.#####.#######.#######.#.#.#
#.#......l#.#.....#.......#.........#...#
#.#########.#.#########.#.#############.#
#.....#.....#.#...#...#.#...#.......#..z#
#.###.#.###.#.#.#.#.#.###.#.#.###.#.#.###
#...#.#.#.#...#.#.#.#...#.#.#.#...#.#...#
###.###.#.#####.#.#.###.#.#.###.#.#####.#
#...#..d#.#...#.#.#...#...#...#.#.#.....#
#.#.#.###.#.#.#.#.###.#######.#.#.#.#####
#.#.#...#.#.#...#.#...#.........#.#.#...#
#.#####.#.#.#####.#.#######.#######.#.###
#.......#.#...#...#.#.....#.#.......#...#
#.#######.###.###.#.#.###.###.#######.#.#
#.......#...#...#...#.#.#...#.#...#...#.#
#######.#.#.###.#####.#.###.#.#.#.#####.#
#.........#...#...........#.....#......@#
#########################################
"""
map_str2 ="""#########################################
#...........#.........#.C.........#....@#
#Q#########.#.#.#####.#.#########.#.###.#
#.#.........#.#...#.#...#.......#.#.#.#.#
#.#####.#########.#.#####.#####.#.#.#.#.#
#.....#.#.....#...#.....#.#...#.#...#.#.#
#.###.#U#.###.#.#####.###.#.###.#####.#.#
#j..#.#...#...#.....#.#...#...#.....#.#.#
###.#.#####.#######.#.#.#####.###.#.#.#.#
#...#.....#.....#...#.#...#...#...#.#.#.#
#######.#.#####.#.###.###.#.#.#.###.#.#.#
#.....#.#...#.#.#.#.....#.#.#.#.#.....#.#
#.###.#.###.#.#.#.###.#.#.#.#.#.#######.#
#f#.#.#.#...#.#.#...#.#.#b#.#.#.#.......#
#.#.#.###.###.#.###.#.#.#.#.###.#.#######
#.#.......#...#.#...#.#...#...#...#.....#
#.#########.#.#.#.###.#######.#######.###
#.....#.....#.....#....x....#.......#...#
#.###.#####.###############.###.###.###.#
#...#.....#.#r..........#.#.....#.#...#.#
#.#######.###.#########R#.#######.###.#.#
#.#.......#...#....g#...#.........#...#.#
#.#.#######.#######.#####.#.#######.###.#
#.#...#...#...#.....#.....#.......#...#.#
#.###.#.#.###G#.###I#.###########.###.#.#
#k#...#.#...#...#...#.....#s....#.#...#.#
###.#.#.###.#####.#######.#.###O#.#.###.#
#..p#.#...#.....#.......#.#.#...#.#.....#
#.###.###.###.#########.###.#.###.#####.#
#.#.#...#...#.......#..i#...#...#.#.....#
#.#.###.#.#######.#.#H###.#####.#.#.#####
#.#.....#.#.....#.#.#.#...#o....#.#.#...#
#.#######.#.###.###.#.#S#####.###.#.###.#
#.#.......#.#.......#.#.....#.A.#.....#.#
#.#.#######.#######.#.#####.###.#####.#.#
#.#...#...#.#.Y.#...#..h....#.#...#.#.#.#
#.###.#.#.#.#.#.#############.###.#.#.#.#
#...#...#.#...#...........#.......#.#.#.#
#.#.#####.###########.#####.#######.#.#.#
#.#.....M...........#e......#...........#
#########################################"""

map_str3 = """#########################################
#@....#.........#.....................X.#
#.###.#.#######.#.###############.#####.#
#...#.....#...#.#.....#.#.......#...#...#
###.#######.#.#.#####.#.#.#####.#.###.#.#
#.#.#...#...#...#.....#.#.#.....#.#u..#.#
#.#.###.#.#.#####.#####.#.#.#######.###.#
#.#.....#.#.#.....#.....#.#.........#...#
#.#####.#.###.#####.###.#.#####.#######.#
#...#...#.....#.....#...#.#...#.#.....#.#
###.#.#########.#####.###.#.#.###.###.###
#...#.#.....#...#.....#.#...#.......#...#
#.###.###.#.###.#.#####.###########.###.#
#.#...#...#.#...#.....#...#.....#...#...#
#.#.###.###.#.#######.###.#.###.#####.#.#
#...#...#.....#...........#.#.#.#.....#.#
#.###.#.#######.###########.#.#.#.#####.#
#n#...#.#.....#.....#.....#.#.#.F.#...#.#
#.###.###.###.#######.###.#.#.#####.###.#
#.....#...#...........#...#.#.#.........#
#####.#.###.###########.###K#.#.#########
#.....#.#...#.......#.#.....#.#...#.....#
#.#####.#.###.#####.#.#######.###.#.#.###
#...#.#.#.#...#...#.#.#.#...#.....#.#...#
###.#.#.#.#.#####.#.#.#.#.#.#.#####.###.#
#...#.#.#.#.......#...#...#.#.#.#...#.L.#
#.###.#.#.#######.#####.###.#.#.#.###.#.#
#.Z...#.#...#...#.#...#.#.#...#.#...#.#.#
#######.###.###.#.#.#.#.#.#####.###.#.###
#.....#.#.#.....#.#.#...#....a....#.#...#
#.###.#.#.#.#####.#.#####.#.#######.###.#
#...#...#...#.....#.#...E.#.#......y..#.#
#.#.###.#####W#####.#.#.###.#.#########.#
#.#.#...#...#...#...#.#.#...#.#...#.....#
###.#.###.#.###.#.###.#.#####.###.#.###.#
#...#...#.#.....#.#...#...........#...#.#
#.###.###.#######.#############.#####.#.#
#.#...#...#.....#...#.........#.#.....#.#
#.#####.###.#######.#.#######.###.#####.#
#.......#.............#...........#.....#
#########################################"""

map_str4 = """#########################################
#...............#.....#.....#....t#.....#
#.#####.#######.#.###.#.###.#.###.#.#.#.#
#.....#...#...#...#...#...#...#...#.#.#.#
#######.#.#.#.#####.#####.#####.###.#.#.#
#.....#.#...#.....#.#...#...#.#...#.#.#.#
#.###.###########.#.#.#.###.#.###.#.#.#.#
#...#...B.........#...#.J.#.#...#.#.#.#.#
###.#####################.#.###.#.###.#.#
#...#.............#...#...#.#...#....v#.#
#.###.###########.#.#.#.###.#.#########P#
#...#.....#...#...#.#...#w..#.#...#.....#
#.#.#####.#.#.#.###.#####.###.#.#.#.#####
#.#.#.....#.#.#.#.#.#...#.#...#.#.#.....#
#.#.#.#####.#.#.#.#.###.#.#.###.#.#####.#
#.#.#...#...#.....#.....#.#.#...#...#...#
#.#N#.#.#########.###.###.#.#.###.###.###
#.#.#.#...#.....#.#...#...#...#.#...#.#.#
###.#.###.#.###.###.###.###.###D###.#.#.#
#...#.#...#...#.#...#...#.#.#.....#.#...#
#.###.#.#####.#.#.###.###.#.#.###.#.###.#
#.#...#.....#.#.....#.#...#.#.#...#.....#
#.#########.#.###########.#.#.###########
#...#.....#.....#.........#.#...........#
###.#.###.#######.#####.###.#####.#######
#...#.#.#.#.....#...#.#...#.....#...#...#
#.###.#.#.#.###.###.#.###.#####.#.#.#.#.#
#.....#.#...#.....#.#...#.......#.#...#.#
#.#####.#####.#####.#.#.#########.#####.#
#.#.........#.....#...#.#...#.....#.....#
#.#######.#.#####.#####.#.#.#.#####.###.#
#.....#...#.....#.....#...#.#...#q..#.#.#
#####.#.###########.#.#####.#####.###.#.#
#.#...#...........#.#.....#...#...#...#.#
#.#.###.#########.#.#####.###.#.#####.#.#
#.#.#.....#.....#.#...#...#...#.....#...#
#.#.#####.#.#####.###.#####.#######.#####
#.#.#...#...#...#...#.....#.#.....#.....#
#.#.#.#.#####.#.###.#####.#.#.###.#####.#
#@....#....c..#.........#.....#.........#
#########################################"""

map_str_list = map_str4.split("\n")

print(520+580+364+352)

map_dict = {}  # defaultdict()

# translate the result to the explored_dict
for y, line in enumerate(map_str_list):
    for x, char in enumerate(line):
        map_dict[(x, y)] = char

# display_board([map_dict], [{}], " ")

start, = [x for x in map_dict if map_dict[x] == "@"]
print("@ is at position", start)
print("count of chars in map", len(map_dict))
# def explore(start,list)

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
print("shaving bridges")
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
nodes_map_dict = {x: nodes_dict[x].value for x in nodes_dict}
display_board([nodes_map_dict], [{}], " ")

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
nodes_map_dict = {x: nodes_dict[x].value for x in nodes_dict}
display_board([nodes_map_dict], [{}], " ")

# shave bridges left after dead ends
print("shave the bridges left after removing dead ends")
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

nodes_map_dict = {x: nodes_dict[x].value for x in nodes_dict}
display_board([nodes_map_dict], [{}], " ")

for x in nodes_dict:
    print(nodes_dict[x].value, nodes_dict[x].neighbours)

start, = [x for x in nodes_dict if nodes_dict[x].value == "@"]
print("\n")
print("@ is at position", start)


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

cache = {}

# use recursion
def search_for_keys(keysleft_i, node_i):

    # print(recursion_lvl)
    # dist = dist + route_i.distance
    # if dist >= min_distance_so_far:
    #    return 100000
    # new_keychain

    keyset = (node_i.value, frozenset(keysleft_i))
    if keyset in cache:
        return cache[keyset]

    if not keysleft_i:
        cache[keyset] = 0
        return 0

    min_returned = float('inf')

    for key,route in node_i.routes.items():
        doors = {x.lower() for x in route.trace_set if x.isupper()}
        #print(doors)
        if keysleft_i.isdisjoint(doors) and route.target.lower() in keysleft_i :    # if keys left do not match any door

            temp_dist = route.distance+search_for_keys(keysleft_i - {key.lower()}, nodes_v3[route.target])
            if temp_dist < min_returned:
                min_returned = temp_dist
            #keysleft_i = keysleft_i.subtract(node_i.value)
    cache[keyset] = min_returned

    return min_returned

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
distance = search_for_keys(all_keys, nodes_v3["@"])
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
