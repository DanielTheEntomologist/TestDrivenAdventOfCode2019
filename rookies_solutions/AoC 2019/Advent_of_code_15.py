import pandas as pd
# import easygui
# import os
import math
import copy
import time
from pathlib import PureWindowsPath
from collections import deque
from collections import defaultdict
from collections import Counter
# import matplotlib
import matplotlib.pyplot as plt
import numpy as np


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
    for line in display:
        print("".join(line))
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


# program = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
# program = [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]
# program = [3, 52, 1001, 52, -5, 52, 3, 53, 1, 52, 56, 54, 1007, 54, 5, 55, 1005, 55, 26, 1001, 54, -5, 54, 1105, 1, 12,1, 53, 54, 53, 1008, 54, 0, 55, 1001, 55, 1, 55, 2, 53, 55, 53, 4, 53, 1001, 56, -1, 56, 1005, 56, 6, 99, 0,0, 0, 0, 10]
# program = starting_file


# program = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
# program = [1102,34915192,34915192,7,4,7,99,0] # should output 16 digit number on full intcode computer
# program = [104,1125899906842624,99]
# BOOST program:
# program = [1102,34463338,34463338,63,1007,63,34463338,63,1005,63,53,1101,3,0,1000,109,988,209,12,9,1000,209,6,209,3,203,0,1008,1000,1,63,1005,63,65,1008,1000,2,63,1005,63,902,1008,1000,0,63,1005,63,58,4,25,104,0,99,4,0,104,0,99,4,17,104,0,99,0,0,1101,26,0,1015,1101,29,0,1010,1102,1,24,1013,1102,1,33,1008,1102,36,1,1012,1101,0,572,1023,1101,35,0,1014,1101,0,38,1019,1102,1,30,1006,1101,0,890,1029,1101,34,0,1011,1101,28,0,1002,1102,1,1,1021,1101,0,37,1001,1101,0,197,1026,1101,22,0,1017,1102,1,895,1028,1101,0,20,1007,1102,21,1,1004,1102,1,39,1016,1101,0,0,1020,1102,1,190,1027,1101,0,775,1024,1102,31,1,1018,1101,0,23,1003,1101,0,25,1009,1101,770,0,1025,1101,0,27,1000,1102,1,575,1022,1101,0,32,1005,109,27,2106,0,0,1001,64,1,64,1106,0,199,4,187,1002,64,2,64,109,-18,21101,40,0,5,1008,1014,39,63,1005,63,219,1106,0,225,4,205,1001,64,1,64,1002,64,2,64,109,-6,1201,-1,0,63,1008,63,28,63,1005,63,251,4,231,1001,64,1,64,1105,1,251,1002,64,2,64,109,5,21102,41,1,3,1008,1011,38,63,1005,63,271,1105,1,277,4,257,1001,64,1,64,1002,64,2,64,109,-7,2102,1,1,63,1008,63,28,63,1005,63,299,4,283,1106,0,303,1001,64,1,64,1002,64,2,64,109,-7,1207,10,22,63,1005,63,321,4,309,1106,0,325,1001,64,1,64,1002,64,2,64,109,16,2107,31,-4,63,1005,63,345,1001,64,1,64,1105,1,347,4,331,1002,64,2,64,109,-9,1201,3,0,63,1008,63,18,63,1005,63,371,1001,64,1,64,1106,0,373,4,353,1002,64,2,64,109,7,1202,-7,1,63,1008,63,40,63,1005,63,393,1106,0,399,4,379,1001,64,1,64,1002,64,2,64,109,-5,1208,5,33,63,1005,63,417,4,405,1106,0,421,1001,64,1,64,1002,64,2,64,109,1,1202,2,1,63,1008,63,30,63,1005,63,443,4,427,1105,1,447,1001,64,1,64,1002,64,2,64,109,-7,2102,1,10,63,1008,63,19,63,1005,63,471,1001,64,1,64,1105,1,473,4,453,1002,64,2,64,109,6,2108,21,0,63,1005,63,489,1105,1,495,4,479,1001,64,1,64,1002,64,2,64,109,9,21108,42,42,0,1005,1012,513,4,501,1105,1,517,1001,64,1,64,1002,64,2,64,109,7,21107,43,44,-1,1005,1018,535,4,523,1106,0,539,1001,64,1,64,1002,64,2,64,109,-5,21101,44,0,2,1008,1016,44,63,1005,63,561,4,545,1105,1,565,1001,64,1,64,1002,64,2,64,2105,1,9,1106,0,581,4,569,1001,64,1,64,1002,64,2,64,109,13,21107,45,44,-9,1005,1018,597,1105,1,603,4,587,1001,64,1,64,1002,64,2,64,109,-25,2101,0,3,63,1008,63,32,63,1005,63,625,4,609,1105,1,629,1001,64,1,64,1002,64,2,64,109,7,1208,-7,30,63,1005,63,645,1105,1,651,4,635,1001,64,1,64,1002,64,2,64,109,-2,21102,46,1,9,1008,1016,46,63,1005,63,677,4,657,1001,64,1,64,1106,0,677,1002,64,2,64,109,-2,21108,47,48,9,1005,1014,697,1001,64,1,64,1105,1,699,4,683,1002,64,2,64,109,14,1205,2,713,4,705,1105,1,717,1001,64,1,64,1002,64,2,64,109,-7,1206,8,735,4,723,1001,64,1,64,1106,0,735,1002,64,2,64,109,-18,2101,0,6,63,1008,63,24,63,1005,63,759,1001,64,1,64,1106,0,761,4,741,1002,64,2,64,109,29,2105,1,1,4,767,1106,0,779,1001,64,1,64,1002,64,2,64,109,-5,1206,3,791,1106,0,797,4,785,1001,64,1,64,1002,64,2,64,109,-12,2107,31,-1,63,1005,63,819,4,803,1001,64,1,64,1105,1,819,1002,64,2,64,109,7,1205,7,835,1001,64,1,64,1105,1,837,4,825,1002,64,2,64,109,-11,1207,7,24,63,1005,63,853,1106,0,859,4,843,1001,64,1,64,1002,64,2,64,109,4,2108,27,-6,63,1005,63,881,4,865,1001,64,1,64,1106,0,881,1002,64,2,64,109,24,2106,0,-2,4,887,1106,0,899,1001,64,1,64,4,64,99,21102,27,1,1,21101,0,913,0,1106,0,920,21201,1,61934,1,204,1,99,109,3,1207,-2,3,63,1005,63,962,21201,-2,-1,1,21101,0,940,0,1106,0,920,21202,1,1,-1,21201,-2,-3,1,21101,0,955,0,1105,1,920,22201,1,-1,-2,1105,1,966,22102,1,-2,-2,109,-3,2105,1,0]
# PAINTING BOT:
# program = [3, 8, 1005, 8, 325, 1106, 0, 11, 0, 0, 0, 104, 1, 104, 0, 3, 8, 102, -1, 8, 10, 1001, 10, 1, 10, 4, 10, 108,
#            0, 8, 10, 4, 10, 101, 0, 8, 28, 2, 3, 7, 10, 2, 1109, 3, 10, 2, 102, 0, 10, 2, 1005, 12, 10, 3, 8, 102, -1,
#            8, 10, 101, 1, 10, 10, 4, 10, 1008, 8, 0, 10, 4, 10, 101, 0, 8, 67, 2, 109, 12, 10, 1, 1003, 15, 10, 3, 8,
#            1002, 8, -1, 10, 1001, 10, 1, 10, 4, 10, 108, 1, 8, 10, 4, 10, 101, 0, 8, 96, 3, 8, 102, -1, 8, 10, 101, 1,
#            10, 10, 4, 10, 1008, 8, 0, 10, 4, 10, 1002, 8, 1, 119, 3, 8, 102, -1, 8, 10, 1001, 10, 1, 10, 4, 10, 1008, 8,
#            0, 10, 4, 10, 101, 0, 8, 141, 3, 8, 1002, 8, -1, 10, 101, 1, 10, 10, 4, 10, 108, 0, 8, 10, 4, 10, 1001, 8, 0,
#            162, 1, 106, 17, 10, 1006, 0, 52, 1006, 0, 73, 3, 8, 102, -1, 8, 10, 1001, 10, 1, 10, 4, 10, 108, 1, 8, 10,
#            4, 10, 1001, 8, 0, 194, 1006, 0, 97, 1, 1004, 6, 10, 1006, 0, 32, 2, 8, 20, 10, 3, 8, 102, -1, 8, 10, 101, 1,
#            10, 10, 4, 10, 1008, 8, 1, 10, 4, 10, 102, 1, 8, 231, 1, 1, 15, 10, 1006, 0, 21, 1, 6, 17, 10, 2, 1005, 8,
#            10, 3, 8, 102, -1, 8, 10, 101, 1, 10, 10, 4, 10, 108, 1, 8, 10, 4, 10, 102, 1, 8, 267, 2, 1007, 10, 10, 3, 8,
#            1002, 8, -1, 10, 1001, 10, 1, 10, 4, 10, 1008, 8, 1, 10, 4, 10, 102, 1, 8, 294, 1006, 0, 74, 2, 1003, 2, 10,
#            1, 107, 1, 10, 101, 1, 9, 9, 1007, 9, 1042, 10, 1005, 10, 15, 99, 109, 647, 104, 0, 104, 1, 21101,
#            936333018008, 0, 1, 21101, 342, 0, 0, 1106, 0, 446, 21102, 937121129228, 1, 1, 21101, 0, 353, 0, 1105, 1,
#            446, 3, 10, 104, 0, 104, 1, 3, 10, 104, 0, 104, 0, 3, 10, 104, 0, 104, 1, 3, 10, 104, 0, 104, 1, 3, 10, 104,
#            0, 104, 0, 3, 10, 104, 0, 104, 1, 21101, 0, 209383001255, 1, 21102, 400, 1, 0, 1106, 0, 446, 21101, 0,
#            28994371675, 1, 21101, 411, 0, 0, 1105, 1, 446, 3, 10, 104, 0, 104, 0, 3, 10, 104, 0, 104, 0, 21101,
#            867961824000, 0, 1, 21101, 0, 434, 0, 1106, 0, 446, 21102, 1, 983925674344, 1, 21101, 0, 445, 0, 1106, 0,
#            446, 99, 109, 2, 21201, -1, 0, 1, 21102, 40, 1, 2, 21101, 477, 0, 3, 21102, 467, 1, 0, 1106, 0, 510, 109, -2,
#            2106, 0, 0, 0, 1, 0, 0, 1, 109, 2, 3, 10, 204, -1, 1001, 472, 473, 488, 4, 0, 1001, 472, 1, 472, 108, 4, 472,
#            10, 1006, 10, 504, 1101, 0, 0, 472, 109, -2, 2106, 0, 0, 0, 109, 4, 1201, -1, 0, 509, 1207, -3, 0, 10, 1006,
#            10, 527, 21102, 1, 0, -3, 21202, -3, 1, 1, 21201, -2, 0, 2, 21102, 1, 1, 3, 21102, 1, 546, 0, 1106, 0, 551,
#            109, -4, 2105, 1, 0, 109, 5, 1207, -3, 1, 10, 1006, 10, 574, 2207, -4, -2, 10, 1006, 10, 574, 22101, 0, -4,
#            -4, 1105, 1, 642, 21202, -4, 1, 1, 21201, -3, -1, 2, 21202, -2, 2, 3, 21101, 0, 593, 0, 1105, 1, 551, 22102,
#            1, 1, -4, 21101, 1, 0, -1, 2207, -4, -2, 10, 1006, 10, 612, 21102, 1, 0, -1, 22202, -2, -1, -2, 2107, 0, -3,
#            10, 1006, 10, 634, 21201, -1, 0, 1, 21101, 634, 0, 0, 105, 1, 509, 21202, -2, -1, -2, 22201, -4, -2, -4, 109,
#            -5, 2106, 0, 0]
# ARCADE GAME:
# program = [1, 380, 379, 385, 1008, 2719, 351522, 381, 1005, 381, 12, 99, 109, 2720, 1102, 1, 0, 383, 1101, 0, 0, 382,
#            20102, 1, 382, 1, 21002, 383, 1, 2, 21101, 37, 0, 0, 1105, 1, 578, 4, 382, 4, 383, 204, 1, 1001, 382, 1, 382,
#            1007, 382, 40, 381, 1005, 381, 22, 1001, 383, 1, 383, 1007, 383, 26, 381, 1005, 381, 18, 1006, 385, 69, 99,
#            104, -1, 104, 0, 4, 386, 3, 384, 1007, 384, 0, 381, 1005, 381, 94, 107, 0, 384, 381, 1005, 381, 108, 1106, 0,
#            161, 107, 1, 392, 381, 1006, 381, 161, 1102, 1, -1, 384, 1105, 1, 119, 1007, 392, 38, 381, 1006, 381, 161,
#            1102, 1, 1, 384, 21002, 392, 1, 1, 21101, 24, 0, 2, 21101, 0, 0, 3, 21102, 1, 138, 0, 1105, 1, 549, 1, 392,
#            384, 392, 20102, 1, 392, 1, 21101, 0, 24, 2, 21102, 1, 3, 3, 21101, 0, 161, 0, 1105, 1, 549, 1101, 0, 0, 384,
#            20001, 388, 390, 1, 21001, 389, 0, 2, 21102, 1, 180, 0, 1106, 0, 578, 1206, 1, 213, 1208, 1, 2, 381, 1006,
#            381, 205, 20001, 388, 390, 1, 21001, 389, 0, 2, 21101, 205, 0, 0, 1106, 0, 393, 1002, 390, -1, 390, 1101, 1,
#            0, 384, 20102, 1, 388, 1, 20001, 389, 391, 2, 21101, 0, 228, 0, 1105, 1, 578, 1206, 1, 261, 1208, 1, 2, 381,
#            1006, 381, 253, 21002, 388, 1, 1, 20001, 389, 391, 2, 21102, 253, 1, 0, 1106, 0, 393, 1002, 391, -1, 391,
#            1101, 0, 1, 384, 1005, 384, 161, 20001, 388, 390, 1, 20001, 389, 391, 2, 21102, 1, 279, 0, 1106, 0, 578,
#            1206, 1, 316, 1208, 1, 2, 381, 1006, 381, 304, 20001, 388, 390, 1, 20001, 389, 391, 2, 21101, 304, 0, 0,
#            1106, 0, 393, 1002, 390, -1, 390, 1002, 391, -1, 391, 1101, 1, 0, 384, 1005, 384, 161, 21001, 388, 0, 1,
#            21002, 389, 1, 2, 21102, 0, 1, 3, 21102, 338, 1, 0, 1106, 0, 549, 1, 388, 390, 388, 1, 389, 391, 389, 21001,
#            388, 0, 1, 20101, 0, 389, 2, 21101, 4, 0, 3, 21101, 365, 0, 0, 1106, 0, 549, 1007, 389, 25, 381, 1005, 381,
#            75, 104, -1, 104, 0, 104, 0, 99, 0, 1, 0, 0, 0, 0, 0, 0, 298, 18, 21, 1, 1, 20, 109, 3, 22101, 0, -2, 1,
#            22101, 0, -1, 2, 21102, 1, 0, 3, 21102, 414, 1, 0, 1106, 0, 549, 21202, -2, 1, 1, 22101, 0, -1, 2, 21101,
#            429, 0, 0, 1106, 0, 601, 2101, 0, 1, 435, 1, 386, 0, 386, 104, -1, 104, 0, 4, 386, 1001, 387, -1, 387, 1005,
#            387, 451, 99, 109, -3, 2105, 1, 0, 109, 8, 22202, -7, -6, -3, 22201, -3, -5, -3, 21202, -4, 64, -2, 2207, -3,
#            -2, 381, 1005, 381, 492, 21202, -2, -1, -1, 22201, -3, -1, -3, 2207, -3, -2, 381, 1006, 381, 481, 21202, -4,
#            8, -2, 2207, -3, -2, 381, 1005, 381, 518, 21202, -2, -1, -1, 22201, -3, -1, -3, 2207, -3, -2, 381, 1006, 381,
#            507, 2207, -3, -4, 381, 1005, 381, 540, 21202, -4, -1, -1, 22201, -3, -1, -3, 2207, -3, -4, 381, 1006, 381,
#            529, 21201, -3, 0, -7, 109, -8, 2106, 0, 0, 109, 4, 1202, -2, 40, 566, 201, -3, 566, 566, 101, 639, 566, 566,
#            1201, -1, 0, 0, 204, -3, 204, -2, 204, -1, 109, -4, 2105, 1, 0, 109, 3, 1202, -1, 40, 593, 201, -2, 593, 593,
#            101, 639, 593, 593, 21001, 0, 0, -2, 109, -3, 2106, 0, 0, 109, 3, 22102, 26, -2, 1, 22201, 1, -1, 1, 21102,
#            1, 523, 2, 21102, 583, 1, 3, 21102, 1040, 1, 4, 21101, 0, 630, 0, 1106, 0, 456, 21201, 1, 1679, -2, 109, -3,
#            2105, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
#            1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 2, 0, 0, 2, 0, 2, 2, 2, 0, 2, 0,
#            2, 0, 2, 2, 0, 0, 0, 2, 2, 2, 0, 2, 0, 0, 0, 1, 1, 0, 2, 2, 0, 2, 0, 2, 0, 0, 2, 0, 0, 0, 2, 2, 2, 0, 0, 0,
#            2, 0, 2, 0, 0, 0, 2, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 2, 0, 1, 1, 0, 2, 0, 2, 0, 2, 0, 2, 2, 2, 0, 0, 2, 0, 0,
#            0, 0, 0, 2, 0, 0, 0, 2, 0, 2, 0, 2, 2, 0, 2, 2, 0, 2, 2, 2, 2, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0,
#            0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 2, 2, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 2, 0, 1, 1, 0, 2, 0, 0, 2, 0, 0,
#            0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 2, 0, 0, 2, 2, 2, 0, 0, 0, 2, 2, 2, 0, 2, 0, 0, 0, 2, 0, 0, 0, 1, 1, 0, 0, 2,
#            0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 2, 0, 0, 2, 0, 2, 0, 0, 0, 2, 2, 2, 2, 0, 2, 2, 2, 2, 0, 0, 1,
#            1, 0, 2, 2, 0, 0, 0, 0, 2, 2, 0, 2, 0, 0, 0, 2, 2, 2, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 2, 0, 2, 2, 2, 0,
#            0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 2, 2, 2, 2, 0, 2, 2, 0, 0, 2, 0, 0, 2, 2, 0, 2, 2, 2, 0, 0, 2,
#            2, 0, 0, 0, 2, 0, 0, 1, 1, 0, 0, 0, 2, 0, 2, 0, 2, 0, 2, 0, 0, 2, 2, 2, 2, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 0,
#            0, 2, 2, 2, 0, 0, 0, 2, 0, 0, 0, 1, 1, 0, 0, 2, 0, 0, 0, 2, 2, 2, 0, 2, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0,
#            2, 2, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 0, 0, 0, 1, 1, 0, 0, 2, 2, 2, 2, 0, 2, 0, 0, 0, 2, 2, 2, 2, 0, 2, 0, 2,
#            2, 0, 2, 0, 2, 0, 0, 2, 0, 0, 0, 2, 2, 0, 0, 0, 2, 0, 0, 1, 1, 0, 2, 0, 0, 2, 2, 0, 0, 0, 2, 0, 0, 2, 0, 0,
#            0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 2, 0, 2, 2, 2, 0, 2, 0, 0, 1, 1, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0,
#            2, 0, 0, 0, 2, 0, 2, 2, 0, 2, 2, 2, 2, 2, 0, 0, 2, 2, 0, 2, 2, 2, 0, 2, 0, 0, 0, 1, 1, 0, 0, 2, 2, 0, 0, 0,
#            2, 0, 0, 0, 0, 2, 0, 0, 2, 2, 0, 2, 2, 2, 0, 0, 2, 2, 2, 2, 2, 2, 0, 2, 0, 2, 2, 0, 0, 2, 0, 1, 1, 0, 2, 2,
#            2, 0, 2, 0, 0, 0, 2, 2, 2, 2, 0, 0, 2, 2, 2, 0, 0, 0, 2, 2, 2, 0, 2, 0, 2, 0, 2, 0, 2, 2, 0, 0, 0, 2, 0, 1,
#            1, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 2, 0, 2, 2, 0, 0, 0, 2, 0, 0, 2, 2, 2, 2, 0, 0, 2, 0, 0, 0, 2, 0, 2, 0, 0,
#            2, 0, 0, 1, 1, 0, 0, 0, 2, 0, 2, 2, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 0, 2, 0, 0, 2, 0, 2, 2, 2, 2, 2, 0,
#            2, 2, 2, 0, 0, 0, 0, 1, 1, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 0, 2, 2, 0, 0, 0, 0, 0, 2, 0, 2, 0,
#            0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0,
#            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0,
#            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0,
#            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
#            94, 63, 98, 14, 55, 98, 64, 9, 39, 55, 40, 3, 77, 79, 41, 40, 52, 25, 26, 46, 83, 8, 72, 65, 35, 58, 50, 6,
#            78, 78, 40, 77, 45, 49, 98, 98, 47, 68, 93, 85, 87, 19, 71, 89, 59, 81, 2, 62, 12, 53, 10, 21, 45, 23, 11,
#            95, 37, 33, 57, 32, 82, 63, 2, 97, 43, 93, 91, 66, 32, 55, 20, 53, 14, 7, 50, 62, 41, 32, 12, 63, 85, 86, 2,
#            83, 63, 7, 1, 91, 7, 67, 6, 57, 74, 63, 21, 14, 50, 92, 96, 13, 73, 52, 27, 39, 1, 17, 82, 87, 58, 45, 30,
#            31, 29, 85, 70, 59, 95, 71, 75, 74, 12, 51, 62, 83, 38, 53, 15, 13, 45, 6, 71, 35, 98, 36, 88, 9, 77, 37, 4,
#            5, 52, 59, 53, 83, 77, 7, 8, 97, 56, 97, 14, 40, 82, 93, 1, 81, 37, 38, 49, 89, 70, 9, 60, 1, 12, 79, 5, 22,
#            7, 86, 41, 42, 79, 24, 51, 9, 1, 8, 72, 3, 53, 71, 76, 49, 55, 57, 95, 87, 68, 33, 6, 28, 7, 50, 81, 75, 57,
#            72, 95, 67, 12, 29, 19, 77, 52, 69, 72, 38, 16, 21, 4, 91, 15, 1, 11, 3, 70, 46, 54, 95, 24, 93, 13, 40, 23,
#            14, 93, 58, 59, 87, 54, 79, 84, 38, 7, 97, 66, 40, 66, 42, 1, 66, 45, 82, 64, 65, 95, 19, 43, 16, 20, 36, 94,
#            39, 95, 25, 2, 75, 96, 55, 7, 63, 30, 8, 86, 92, 68, 54, 75, 81, 49, 75, 29, 77, 3, 85, 23, 72, 19, 44, 8, 5,
#            40, 48, 65, 23, 67, 76, 43, 87, 72, 52, 46, 61, 22, 42, 86, 86, 23, 46, 17, 58, 67, 86, 83, 36, 93, 95, 53,
#            69, 14, 58, 54, 69, 25, 2, 51, 2, 51, 35, 24, 57, 92, 75, 82, 23, 61, 19, 94, 15, 34, 4, 29, 10, 24, 81, 2,
#            88, 48, 5, 84, 72, 64, 28, 11, 57, 3, 30, 71, 58, 88, 7, 63, 54, 15, 66, 48, 4, 5, 78, 35, 37, 24, 89, 89,
#            68, 90, 38, 85, 81, 9, 73, 36, 28, 5, 89, 42, 14, 5, 76, 72, 2, 38, 97, 49, 46, 80, 86, 17, 71, 3, 27, 2, 4,
#            28, 91, 31, 9, 83, 89, 63, 47, 53, 38, 30, 35, 21, 66, 27, 51, 3, 68, 70, 17, 30, 57, 83, 80, 66, 32, 92, 52,
#            84, 80, 29, 4, 79, 20, 86, 41, 17, 31, 39, 67, 25, 39, 97, 41, 53, 63, 78, 26, 85, 57, 76, 82, 25, 48, 81,
#            92, 66, 49, 29, 95, 89, 56, 65, 87, 62, 71, 63, 17, 46, 98, 4, 86, 39, 26, 12, 14, 51, 73, 38, 46, 27, 98,
#            66, 1, 19, 65, 56, 98, 25, 27, 98, 78, 31, 49, 47, 42, 32, 13, 3, 60, 1, 11, 14, 42, 69, 11, 76, 86, 95, 17,
#            19, 92, 77, 8, 19, 85, 81, 69, 22, 18, 48, 68, 27, 2, 24, 3, 10, 25, 6, 27, 3, 28, 64, 23, 3, 7, 94, 96, 84,
#            27, 18, 9, 60, 90, 60, 37, 72, 58, 93, 72, 36, 21, 85, 62, 11, 64, 34, 5, 3, 6, 9, 31, 85, 25, 81, 34, 87,
#            86, 88, 35, 69, 8, 7, 18, 31, 24, 8, 79, 71, 45, 51, 41, 83, 13, 81, 39, 34, 3, 44, 17, 27, 71, 7, 13, 36,
#            89, 70, 77, 79, 61, 31, 62, 51, 15, 78, 72, 37, 32, 82, 62, 10, 32, 84, 79, 64, 19, 89, 56, 51, 52, 87, 44,
#            31, 18, 75, 96, 26, 79, 58, 51, 2, 54, 84, 42, 17, 60, 37, 34, 66, 33, 4, 20, 93, 43, 8, 90, 43, 92, 10, 90,
#            43, 9, 34, 18, 39, 79, 32, 1, 36, 69, 90, 29, 49, 56, 63, 60, 36, 46, 38, 79, 6, 57, 1, 97, 65, 78, 47, 82,
#            78, 25, 33, 3, 14, 22, 89, 37, 29, 81, 68, 82, 41, 31, 16, 91, 13, 73, 68, 4, 79, 6, 86, 91, 87, 69, 85, 46,
#            41, 85, 6, 36, 87, 93, 18, 74, 55, 84, 3, 9, 88, 19, 30, 46, 47, 33, 79, 94, 67, 75, 36, 8, 66, 14, 52, 10,
#            92, 91, 93, 5, 63, 52, 42, 11, 11, 48, 45, 66, 51, 30, 5, 39, 39, 49, 66, 38, 57, 19, 54, 90, 44, 60, 31, 11,
#            21, 31, 56, 35, 76, 35, 67, 79, 70, 18, 11, 50, 6, 97, 59, 5, 72, 50, 54, 75, 41, 19, 54, 12, 47, 56, 42, 80,
#            70, 69, 69, 34, 97, 57, 43, 6, 60, 52, 39, 43, 52, 34, 4, 41, 86, 47, 2, 80, 41, 15, 60, 50, 24, 31, 24, 83,
#            34, 19, 40, 55, 42, 25, 93, 39, 85, 29, 98, 95, 67, 55, 62, 4, 26, 19, 61, 93, 14, 11, 45, 50, 40, 81, 61,
#            57, 17, 44, 3, 75, 7, 74, 20, 70, 2, 63, 29, 52, 48, 47, 29, 90, 8, 36, 39, 77, 62, 97, 11, 43, 31, 13, 25,
#            5, 66, 2, 6, 20, 49, 89, 48, 67, 79, 66, 74, 48, 79, 45, 5, 35, 31, 33, 50, 95, 23, 56, 33, 40, 75, 24, 81,
#            84, 56, 35, 96, 11, 95, 29, 7, 55, 17, 37, 18, 20, 32, 41, 4, 71, 74, 67, 7, 46, 1, 86, 70, 9, 13, 40, 17,
#            12, 64, 31, 65, 60, 40, 4, 6, 42, 57, 89, 15, 40, 53, 88, 14, 2, 35, 5, 16, 44, 62, 6, 53, 83, 76, 87, 26,
#            82, 1, 7, 25, 66, 65, 53, 60, 52, 57, 64, 9, 16, 88, 2, 93, 33, 62, 82, 27, 17, 29, 17, 40, 68, 83, 4, 28,
#            83, 62, 6, 91, 45, 69, 30, 8, 39, 55, 78, 97, 46, 13, 2, 7, 80, 74, 19, 68, 20, 2, 5, 35, 55, 62, 25, 32, 55,
#            3, 76, 92, 70, 62, 36, 73, 14, 55, 12, 4, 25, 46, 25, 17, 41, 63, 19, 74, 70, 86, 4, 80, 50, 97, 44, 65, 51,
#            44, 7, 78, 59, 351522]
# REPAIR BOT 15
program = [3, 1033, 1008, 1033, 1, 1032, 1005, 1032, 31, 1008, 1033, 2, 1032, 1005, 1032, 58, 1008, 1033, 3, 1032, 1005,
           1032, 81, 1008, 1033, 4, 1032, 1005, 1032, 104, 99, 101, 0, 1034, 1039, 102, 1, 1036, 1041, 1001, 1035, -1,
           1040, 1008, 1038, 0, 1043, 102, -1, 1043, 1032, 1, 1037, 1032, 1042, 1106, 0, 124, 1002, 1034, 1, 1039, 101,
           0, 1036, 1041, 1001, 1035, 1, 1040, 1008, 1038, 0, 1043, 1, 1037, 1038, 1042, 1105, 1, 124, 1001, 1034, -1,
           1039, 1008, 1036, 0, 1041, 1002, 1035, 1, 1040, 102, 1, 1038, 1043, 1001, 1037, 0, 1042, 1106, 0, 124, 1001,
           1034, 1, 1039, 1008, 1036, 0, 1041, 1001, 1035, 0, 1040, 1001, 1038, 0, 1043, 1001, 1037, 0, 1042, 1006,
           1039, 217, 1006, 1040, 217, 1008, 1039, 40, 1032, 1005, 1032, 217, 1008, 1040, 40, 1032, 1005, 1032, 217,
           1008, 1039, 1, 1032, 1006, 1032, 165, 1008, 1040, 39, 1032, 1006, 1032, 165, 1102, 2, 1, 1044, 1105, 1, 224,
           2, 1041, 1043, 1032, 1006, 1032, 179, 1101, 0, 1, 1044, 1105, 1, 224, 1, 1041, 1043, 1032, 1006, 1032, 217,
           1, 1042, 1043, 1032, 1001, 1032, -1, 1032, 1002, 1032, 39, 1032, 1, 1032, 1039, 1032, 101, -1, 1032, 1032,
           101, 252, 1032, 211, 1007, 0, 45, 1044, 1106, 0, 224, 1101, 0, 0, 1044, 1105, 1, 224, 1006, 1044, 247, 102,
           1, 1039, 1034, 102, 1, 1040, 1035, 102, 1, 1041, 1036, 1001, 1043, 0, 1038, 1002, 1042, 1, 1037, 4, 1044,
           1106, 0, 0, 12, 89, 14, 22, 56, 12, 54, 34, 71, 12, 40, 31, 83, 2, 95, 25, 4, 70, 18, 59, 32, 11, 19, 23, 67,
           17, 25, 18, 72, 14, 60, 9, 85, 6, 84, 89, 2, 14, 10, 44, 85, 34, 63, 11, 23, 79, 6, 56, 4, 88, 69, 20, 2, 88,
           87, 31, 56, 16, 68, 29, 84, 43, 58, 6, 14, 98, 73, 3, 35, 79, 24, 89, 43, 59, 12, 78, 86, 13, 10, 61, 37, 46,
           44, 61, 25, 12, 71, 36, 65, 79, 31, 5, 71, 13, 99, 90, 87, 35, 40, 98, 3, 80, 69, 97, 31, 37, 93, 37, 78, 34,
           48, 32, 51, 41, 75, 50, 16, 25, 10, 92, 88, 28, 50, 7, 95, 11, 15, 99, 10, 61, 56, 25, 14, 99, 23, 23, 90,
           73, 66, 94, 23, 60, 34, 26, 73, 44, 38, 71, 41, 42, 79, 10, 25, 69, 43, 39, 92, 19, 35, 95, 23, 60, 8, 75,
           38, 55, 82, 40, 44, 29, 84, 82, 33, 36, 63, 93, 10, 7, 50, 41, 22, 76, 79, 59, 42, 61, 40, 72, 4, 51, 5, 83,
           99, 22, 79, 33, 6, 53, 62, 30, 77, 37, 22, 94, 84, 43, 19, 60, 52, 44, 82, 99, 23, 47, 29, 68, 57, 38, 66,
           40, 55, 17, 15, 78, 86, 10, 54, 25, 52, 39, 62, 35, 11, 19, 15, 75, 12, 20, 63, 67, 98, 35, 70, 17, 95, 66,
           24, 37, 56, 10, 75, 3, 95, 35, 41, 62, 8, 3, 60, 72, 5, 98, 61, 27, 42, 63, 16, 55, 29, 6, 54, 48, 40, 7, 66,
           92, 31, 48, 16, 41, 87, 86, 6, 16, 24, 53, 85, 17, 4, 12, 20, 89, 74, 5, 84, 67, 27, 37, 67, 30, 29, 27, 92,
           46, 40, 14, 77, 95, 50, 17, 31, 38, 44, 83, 12, 39, 12, 98, 96, 20, 7, 69, 82, 7, 12, 75, 49, 85, 59, 17, 44,
           98, 58, 28, 94, 34, 81, 49, 48, 66, 51, 43, 5, 96, 52, 22, 81, 36, 83, 94, 32, 28, 94, 27, 97, 18, 99, 32,
           49, 53, 31, 16, 61, 57, 18, 87, 22, 93, 18, 21, 25, 77, 33, 78, 41, 34, 69, 5, 28, 15, 87, 38, 98, 38, 41,
           83, 10, 61, 90, 21, 92, 35, 93, 51, 35, 92, 23, 50, 23, 5, 51, 97, 60, 36, 69, 4, 62, 20, 39, 88, 11, 48, 56,
           9, 92, 8, 85, 78, 62, 24, 62, 82, 15, 16, 30, 81, 34, 9, 98, 94, 8, 16, 85, 22, 75, 40, 62, 78, 25, 70, 16,
           47, 28, 93, 32, 21, 62, 53, 94, 62, 14, 75, 19, 69, 8, 47, 9, 39, 90, 35, 10, 86, 50, 15, 84, 42, 72, 19, 24,
           5, 77, 79, 3, 93, 66, 6, 89, 16, 11, 55, 32, 37, 38, 28, 50, 78, 21, 29, 35, 13, 95, 71, 3, 14, 12, 96, 23,
           75, 33, 97, 26, 41, 96, 88, 68, 22, 39, 18, 4, 7, 46, 91, 8, 55, 39, 37, 28, 47, 79, 38, 73, 11, 72, 8, 28,
           76, 70, 69, 27, 84, 37, 84, 79, 81, 34, 71, 97, 43, 94, 74, 13, 58, 14, 64, 20, 53, 22, 67, 86, 39, 46, 28,
           50, 34, 62, 54, 8, 41, 24, 68, 57, 80, 94, 32, 79, 18, 61, 15, 90, 23, 6, 67, 92, 18, 18, 83, 36, 46, 44, 31,
           76, 39, 2, 77, 23, 93, 10, 67, 37, 25, 46, 19, 87, 21, 2, 92, 92, 92, 68, 27, 13, 38, 42, 85, 13, 46, 39, 61,
           96, 9, 53, 29, 44, 81, 84, 91, 11, 79, 75, 5, 13, 88, 84, 19, 1, 18, 38, 86, 42, 6, 85, 63, 40, 93, 3, 33,
           83, 41, 82, 51, 79, 37, 85, 1, 53, 40, 39, 74, 33, 54, 29, 23, 49, 21, 31, 43, 29, 98, 32, 70, 59, 10, 24,
           21, 74, 89, 20, 96, 78, 21, 25, 9, 99, 52, 8, 39, 64, 25, 29, 95, 37, 49, 94, 35, 1, 85, 48, 5, 97, 23, 64,
           41, 98, 14, 76, 97, 55, 56, 11, 23, 81, 42, 98, 43, 46, 37, 22, 99, 1, 98, 91, 58, 20, 23, 94, 53, 63, 23,
           59, 8, 32, 94, 37, 70, 24, 33, 69, 79, 77, 35, 32, 52, 79, 17, 62, 31, 30, 70, 61, 20, 2, 54, 17, 46, 36, 75,
           58, 61, 33, 71, 10, 50, 10, 53, 10, 79, 30, 79, 41, 91, 80, 52, 20, 54, 65, 84, 24, 85, 9, 69, 11, 54, 12,
           83, 86, 54, 27, 68, 9, 86, 0, 0, 21, 21, 1, 10, 1, 0, 0, 0, 0, 0, 0]

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
explored = {(0, 0): 1}
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
vectors = {1: (0, 1), 2: (0, -1), 3: (-1, 0), 4: (1, 0)}
directions = {1: "UP", 2: "DOWN", 3: "LEFT", 4: "RIGHT"}

