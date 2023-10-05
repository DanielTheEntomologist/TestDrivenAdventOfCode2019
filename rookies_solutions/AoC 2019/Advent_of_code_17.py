# import pandas as pd
# import easygui
# import os
# import math
import copy
# import time
# from pathlib import PureWindowsPath
from collections import deque
# from collections import defaultdict
# from collections import Counter
# import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import re


def constant_factory():
    return lambda: " "


def display_board(board_dict_list, translation_list, empty_space):  # xmin,ymax_,xmin=None,ymin,
    xmax, xmin = max([x for x, y in board_dict_list[0].keys()]), min([x for x, y in board_dict_list[0].keys()])
    ymax, ymin = max([y for x, y in board_dict_list[0].keys()]), min([y for x, y in board_dict_list[0].keys()])

    # board_dict_copy = board_dict.copy()

    board_dict_copy_list = []

    for board_dict in board_dict_list:
        # buffer_dict = defaultdict(constant_factory())
        # print(board_dict, xmax, xmin, ymax, ymin)
        # translate by xmin,ymin

        temp = {((x - xmin, y - ymin)): board_dict[(x, y)] for x, y in board_dict.keys()}
        board_dict_copy_list.append(temp)

    # buffer_dict.update(board_dict_copy)

    # initiate display
    display = [[empty_space for i in range(xmax - xmin + 1)] for j in range(ymax - ymin + 1)]
    # print("display size x,y initiated in display", len(display[0]), len(display))

    for i, board_dict_copy in enumerate(board_dict_copy_list):
        for y in range(ymax - ymin, -1, -1):  # reverse to display from top to bottom
            line = []
            for x in range(xmax - xmin + 1):
                try:
                    char = str([translation_list[i].get(n, n) for n in [board_dict_copy[(x, y)]]][0])
                    display[y][x] = char
                except KeyError:
                    pass  # char = " "
                # char = str(map({1: "_", 0: '#'}, [board_dict_copy[(x, y)]]))

                # pass #line.append([buffer_dict[(x-xmin,y-ymin)] ])
    #                except KeyError:
    #                   line.append(" ")
    # print(line)
    # display.append(line)
    # pass
    for screenline in display:
        print("".join(screenline))
    print("===================================================================")
    return None


def decode_opcode(opcode_int):
    # print("decoding opcode:", opcode_int)
    opcode_str = str(opcode_int)
    lenght_of_instruction = 5
    r_inst = opcode_str[-1::-1] + "0" * (lenght_of_instruction - len(opcode_str))
    # print(r_inst)
    opcode_int = int(r_inst[1::-1])  # [int(x) for x in r_inst[1::-1]]
    modes_int = [int(b) for b in r_inst[2:]]

    # print("obtained opcode", opcode, " with modes", modes)

    return opcode_int, modes_int


def pointers_get(parameters, modes, pos, rel_pos, mem):
    # INPUT: list of parameters , string of modes
    # OUTPUT: list of addreses on which to perform operations

    # print("read parameters:", parameters)

    pointers = []
    for m, parameter in enumerate(parameters):
        if modes[m] == 0:
            pointers.append(parameter)
        elif modes[m] == 1:
            pointers.append(pos + 1 + m)
        elif modes[m] == 2:
            pointers.append(parameter + rel_pos)
        else:
            print("ERROR - invalid mode read in:", modes)
            exit(0)

    overflow = max(pointers) - len(mem) + 1
    if overflow > 0:
        mem.extend([0] * overflow)
    # print("obtained pointers:", pointers)
    if min(pointers) < 0:
        print("ERROR - trying to use negative address with:", pointers)
    return pointers


def init_command(pos, length, modes, mem, rel_pos):
    parameters = mem[pos + 1:pos + length]
    pointers = pointers_get(parameters, modes, pos, rel_pos, mem)
    return pointers


