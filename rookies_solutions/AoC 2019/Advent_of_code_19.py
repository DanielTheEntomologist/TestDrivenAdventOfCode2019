# import re
# import copy
# from collections import Counter
# from collections import defaultdict
# from collections import OrderedDict
# import numpy as np
# from collections import deque
# import math
import itertools
# import time
# from operator import itemgetter
# from functools import reduce
# import networkx as nx
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


class IntComp():
    def __init__(self, memory_init):
        self.mem = memory_init.copy()
        self.pos = 0
        self.rel_pos = 0
        self.inputs = deque()
        self.outputs = list()
        self.state = "initialised"
        self.unconsumed_inputs = deque()

    # functions
    # advance until ( input, outputs, halted )
    #

    def decode_opcode(self, opcode_int):
        # print("decoding opcode:", opcode_int)
        opcode_str = str(opcode_int)
        lenght_of_instruction = 5
        r_inst = opcode_str[-1::-1] + "0" * (lenght_of_instruction - len(opcode_str))
        # print(r_inst)
        opcode_int = int(r_inst[1::-1])  # [int(x) for x in r_inst[1::-1]]
        modes_int = [int(x) for x in r_inst[2:]]

        # print("optained opcode", opcode, " with modes", modes)

        return opcode_int, modes_int

    def pointers_get(self, parameters, modes):
        # INPUT: list of parameters , string of modes
        # OUTPUT: list of addreses on which to perform operations

        # print("read parameters:", parameters)

        pointers = []
        for m, parameter in enumerate(parameters):
            if modes[m] == 0:
                pointers.append(parameter)
            elif modes[m] == 1:
                pointers.append(self.pos + 1 + m)
            elif modes[m] == 2:
                pointers.append(parameter + self.rel_pos)
            else:
                print("ERROR - invalid mode read in:", modes)
                exit(0)

        overflow = max(pointers) - len(self.mem) + 1
        if overflow > 0:
            self.mem.extend([0] * overflow)
        # print("obtained pointers:", pointers)
        if min(pointers) < 0:
            print("ERROR - trying to use negative address with:", pointers)
        return pointers

    def init_command(self, length, modes):
        parameters = self.mem[self.pos + 1:self.pos + length]
        pointers = self.pointers_get(parameters, modes)
        return pointers

    def advance(self, until="halted"):

        # print("initialised with position", pos)
        # print("initialised with relative position", rel_pos)
        # print("initialised with input list", input_list)

        while True:
            # print("starting at position ", pos)
            # print("next 4 positions in mem are", mem[pos:pos + 4])
            jump = False
            opcode, modes = self.decode_opcode(self.mem[self.pos])
            # print(opcode, modes)
            # print("opcode",opcode)
            if opcode == 99:  # halt
                # length = 1
                # output_list.append("halted")
                self.unconsumed_inputs = self.inputs
                # print("halted")
                last_action = "halt"
                self.state = "halted"
                return None
            elif opcode == 1:  # addition
                length = 4
                last_action = "add"
                pointers = self.init_command(length, modes)
                self.mem[pointers[2]] = int(self.mem[pointers[1]]) + int(self.mem[pointers[0]])
                # print("new value at final adress should be:", int(mem[pointers[1]]) + int(mem[pointers[0]]))
                # print("new value at final adress is:", mem[pointers[2]])
            elif opcode == 2:  # multiplication
                length = 4
                last_action = "multi"
                pointers = self.init_command(length, modes)
                self.mem[pointers[2]] = int(self.mem[pointers[1]]) * int(self.mem[pointers[0]])

            elif opcode == 3:  # input
                length = 2
                last_action = "input"
                pointers = self.init_command(length, modes)
                try:
                    temp = self.inputs.popleft()
                    self.mem[pointers[0]] = int(temp)
                except IndexError:
                    #    print("Intcomp waiting for input")
                    # pos = pos  # + length
                    self.unconsumed_inputs = self.inputs
                    self.state = "waiting for input"
                    return None
                # if until == "no_input":
                #     self.unconsumed_inputs = self.inputs
                #     self.state = "waiting for input"
                #     return None
                # int(input("provide input\n"))
                # mem[pointers[0]] = int(100 * input_1 + input_2)
                # mem[parameters[1]] = mem[0]
                # pos = pos + length
            elif opcode == 4:  # output
                length = 2
                last_action = "output"
                pointers = self.init_command(length, modes)
                # print("output", self.mem[pointers[0]])
                self.outputs.append(self.mem[pointers[0]])
                # print("Intcomp returning output")
                # pos = pos + length
                # print("going to pos", self.pos)
                # print("suspended with position", self.pos)
                # print("suspended with relative position", self.rel_pos)
                # print("suspended with input list", self.inputs)
                if until == "output":
                    self.state = "waiting after output"
                    self.unconsumed_inputs = self.inputs
                else:
                    pass

            elif opcode == 5:  # jump if true
                length = 3
                last_action = "jumpiftrue"
                pointers = self.init_command(length, modes)
                if self.mem[pointers[0]] != 0:
                    self.pos = self.mem[pointers[1]]
                    jump = True
            elif opcode == 6:  # jump if false
                length = 3
                last_action = "jumpiffalse"
                pointers = self.init_command(length, modes)
                if self.mem[pointers[0]] == 0:
                    self.pos = self.mem[pointers[1]]
                    jump = True
            elif opcode == 7:  # less than
                length = 4
                last_action = "lessthan"
                pointers = self.init_command(length, modes)
                if self.mem[pointers[0]] < self.mem[pointers[1]]:
                    self.mem[pointers[2]] = 1
                else:
                    self.mem[pointers[2]] = 0
            elif opcode == 8:  # equal
                length = 4
                last_action = "equal"
                pointers = self.init_command(length, modes)
                if self.mem[pointers[0]] == self.mem[pointers[1]]:
                    self.mem[pointers[2]] = 1
                else:
                    self.mem[pointers[2]] = 0
            elif opcode == 9:  # relative
                length = 2
                last_action = "relative"
                pointers = self.init_command(length, modes)
                self.rel_pos = self.rel_pos + self.mem[pointers[0]]
            else:
                # length = 0
                print("no valid opcode detected exiting")
                self.unconsumed_inputs = self.inputs
                self.state = "error"
                return None
            # print("moving to next step\n")
            if not jump:
                self.pos = self.pos + length
                if last_action == "output" and until == "output":
                    # print("halted after output")
                    return None