OxygenRiderMode = True

if OxygenRiderMode:
    OxygenRiderActive = False
    OxygenWaves = []
    while True:
        """ 
        1. Spróbuj się poruszyć po kolei w kierunku. 
            jeżęli eksplorowany kierunek przejdź do kolejnego OK
            jeżęli ściana spróbuj kolejnego kierunku OK
            jeżęli pusto zapętlamy
            Jeżeli wyczerpią się wszystkie kierunki - cofaj o jedną pozycje
        """
        for d in 1, 2, 3, 4:

            # display preprocessing
            track_dict = {(x, y): 1 for x, y in track}
            position_dict = {position: 1}

            # print(Counter([x for x in explored.values()]))
            # print(explored)
            # display_board([explored, track_dict, start_dict, position_dict], translations, empty)  #[explored_t, track_t, start_t, position_t]
            # print("position", position)
            # print("aiming",directions[d])
            # input("press ENTER to continue")

            # aim
            vector = vectors[d]
            position_to_probe = position_probed = (vector[0] + position[0], vector[1] + position[1])
            # recall
            if position_to_probe in explored.keys():
                # print("already explored",position_to_probe)
                continue  # if already explored try another direction

            # try to move the bot in direction
            mem_out, inputs_out, pos_out, rel_pos_out, last_output, state = stepper_computer(mem_out, d, pos_out,
                                                                                             rel_pos_out)

            result = last_output[0]

            if result == 0:  # if wall was encountered show it on map
                explored[position_to_probe] = 0
                # print("found wall at ",position_to_probe)
                continue

            elif result in [1, 2]:  # if result was empty, space mark on map, add to track , move robot
                explored[position_to_probe] = result
                track.append(position)
                if result == 2:
                    print("Found the Oxygen Station at", position_to_probe)
                    print("To go back I would have to move:", len(track))
                    OxygenRiderActive = True
                    explored = {position_to_probe: 1}
                    track = []
                # print("moving from", position,"to", position_to_probe)
                position = position_to_probe
                # print("moved to",position)
                break

        # if no possibilites to move exists move back
        # determine direction to move back
        else:
            if OxygenRiderActive:
                OxygenWaves.append(len(track))
            try:
                position_target = track.pop()
                # print("backtracking to", position_target)
            except IndexError:
                print("back at the start and nowhere to go")
                display_board([explored, track_dict, start_dict, position_dict], translations, empty)
                print("longest path", max(OxygenWaves))
                exit(0)
            vector_required = (position_target[0] - position[0], position_target[1] - position[1])
            d = [key for key, vector in vectors.items() if vector == vector_required]
            # move the bot in direction
            mem_out, inputs_out, pos_out, rel_pos_out, last_output, state = stepper_computer(mem_out, d, pos_out,
                                                                                             rel_pos_out)

            result = last_output[0]

            if result in [1, 2]:  # if wall was encountered show it on map
                position = position_target
            else:
                print("Tried to moved back but encountered", result)
                exit(1)

                break