def stepper_computer(mem, input_list, starting_pos=0, relative_pos=0):
    pos = starting_pos
    rel_pos = relative_pos
    # print("initialised with position", pos)
    # print("initialised with relative position", rel_pos)
    # print("initialised with input list", input_list)
    # print( "starting pos", pos)
    if isinstance(input_list, list):
        input_x = iter(input_list)
    else:
        input_x = iter([input_list])
    output_list = []

    while True:
        # print("starting at position ", pos)
        # print("next 4 positions in mem are", mem[pos:pos + 4])
        jump = False
        opcode, modes = decode_opcode(mem[pos])
        # print(opcode, modes)
        # print("opcode",opcode)
        if opcode == 99:  # halt
            # length = 1
            # output_list.append("halted")
            unconsumed_inputs = list(deque(input_x))
            return mem, unconsumed_inputs, pos, rel_pos, output_list, "halted"
        elif opcode == 1:  # addition
            length = 4
            pointers = init_command(pos, length, modes, mem, rel_pos)
            mem[pointers[2]] = int(mem[pointers[1]]) + int(mem[pointers[0]])
            # print("new value at final adress should be:", int(mem[pointers[1]]) + int(mem[pointers[0]]))
            # print("new value at final adress is:", mem[pointers[2]])
        elif opcode == 2:  # multiplication
            length = 4
            pointers = init_command(pos, length, modes, mem, rel_pos)
            mem[pointers[2]] = int(mem[pointers[1]]) * int(mem[pointers[0]])

        elif opcode == 3:  # input
            length = 2
            pointers = init_command(pos, length, modes, mem, rel_pos)
            try:
                temp = next(input_x)
                mem[pointers[0]] = int(temp)
            except StopIteration:
                #    print("Intcomp waiting for input")
                # pos = pos  # + length
                unconsumed_inputs = []
                return mem, unconsumed_inputs, pos, rel_pos, output_list, "waiting for input"
            # int(input("provide input\n"))
            # mem[pointers[0]] = int(100 * input_1 + input_2)
            # mem[parameters[1]] = mem[0]
            # pos = pos + length
        elif opcode == 4:  # output
            length = 2
            pointers = init_command(pos, length, modes, mem, rel_pos)
            # print("output", mem[pointers[0]])
            output_list.append(mem[pointers[0]])
            # print("Intcomp returning output")
            # pos = pos + length
            # print("going to pos", pos)
            # print("suspended with position", pos)
            # print("suspended with relative position", rel_pos)
            # print("suspended with input list", input_x)

            # unconsumed_inputs = list(deque(input_x))
            # return mem, unconsumed_inputs, pos, rel_pos, output_list, "waiting to resume after output"
        elif opcode == 5:  # jump if true
            length = 3
            pointers = init_command(pos, length, modes, mem, rel_pos)
            if mem[pointers[0]] != 0:
                pos = mem[pointers[1]]
                jump = True
        elif opcode == 6:  # jump to parameter 2 if param 1 == 0
            length = 3
            pointers = init_command(pos, length, modes, mem, rel_pos)
            if mem[pointers[0]] == 0:
                pos = mem[pointers[1]]
                jump = True
        elif opcode == 7:  # 1 in parameter 3 if parameters 1<2
            length = 4
            pointers = init_command(pos, length, modes, mem, rel_pos)
            if mem[pointers[0]] < mem[pointers[1]]:
                mem[pointers[2]] = 1
            else:
                mem[pointers[2]] = 0
        elif opcode == 8:  # 1 in parameter 3 if parameters 1==2
            length = 4
            pointers = init_command(pos, length, modes, mem, rel_pos)
            if mem[pointers[0]] == mem[pointers[1]]:
                mem[pointers[2]] = 1
            else:
                mem[pointers[2]] = 0
        elif opcode == 9:  # change relative postion
            length = 2
            pointers = init_command(pos, length, modes, mem, rel_pos)
            rel_pos = rel_pos + mem[pointers[0]]
        else:

            print("no valid opcode detected exiting")
            unconsumed_inputs = list(deque(input_x))
            return mem, unconsumed_inputs, pos, rel_pos, output_list, "error"

        if not jump:
            pos = pos + length


