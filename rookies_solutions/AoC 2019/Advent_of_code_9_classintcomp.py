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

# BOOST program:
program = [1102, 34463338, 34463338, 63, 1007, 63, 34463338, 63, 1005, 63, 53, 1101, 3, 0, 1000, 109, 988, 209, 12, 9,
           1000, 209, 6, 209, 3, 203, 0, 1008, 1000, 1, 63, 1005, 63, 65, 1008, 1000, 2, 63, 1005, 63, 902, 1008, 1000,
           0, 63, 1005, 63, 58, 4, 25, 104, 0, 99, 4, 0, 104, 0, 99, 4, 17, 104, 0, 99, 0, 0, 1101, 26, 0, 1015, 1101,
           29, 0, 1010, 1102, 1, 24, 1013, 1102, 1, 33, 1008, 1102, 36, 1, 1012, 1101, 0, 572, 1023, 1101, 35, 0, 1014,
           1101, 0, 38, 1019, 1102, 1, 30, 1006, 1101, 0, 890, 1029, 1101, 34, 0, 1011, 1101, 28, 0, 1002, 1102, 1, 1,
           1021, 1101, 0, 37, 1001, 1101, 0, 197, 1026, 1101, 22, 0, 1017, 1102, 1, 895, 1028, 1101, 0, 20, 1007, 1102,
           21, 1, 1004, 1102, 1, 39, 1016, 1101, 0, 0, 1020, 1102, 1, 190, 1027, 1101, 0, 775, 1024, 1102, 31, 1, 1018,
           1101, 0, 23, 1003, 1101, 0, 25, 1009, 1101, 770, 0, 1025, 1101, 0, 27, 1000, 1102, 1, 575, 1022, 1101, 0, 32,
           1005, 109, 27, 2106, 0, 0, 1001, 64, 1, 64, 1106, 0, 199, 4, 187, 1002, 64, 2, 64, 109, -18, 21101, 40, 0, 5,
           1008, 1014, 39, 63, 1005, 63, 219, 1106, 0, 225, 4, 205, 1001, 64, 1, 64, 1002, 64, 2, 64, 109, -6, 1201, -1,
           0, 63, 1008, 63, 28, 63, 1005, 63, 251, 4, 231, 1001, 64, 1, 64, 1105, 1, 251, 1002, 64, 2, 64, 109, 5,
           21102, 41, 1, 3, 1008, 1011, 38, 63, 1005, 63, 271, 1105, 1, 277, 4, 257, 1001, 64, 1, 64, 1002, 64, 2, 64,
           109, -7, 2102, 1, 1, 63, 1008, 63, 28, 63, 1005, 63, 299, 4, 283, 1106, 0, 303, 1001, 64, 1, 64, 1002, 64, 2,
           64, 109, -7, 1207, 10, 22, 63, 1005, 63, 321, 4, 309, 1106, 0, 325, 1001, 64, 1, 64, 1002, 64, 2, 64, 109,
           16, 2107, 31, -4, 63, 1005, 63, 345, 1001, 64, 1, 64, 1105, 1, 347, 4, 331, 1002, 64, 2, 64, 109, -9, 1201,
           3, 0, 63, 1008, 63, 18, 63, 1005, 63, 371, 1001, 64, 1, 64, 1106, 0, 373, 4, 353, 1002, 64, 2, 64, 109, 7,
           1202, -7, 1, 63, 1008, 63, 40, 63, 1005, 63, 393, 1106, 0, 399, 4, 379, 1001, 64, 1, 64, 1002, 64, 2, 64,
           109, -5, 1208, 5, 33, 63, 1005, 63, 417, 4, 405, 1106, 0, 421, 1001, 64, 1, 64, 1002, 64, 2, 64, 109, 1,
           1202, 2, 1, 63, 1008, 63, 30, 63, 1005, 63, 443, 4, 427, 1105, 1, 447, 1001, 64, 1, 64, 1002, 64, 2, 64, 109,
           -7, 2102, 1, 10, 63, 1008, 63, 19, 63, 1005, 63, 471, 1001, 64, 1, 64, 1105, 1, 473, 4, 453, 1002, 64, 2, 64,
           109, 6, 2108, 21, 0, 63, 1005, 63, 489, 1105, 1, 495, 4, 479, 1001, 64, 1, 64, 1002, 64, 2, 64, 109, 9,
           21108, 42, 42, 0, 1005, 1012, 513, 4, 501, 1105, 1, 517, 1001, 64, 1, 64, 1002, 64, 2, 64, 109, 7, 21107, 43,
           44, -1, 1005, 1018, 535, 4, 523, 1106, 0, 539, 1001, 64, 1, 64, 1002, 64, 2, 64, 109, -5, 21101, 44, 0, 2,
           1008, 1016, 44, 63, 1005, 63, 561, 4, 545, 1105, 1, 565, 1001, 64, 1, 64, 1002, 64, 2, 64, 2105, 1, 9, 1106,
           0, 581, 4, 569, 1001, 64, 1, 64, 1002, 64, 2, 64, 109, 13, 21107, 45, 44, -9, 1005, 1018, 597, 1105, 1, 603,
           4, 587, 1001, 64, 1, 64, 1002, 64, 2, 64, 109, -25, 2101, 0, 3, 63, 1008, 63, 32, 63, 1005, 63, 625, 4, 609,
           1105, 1, 629, 1001, 64, 1, 64, 1002, 64, 2, 64, 109, 7, 1208, -7, 30, 63, 1005, 63, 645, 1105, 1, 651, 4,
           635, 1001, 64, 1, 64, 1002, 64, 2, 64, 109, -2, 21102, 46, 1, 9, 1008, 1016, 46, 63, 1005, 63, 677, 4, 657,
           1001, 64, 1, 64, 1106, 0, 677, 1002, 64, 2, 64, 109, -2, 21108, 47, 48, 9, 1005, 1014, 697, 1001, 64, 1, 64,
           1105, 1, 699, 4, 683, 1002, 64, 2, 64, 109, 14, 1205, 2, 713, 4, 705, 1105, 1, 717, 1001, 64, 1, 64, 1002,
           64, 2, 64, 109, -7, 1206, 8, 735, 4, 723, 1001, 64, 1, 64, 1106, 0, 735, 1002, 64, 2, 64, 109, -18, 2101, 0,
           6, 63, 1008, 63, 24, 63, 1005, 63, 759, 1001, 64, 1, 64, 1106, 0, 761, 4, 741, 1002, 64, 2, 64, 109, 29,
           2105, 1, 1, 4, 767, 1106, 0, 779, 1001, 64, 1, 64, 1002, 64, 2, 64, 109, -5, 1206, 3, 791, 1106, 0, 797, 4,
           785, 1001, 64, 1, 64, 1002, 64, 2, 64, 109, -12, 2107, 31, -1, 63, 1005, 63, 819, 4, 803, 1001, 64, 1, 64,
           1105, 1, 819, 1002, 64, 2, 64, 109, 7, 1205, 7, 835, 1001, 64, 1, 64, 1105, 1, 837, 4, 825, 1002, 64, 2, 64,
           109, -11, 1207, 7, 24, 63, 1005, 63, 853, 1106, 0, 859, 4, 843, 1001, 64, 1, 64, 1002, 64, 2, 64, 109, 4,
           2108, 27, -6, 63, 1005, 63, 881, 4, 865, 1001, 64, 1, 64, 1106, 0, 881, 1002, 64, 2, 64, 109, 24, 2106, 0,
           -2, 4, 887, 1106, 0, 899, 1001, 64, 1, 64, 4, 64, 99, 21102, 27, 1, 1, 21101, 0, 913, 0, 1106, 0, 920, 21201,
           1, 61934, 1, 204, 1, 99, 109, 3, 1207, -2, 3, 63, 1005, 63, 962, 21201, -2, -1, 1, 21101, 0, 940, 0, 1106, 0,
           920, 21202, 1, 1, -1, 21201, -2, -3, 1, 21101, 0, 955, 0, 1105, 1, 920, 22201, 1, -1, -2, 1105, 1, 966,
           22102, 1, -2, -2, 109, -3, 2105, 1, 0]




print("Part 1")
comp1 = IntComp(program)
print("intcomp 1:", comp1.state)
# input the command
#comp1.inputs.append()
# advance until halted
comp1.advance(until="output")
comp1.advance(until="output")
comp1.advance()
# provide output
print("intcomp 1:", comp1.state)
comp1.inputs.append(1)
comp1.advance(until="output")
comp1.advance(until="output")
print("intcomp 1:", comp1.state)
print("answer 1:", comp1.outputs)

print("\nPart 2")
comp2 = IntComp(program)
print("intcomp 2:", comp2.state)
# input the command
comp2.inputs.append(2)
# advance until halted
comp2.advance()
# provide output
print("intcomp 2:", comp2.state)
print("answer 2:", comp2.outputs)