else:
    while True:
        """ 
        1. Spróbuj się poruszyć po kolei w kierunku. 
            jeżęli eksplorowany kierunek przejdź do kolejnego OK
            jeżęli ściana spróbuj kolejnego kierunku OK
            jeżęli pusto zapętlamy
            Jeżeli wyczerpią się wszystkie kierunki - cofaj o jedną pozycje
        """
        for d in 1, 2, 3, 4:

            # display preprocessing
            track_dict = {(x, y): 1 for x, y in track}
            position_dict = {position: 1}

            # print(Counter([x for x in explored.values()]))
            # print(explored)
            # display_board([explored, track_dict, start_dict, position_dict], translations, empty)  #[explored_t, track_t, start_t, position_t]
            # print("position", position)
            # print("aiming",directions[d])
            # input("press ENTER to continue")

            # aim
            vector = vectors[d]
            position_to_probe = position_probed = (vector[0] + position[0], vector[1] + position[1])
            # recall
            if position_to_probe in explored.keys():
                # print("already explored",position_to_probe)
                continue  # if already explored try another direction

            # try to move the bot in direction
            mem_out, inputs_out, pos_out, rel_pos_out, last_output, state = stepper_computer(mem_out, d, pos_out,
                                                                                             rel_pos_out)

            result = last_output[0]

            if result == 0:  # if wall was encountered show it on map
                explored[position_to_probe] = 0
                # print("found wall at ",position_to_probe)
                continue

            elif result in [1, 2]:  # if result was empty, space mark on map, add to track , move robot
                explored[position_to_probe] = result
                track.append(position)
                if result == 2:
                    print("Found the Oxygen Station at", position_to_probe)
                    print("To go back I would have to move:", len(track))

                # print("moving from", position,"to", position_to_probe)
                position = position_to_probe
                # print("moved to",position)
                break

        # if no possibilites to move exists move back
        # determine direction to move back
        else:
            try:
                position_target = track.pop()
                # print("backtracking to", position_target)
            except IndexError:
                print("back at the start and nowhere to go")
                display_board([explored, track_dict, start_dict, position_dict], translations, empty)
                exit(0)
            vector_required = (position_target[0] - position[0], position_target[1] - position[1])
            d = [key for key, vector in vectors.items() if vector == vector_required]
            # move the bot in direction
            mem_out, inputs_out, pos_out, rel_pos_out, last_output, state = stepper_computer(mem_out, d, pos_out,
                                                                                             rel_pos_out)

            result = last_output[0]

            if result == 1:  # if wall was encountered show it on map
                position = position_target
            else:
                print("Tried to moved back but encountered", result)
                exit(1)

                break