# Scaffolding Cameras
program = [1, 330, 331, 332, 109, 3652, 1102, 1182, 1, 16, 1101, 0, 1447, 24, 102, 1, 0, 570, 1006, 570, 36, 1001, 571,
           0, 0, 1001, 570, -1, 570, 1001, 24, 1, 24, 1105, 1, 18, 1008, 571, 0, 571, 1001, 16, 1, 16, 1008, 16, 1447,
           570, 1006, 570, 14, 21101, 58, 0, 0, 1106, 0, 786, 1006, 332, 62, 99, 21101, 333, 0, 1, 21101, 0, 73, 0,
           1106, 0, 579, 1102, 0, 1, 572, 1102, 0, 1, 573, 3, 574, 101, 1, 573, 573, 1007, 574, 65, 570, 1005, 570, 151,
           107, 67, 574, 570, 1005, 570, 151, 1001, 574, -64, 574, 1002, 574, -1, 574, 1001, 572, 1, 572, 1007, 572, 11,
           570, 1006, 570, 165, 101, 1182, 572, 127, 1002, 574, 1, 0, 3, 574, 101, 1, 573, 573, 1008, 574, 10, 570,
           1005, 570, 189, 1008, 574, 44, 570, 1006, 570, 158, 1105, 1, 81, 21102, 1, 340, 1, 1106, 0, 177, 21102, 477,
           1, 1, 1106, 0, 177, 21101, 514, 0, 1, 21101, 176, 0, 0, 1105, 1, 579, 99, 21101, 184, 0, 0, 1106, 0, 579, 4,
           574, 104, 10, 99, 1007, 573, 22, 570, 1006, 570, 165, 101, 0, 572, 1182, 21101, 0, 375, 1, 21102, 1, 211, 0,
           1105, 1, 579, 21101, 1182, 11, 1, 21101, 222, 0, 0, 1105, 1, 979, 21101, 388, 0, 1, 21101, 0, 233, 0, 1105,
           1, 579, 21101, 1182, 22, 1, 21102, 244, 1, 0, 1106, 0, 979, 21101, 0, 401, 1, 21101, 255, 0, 0, 1105, 1, 579,
           21101, 1182, 33, 1, 21101, 266, 0, 0, 1106, 0, 979, 21101, 414, 0, 1, 21101, 277, 0, 0, 1106, 0, 579, 3, 575,
           1008, 575, 89, 570, 1008, 575, 121, 575, 1, 575, 570, 575, 3, 574, 1008, 574, 10, 570, 1006, 570, 291, 104,
           10, 21102, 1182, 1, 1, 21101, 0, 313, 0, 1106, 0, 622, 1005, 575, 327, 1101, 1, 0, 575, 21102, 1, 327, 0,
           1105, 1, 786, 4, 438, 99, 0, 1, 1, 6, 77, 97, 105, 110, 58, 10, 33, 10, 69, 120, 112, 101, 99, 116, 101, 100,
           32, 102, 117, 110, 99, 116, 105, 111, 110, 32, 110, 97, 109, 101, 32, 98, 117, 116, 32, 103, 111, 116, 58,
           32, 0, 12, 70, 117, 110, 99, 116, 105, 111, 110, 32, 65, 58, 10, 12, 70, 117, 110, 99, 116, 105, 111, 110,
           32, 66, 58, 10, 12, 70, 117, 110, 99, 116, 105, 111, 110, 32, 67, 58, 10, 23, 67, 111, 110, 116, 105, 110,
           117, 111, 117, 115, 32, 118, 105, 100, 101, 111, 32, 102, 101, 101, 100, 63, 10, 0, 37, 10, 69, 120, 112,
           101, 99, 116, 101, 100, 32, 82, 44, 32, 76, 44, 32, 111, 114, 32, 100, 105, 115, 116, 97, 110, 99, 101, 32,
           98, 117, 116, 32, 103, 111, 116, 58, 32, 36, 10, 69, 120, 112, 101, 99, 116, 101, 100, 32, 99, 111, 109, 109,
           97, 32, 111, 114, 32, 110, 101, 119, 108, 105, 110, 101, 32, 98, 117, 116, 32, 103, 111, 116, 58, 32, 43, 10,
           68, 101, 102, 105, 110, 105, 116, 105, 111, 110, 115, 32, 109, 97, 121, 32, 98, 101, 32, 97, 116, 32, 109,
           111, 115, 116, 32, 50, 48, 32, 99, 104, 97, 114, 97, 99, 116, 101, 114, 115, 33, 10, 94, 62, 118, 60, 0, 1,
           0, -1, -1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 18, 40, 0, 109, 4, 2102, 1, -3, 587, 20101, 0, 0, -1, 22101, 1, -3, -3,
           21102, 1, 0, -2, 2208, -2, -1, 570, 1005, 570, 617, 2201, -3, -2, 609, 4, 0, 21201, -2, 1, -2, 1105, 1, 597,
           109, -4, 2105, 1, 0, 109, 5, 2101, 0, -4, 630, 20102, 1, 0, -2, 22101, 1, -4, -4, 21102, 1, 0, -3, 2208, -3,
           -2, 570, 1005, 570, 781, 2201, -4, -3, 653, 20102, 1, 0, -1, 1208, -1, -4, 570, 1005, 570, 709, 1208, -1, -5,
           570, 1005, 570, 734, 1207, -1, 0, 570, 1005, 570, 759, 1206, -1, 774, 1001, 578, 562, 684, 1, 0, 576, 576,
           1001, 578, 566, 692, 1, 0, 577, 577, 21102, 702, 1, 0, 1106, 0, 786, 21201, -1, -1, -1, 1105, 1, 676, 1001,
           578, 1, 578, 1008, 578, 4, 570, 1006, 570, 724, 1001, 578, -4, 578, 21101, 731, 0, 0, 1105, 1, 786, 1105, 1,
           774, 1001, 578, -1, 578, 1008, 578, -1, 570, 1006, 570, 749, 1001, 578, 4, 578, 21101, 0, 756, 0, 1105, 1,
           786, 1105, 1, 774, 21202, -1, -11, 1, 22101, 1182, 1, 1, 21102, 1, 774, 0, 1106, 0, 622, 21201, -3, 1, -3,
           1106, 0, 640, 109, -5, 2105, 1, 0, 109, 7, 1005, 575, 802, 20102, 1, 576, -6, 20102, 1, 577, -5, 1106, 0,
           814, 21101, 0, 0, -1, 21102, 0, 1, -5, 21102, 1, 0, -6, 20208, -6, 576, -2, 208, -5, 577, 570, 22002, 570,
           -2, -2, 21202, -5, 49, -3, 22201, -6, -3, -3, 22101, 1447, -3, -3, 1202, -3, 1, 843, 1005, 0, 863, 21202, -2,
           42, -4, 22101, 46, -4, -4, 1206, -2, 924, 21102, 1, 1, -1, 1106, 0, 924, 1205, -2, 873, 21102, 35, 1, -4,
           1106, 0, 924, 1201, -3, 0, 878, 1008, 0, 1, 570, 1006, 570, 916, 1001, 374, 1, 374, 2101, 0, -3, 895, 1101,
           2, 0, 0, 2102, 1, -3, 902, 1001, 438, 0, 438, 2202, -6, -5, 570, 1, 570, 374, 570, 1, 570, 438, 438, 1001,
           578, 558, 921, 21001, 0, 0, -4, 1006, 575, 959, 204, -4, 22101, 1, -6, -6, 1208, -6, 49, 570, 1006, 570, 814,
           104, 10, 22101, 1, -5, -5, 1208, -5, 45, 570, 1006, 570, 810, 104, 10, 1206, -1, 974, 99, 1206, -1, 974,
           1102, 1, 1, 575, 21101, 0, 973, 0, 1106, 0, 786, 99, 109, -7, 2105, 1, 0, 109, 6, 21102, 1, 0, -4, 21101, 0,
           0, -3, 203, -2, 22101, 1, -3, -3, 21208, -2, 82, -1, 1205, -1, 1030, 21208, -2, 76, -1, 1205, -1, 1037,
           21207, -2, 48, -1, 1205, -1, 1124, 22107, 57, -2, -1, 1205, -1, 1124, 21201, -2, -48, -2, 1106, 0, 1041,
           21101, 0, -4, -2, 1105, 1, 1041, 21102, 1, -5, -2, 21201, -4, 1, -4, 21207, -4, 11, -1, 1206, -1, 1138, 2201,
           -5, -4, 1059, 1202, -2, 1, 0, 203, -2, 22101, 1, -3, -3, 21207, -2, 48, -1, 1205, -1, 1107, 22107, 57, -2,
           -1, 1205, -1, 1107, 21201, -2, -48, -2, 2201, -5, -4, 1090, 20102, 10, 0, -1, 22201, -2, -1, -2, 2201, -5,
           -4, 1103, 2101, 0, -2, 0, 1105, 1, 1060, 21208, -2, 10, -1, 1205, -1, 1162, 21208, -2, 44, -1, 1206, -1,
           1131, 1105, 1, 989, 21102, 439, 1, 1, 1106, 0, 1150, 21102, 477, 1, 1, 1105, 1, 1150, 21101, 0, 514, 1,
           21101, 0, 1149, 0, 1105, 1, 579, 99, 21101, 1157, 0, 0, 1106, 0, 579, 204, -2, 104, 10, 99, 21207, -3, 22,
           -1, 1206, -1, 1138, 1201, -5, 0, 1176, 2101, 0, -4, 0, 109, -6, 2106, 0, 0, 18, 5, 44, 1, 3, 1, 36, 11, 1, 1,
           36, 1, 7, 1, 1, 1, 1, 1, 36, 1, 7, 9, 32, 1, 9, 1, 1, 1, 3, 1, 32, 13, 3, 1, 42, 1, 5, 1, 42, 1, 5, 1, 42, 1,
           5, 1, 42, 1, 5, 1, 15, 5, 22, 1, 5, 1, 15, 1, 3, 1, 22, 1, 5, 1, 15, 1, 3, 1, 22, 1, 5, 1, 15, 1, 3, 1, 16,
           7, 5, 9, 7, 1, 3, 1, 16, 1, 19, 1, 7, 1, 3, 1, 16, 1, 19, 1, 7, 1, 3, 1, 16, 1, 19, 1, 7, 1, 3, 1, 16, 1, 19,
           1, 7, 1, 1, 5, 14, 1, 19, 1, 7, 1, 1, 1, 1, 1, 1, 1, 14, 1, 19, 13, 1, 1, 14, 1, 27, 1, 1, 1, 3, 1, 4, 11,
           27, 7, 4, 1, 39, 1, 8, 1, 21, 11, 7, 1, 8, 1, 21, 1, 9, 1, 7, 1, 4, 7, 19, 1, 5, 13, 4, 1, 3, 1, 21, 1, 5, 1,
           3, 1, 12, 1, 3, 1, 21, 1, 5, 1, 3, 1, 12, 1, 3, 1, 21, 1, 5, 1, 3, 1, 12, 5, 21, 1, 5, 1, 3, 1, 38, 1, 5, 1,
           3, 1, 32, 7, 5, 1, 3, 1, 32, 1, 11, 1, 3, 1, 32, 1, 11, 1, 3, 1, 32, 1, 11, 1, 3, 1, 32, 1, 11, 5, 32, 1, 48,
           1, 48, 1, 46, 13, 38, 1, 9, 1, 38, 1, 9, 1, 38, 1, 9, 1, 38, 11, 18]