test = 0
day = 19
year = 2019
if test:
    with open(f'Inputs/{year}-{day}-test.txt') as file:  # read input
        input_list = file.read()
else:
    with open(f'Inputs/{year}-{day}.txt') as file:  # read input
        input_list = file.read()

input_list = [int(x) for x in input_list.split(",")]

print("Part 1")
program = input_list


def check_position(xi,yi):
    comp1 = IntComp(copy.deepcopy(program))
    comp1.inputs.extend([xi, yi])
    comp1.advance()
    return comp1.outputs[0]

tractor_outputs = dict()
for x, y in itertools.product(range(50), repeat=2):
    tractor_outputs[(x, y)] = check_position(x,y)

# try to move the bot in direction

print("In 50x50 square tractor beam reaches ",len({k: v for k, v in tractor_outputs.items() if v == 1}),"/",len(tractor_outputs),"squares")

print("\nPart 2")

# determine the approximate borders of the beam

right_edge = []
x = 999
for y in range(1000):
    right_edge.append(check_position(x,y))

down_edge = []
y = 999
for x in range(1000):
    down_edge.append(check_position(x,y))

print("right edge",right_edge)
print("down_edge",down_edge)

ymin = right_edge.index(1)
ymax = 1000-right_edge[::-1].index(1)
print("ymin", ymin, "ymax", ymax)

B = 99 * (1+ymin/999)
A = (ymax-ymin)/999

x0 = int(B/A)
print(x0, B/A)

def check_shadow(x_to_check):

    templist = []
    y0=int(0.99*x_to_check*ymin/999)
    y1=int(1.01*x_to_check*ymax/999)
    for y_scan in range(y0,y1):
        templist.append(check_position(x_to_check,y_scan))


    shadow1 = templist.index(1)
    shadow2 = templist[shadow1+1:].index(0) + shadow1

    shadow1 += y0
    shadow2 += y0
    return shadow1,shadow2

def check_if_fits_at_x(x_to_check):
    limlow, limup = check_shadow(x0)
    corners = [(x_to_check,limup),(x_to_check,limup-99),(x_to_check+99,limup),(x_to_check+99,limup-99)]
    checked_corners = []
    for corner in corners:
        checked_corners.append(1==check_position(*corner))
    return all(checked_corners)

limlow, limup = check_shadow(x0)
print(check_if_fits_at_x(x0))

print(check_position(x0,limup+1),check_position(x0,limup),check_position(x0,limup-1))

print(10000*x0+limup-99)