exit(0)

while state not in ["halted", 'error']:

    while True:

        # print("In position", position)

        for d in 4, 3, 2, 1:  # north (1), south (2), west (3), and east (4)

            track_dict = {(x, y): 1 for x, y in track}
            position_dict = {position: 1}
            start = {(0, 0): 1}

            # print(Counter([x for x in explored.values()]))
            display_board([explored, track_dict, start, position_dict], translations, empty)
            input("press ENTER to continue")
            # time.sleep(0.15)

            vector = vectors[d]
            position_probed = (vector[0] + position[0], vector[1] + position[1])

            if True:
                try:  # check if direction is explored
                    report = explored[position_probed]
                    # print("   checking dir", d, " explored position", position_probed, "got", explored[position_probed])
                    # pass  # todo what if direction already explored.
                    if d == 1:
                        backtracking = True

                        # print("got miself into a dead end")
                except KeyError:
                    d = d
                    backtracking = False
                if backtracking:
                    position_target = track.pop()
                    vector_required = (position_target[0] - position[0], position_target[1] - position[1])

                    d = [key for key, vector in vectors.items() if vector == vector_required]
                    # print(d)
            # not explored - try to move the bot in direction
            mem_out, inputs_out, pos_out, rel_pos_out, last_output, state = stepper_computer(mem_out, d, pos_out,
                                                                                             rel_pos_out)
            # print(last_output)
            if last_output[0] == 0:  # if hit a wall
                explored[position_probed] = 0
                # print("   probed position", position_probed, "got", last_output)
                if d == 1:
                    backtracking = True
                    # print("got miself into a dead end")
                    if position == (0, 0):
                        print("we are back at the begginning and explored all directions")
                        display_board([explored, track_dict, start, position_dict], translations, empty)
                        exit(0)
                continue
            elif last_output[0] == 1:  # empty space
                track.append(position)  # trace the positions
                position = position_probed
                explored[position_probed] = 1
                # print("   probed position", position_probed, "got", last_output)
            elif last_output[0] == 2:
                backtracking = False
                break
            else:
                print("Znalazłem hej widzę coś co nie jest 0,1", last_output, " powrót zajmie mi", len(track))
                exit(0)

    # state of the intcomp
    # print("state:", state)

    # halt if intcomp halted
    if state == "halted":
        break
    # print(last_output)
    # outputs.append(last_output[0])

exit(0)
print(x)
print(sum(x.values()))

list_of_points = [point for point, value in trace.items() if value == 1]

print(list_of_points)

x = [x[0] for x in list_of_points]
y = [y[1] for y in list_of_points]

t = np.array(x)
s = np.array(y)  # 1 + np.sin(2 * np.pi * t)

fig, ax = plt.subplots()
ax.plot(t, s, marker='o', linestyle='None')

ax.set(xlabel='time (s)', ylabel='voltage (mV)',
       title='About as simple as it gets, folks')
ax.grid()

# fig.savefig("test.png")
plt.show()