# initiate the intcomp - modified to run until halted or run out of inputs
mem_out = copy.copy(program)  # memory outside of running intcopm
inputs_out = [0]  # input list
pos_out = 0  # starting position of memory intcomp
rel_pos_out = 0  # relative position for relative mode

# initiate state and outputs list
outputs = []
state = "running"

# inititate world - overlay
position = (0, 0)
explored_dict = {}
track = []  # defaultdict(constant_factory())

# initiate trackers for display
track_dict = {}
start_dict = {(0, 0): 1}
position_dict = {position: 1}

# translations for display layers
explored_t = {1: " ", 0: '#'}
position_t = {1: "B"}
track_t = {1: "."}
start_t = {1: "X"}
empty = "+"
translations = [explored_t, track_t, start_t, position_t]

# helper variables
# vectors = {1: (0, 1), 2: (0, -1), 3: (-1, 0), 4: (1, 0)}
# directions = {1: "UP", 2: "DOWN", 3: "LEFT", 4: "RIGHT"}

# try to move the bot in direction
mem_out, inputs_out, pos_out, rel_pos_out, last_output, state = stepper_computer(mem_out, inputs_out, pos_out,
                                                                                 rel_pos_out)

result = "".join([chr(x) for x in last_output])
# print(result)
result = result.split("\n")

# translate the result to the explored_dict
for y, line in enumerate(result):
    for x, char in enumerate(line):
        explored_dict[(x, y)] = char

counter = 0
for (x, y), char in explored_dict.items():

    check_for_interesection = [explored_dict.get((x, y), 0) in ["#", "<", ">", "v", "^", "I"],
                               explored_dict.get((x, y - 1), 0) in ["#", "<", ">", "v", "^", "I"],
                               explored_dict.get((x, y + 1), 0) in ["#", "<", ">", "v", "^", "I"],
                               explored_dict.get((x - 1, y), 0) in ["#", "<", ">", "v", "^", "I"],
                               explored_dict.get((x + 1, y), 0) in ["#", "<", ">", "v", "^", "I"]]
    if all(check_for_interesection):
        counter += x * y
    # if explored_dict

print(counter)
# display_board([explored_dict], [{}], " ")

# helper variables
vectors = {1: (0, 1), 2: (0, -1), 3: (-1, 0), 4: (1, 0)}
directions = {1: "UP", 2: "DOWN", 3: "LEFT", 4: "RIGHT"}

index_of_starting_position = list(explored_dict.values()).index("^")
key_of_starting_position = list(explored_dict.keys())[index_of_starting_position]

position = key_of_starting_position

instruction = []
distance = 0
vector = (0, -1)

while any([x == "#" for x in explored_dict.values()]):

    # REPORTING
    # print("instruction so far", instruction)
    # display_board([explored_dict], [{}], " ")
    # input("to continue enter")

    # mark explored get new target position
    explored_dict[position] = "C"
    target_xy = (position[0] + vector[0], position[1] + vector[1])

    # report
    # print("position",position)
    # print("target", target_xy)

    if explored_dict.get(target_xy, 0) in ["#", "C"]:
        # explored_dict[position] = "C"

        position = target_xy
        distance += 1
        instruction.append("F")
    else:
        # check if should rotate to the right or to the left
        vectorr = (-vector[1], vector[0])
        vectorl = (vector[1], -vector[0])
        target_xy_l = (position[0] + vectorl[0], position[1] + vectorl[1])
        target_xy_r = (position[0] + vectorr[0], position[1] + vectorr[1])
        char_l = explored_dict.get(target_xy_l, 0)
        char_r = explored_dict.get(target_xy_r, 0)
        if char_l in ["#", "C"] and char_r not in ["#", "C"]:
            # instruction.extend(str(distance)+",")
            #instruction.append(distance)
            distance = 0
            # instruction.extend(["L",","])
            instruction.append("L")
            vector = vectorl
        elif char_l not in ["#", "C"] and char_r in ["#", "C"]:
            # instruction.extend(str(distance)+",")
            #instruction.append(distance)
            distance = 0
            # instruction.extend(["R",","])
            instruction.append("R")
            vector = vectorr
        elif char_l in ["#", "C"] and char_r in ["#", "C"]:
            print("Error. Turning at intersection")
            display_board([explored_dict], [{}], " ")
            exit(0)
        else:
            print("At the end of the road")
            # instruction.extend([x+"," for x in str(distance)])
            # instruction.append(distance)
            # instruction.append("F")
            break

# got instruction the roadmap.
print(instruction)

inst_str = "".join(str(x) for x in instruction[2:-1:1])
print(inst_str)

leng = len(inst_str)
sequences = []
sequences_cont = []
for i in range(leng - 1):
    offset = (inst_str * 2)[i + 1:leng + i + 1]
    similarity = "".join(["1" if x == y else "0" for x, y in zip(inst_str, offset)])
    # print(similarity)
    answer = re.finditer("1{3,}", similarity)  # re.findall("1{4,}", similarity, flags=0)
    spans = [(m.start(0), m.end(0)) for m in answer]
    sequences.extend([inst_str[s[0] + 1:s[1]] for s in spans])
    sequences_cont.extend([inst_str[s[0] - 2:s[1] + 2] for s in spans])
# print(sequences)

sequences_fiiltered = [x for x in sequences if (len(x) <= 20)]  # and len(x) > 6
print(len(sequences_fiiltered))
sequences_fiiltered = set(sequences_fiiltered)
print(len(sequences_fiiltered))
print(sequences_fiiltered)

solution1 = ["","",""]
position_sim = 0

print(instruction)
#instruction = instruction[1:]
print(instruction)
instruction_str = "".join([str(x) for x in instruction])

max_matched_length = 0
# bet on sequence lenght.
# sequence lenght can be at most 20/3= 7
for alen in range(42, 43, 1):
    for blen in range(27, 28, 1):
        for clen in range(26, 27, 1):

            print(alen, blen, clen)

            position_sim = 0
            solution1 = []
            solution2 = []
            potentials_counter = 0
            sequences = ["","",""]
            while True:

                if len(solution1) > 11:
                    break
                solution1_str = "".join([str(y) for x in solution1 for y in x])
                #print(solution1_str)
                #print(instruction_str)

                #print([x == y for x, y in zip(solution1_str, instruction_str)])

                if len(solution1_str) > max_matched_length:
                    max_matched_length = len(solution1_str)
                    max_matched_sequences = sequences
                    max_matched_solution = solution1_str

                # input("enter to continue\n")

                if "".join([str(x) for x in solution1]) == "".join([str(x) for x in instruction]):
                    print("I found the solution")
                    print("sequences",sequences)
                    print("solution1", solution1)
                    print("solution2",solution2)

                # first check if new sequence is needed
                # read ahead
                apotential = instruction[position_sim:position_sim + alen]
                bpotential = instruction[position_sim:position_sim + blen]
                cpotential = instruction[position_sim:position_sim + clen]

                apotential_str = "".join([str(x) for x in apotential])
                bpotential_str = "".join([str(x) for x in bpotential])
                cpotential_str = "".join([str(x) for x in cpotential])

                #potentials = {1: apotential_str, 2: bpotential_str, 3: cpotential_str}
                potentials = [ apotential_str,  bpotential_str,  cpotential_str]
                letters = ["A","B","C"]
                #print("potentials:\n", potentials)
                #print("sequences\n", sequences)

                # does any sequence match road ahead?
                #try:
                for i,potential in enumerate(potentials):
                    # todo check by zipping
                    check1 = potentials[i] == sequences[i]
                    if check1:
                        solution1.append(sequences[i])
                        solution2.append(letters[i])
                        position_sim = position_sim + len(sequences[i])
                        break

                    # key = next(x for x in potentials.keys() if x in sequences)
                    # solution1.append(potentials[key])
                    # position_sim = position_sim + len(potentials[key])
                #except StopIteration:



                else:
                    if potentials_counter < 3:
                        index1 = sequences.index("")
                        item = potentials[index1]
                        #print("no sequence matching appending sequence:", item)
                        sequences[index1]=item
                        solution1.append(item)
                        solution2.append(letters[index1])
                        position_sim = position_sim + len(item)
                        #print("advancing position to", position_sim)
                        potentials_counter +=1
                    else:
                        break

            # if any(sequence in potentials for sequence in sequences):
            #
            #     solution.append(s)
            #     pass
            # pass
print(max_matched_length, "/", len(instruction_str))
print(["".join(str(x)) for x in max_matched_sequences])
print(max_matched_solution)
print(instruction_str)

# TRY TO RIDE

# initiate the intcomp - modified to run until halted or run out of inputs
mem_out = copy.copy(program)  # memory outside of running intcopm
mem_out[0] = 2  # turn on the bot

inputs_out = []  # input list
pos_out = 0  # starting position of memory intcomp
rel_pos_out = 0  # relative position for relative mode

# initiate state and outputs list
outputs = []
state = "running"

# inititate world - overlay
position = (0, 0)
explored_dict = {}
track = []  # defaultdict(constant_factory())

# initiate trackers for display
track_dict = {}
start_dict = {(0, 0): 1}
position_dict = {position: 1}

result = []

#exit(0)
def test_inputs():
    ins = [",".join(solution2),
           "R,12,R,4,R,10,R,12",
           "R,6,L,8,R,10",
           "L,8,R,4,R,4,R,6",
           "n"]
    for x in ins:
        yield x
#exit(0)

ins1 = test_inputs()

while not any([x == "X" for x in last_output]):

    # try to move the bot in direction
    mem_out, inputs_out, pos_out, rel_pos_out, last_output, state = stepper_computer(mem_out, inputs_out, pos_out,
                                                                                     rel_pos_out)
    print(last_output)
    result = "".join([chr(x) for x in last_output])
    # print(result)
    result = result.split("\n")

    for line in result:
        print(line)

    try:
        manual_input = next(ins1)
        inputs_out = [ord(x) for x in manual_input] + [10]
    except StopIteration:
        inputs_out = []

    if result == ['']:
        break
