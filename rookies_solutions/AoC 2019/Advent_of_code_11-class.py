import pandas as pd
# import easygui
# import os
import math
import copy
from pathlib import PureWindowsPath
from collections import deque
from collections import defaultdict
from collections import Counter
# import matplotlib
import matplotlib.pyplot as plt
import numpy as np


def mass_calculator(mass):
    return math.floor(mass / 3) - 2


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

            unconsumed_inputs = list(deque(input_x))
            return mem, unconsumed_inputs, pos+length, rel_pos, output_list[0], "waiting to resume after output"
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


class intcomp:
    # intcomp class
    def __init__(self, mem):  # , input_list=[], starting_pos=0, relative_pos=0):
        self.mem = mem
        self.input_list = []
        self.pos = 0
        self.rel_pos = 0
        self.output_list = []
        self.state = "initiated"

    def run(self, input_override, finish="halted"):
        self.state = "running"
        counter = 0
        while self.state not in [ "halted","error" ] and counter < int(finish):
            self.mem, self.input_list, self.pos, self.rel_pos, last_output, self.state = stepper_computer(self.mem,
                                                                                                      input_override,
                                                                                                      self.pos,
                                                                                                      self.rel_pos)
            self.output_list.append(last_output)
            counter += 1
            if finish == "onestep":
                return last_output
            if finish == "waiting" and self.state == "waiting for input":
                bring_back = self.output_list
                self.output_list = []
                return bring_back
            if self.state == "halted":
                break

        bring_back = self.output_list
        self.output_list = []
        return bring_back


def constant_factory():
    return lambda: -1

    # print(opcode)
    # return mem,output_list


# x=list(range(100))
# z=iter(x)
# print(next(z))
# print(next(z))
# print(next(z))
# print(list(deque(z)))#,maxlen=0))
#
# exit(0)

# print ([0]*10)
# x=[0]
# x.extend([1]*10)
# print(x)
# exit(0)

path = PureWindowsPath(r"C:\Users\boda9003\Desktop\Python_playground\Advent of Code\Inputs\stepper_computer_7.csv")
# input read out
# noinspection PyTypeChecker
input_file = pd.read_csv(path, header=None, sep=";", dtype=str)
starting_file = input_file.values.astype("int")[0].tolist()

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
program = [3, 8, 1005, 8, 325, 1106, 0, 11, 0, 0, 0, 104, 1, 104, 0, 3, 8, 102, -1, 8, 10, 1001, 10, 1, 10, 4, 10, 108,
           0, 8, 10, 4, 10, 101, 0, 8, 28, 2, 3, 7, 10, 2, 1109, 3, 10, 2, 102, 0, 10, 2, 1005, 12, 10, 3, 8, 102, -1,
           8, 10, 101, 1, 10, 10, 4, 10, 1008, 8, 0, 10, 4, 10, 101, 0, 8, 67, 2, 109, 12, 10, 1, 1003, 15, 10, 3, 8,
           1002, 8, -1, 10, 1001, 10, 1, 10, 4, 10, 108, 1, 8, 10, 4, 10, 101, 0, 8, 96, 3, 8, 102, -1, 8, 10, 101, 1,
           10, 10, 4, 10, 1008, 8, 0, 10, 4, 10, 1002, 8, 1, 119, 3, 8, 102, -1, 8, 10, 1001, 10, 1, 10, 4, 10, 1008, 8,
           0, 10, 4, 10, 101, 0, 8, 141, 3, 8, 1002, 8, -1, 10, 101, 1, 10, 10, 4, 10, 108, 0, 8, 10, 4, 10, 1001, 8, 0,
           162, 1, 106, 17, 10, 1006, 0, 52, 1006, 0, 73, 3, 8, 102, -1, 8, 10, 1001, 10, 1, 10, 4, 10, 108, 1, 8, 10,
           4, 10, 1001, 8, 0, 194, 1006, 0, 97, 1, 1004, 6, 10, 1006, 0, 32, 2, 8, 20, 10, 3, 8, 102, -1, 8, 10, 101, 1,
           10, 10, 4, 10, 1008, 8, 1, 10, 4, 10, 102, 1, 8, 231, 1, 1, 15, 10, 1006, 0, 21, 1, 6, 17, 10, 2, 1005, 8,
           10, 3, 8, 102, -1, 8, 10, 101, 1, 10, 10, 4, 10, 108, 1, 8, 10, 4, 10, 102, 1, 8, 267, 2, 1007, 10, 10, 3, 8,
           1002, 8, -1, 10, 1001, 10, 1, 10, 4, 10, 1008, 8, 1, 10, 4, 10, 102, 1, 8, 294, 1006, 0, 74, 2, 1003, 2, 10,
           1, 107, 1, 10, 101, 1, 9, 9, 1007, 9, 1042, 10, 1005, 10, 15, 99, 109, 647, 104, 0, 104, 1, 21101,
           936333018008, 0, 1, 21101, 342, 0, 0, 1106, 0, 446, 21102, 937121129228, 1, 1, 21101, 0, 353, 0, 1105, 1,
           446, 3, 10, 104, 0, 104, 1, 3, 10, 104, 0, 104, 0, 3, 10, 104, 0, 104, 1, 3, 10, 104, 0, 104, 1, 3, 10, 104,
           0, 104, 0, 3, 10, 104, 0, 104, 1, 21101, 0, 209383001255, 1, 21102, 400, 1, 0, 1106, 0, 446, 21101, 0,
           28994371675, 1, 21101, 411, 0, 0, 1105, 1, 446, 3, 10, 104, 0, 104, 0, 3, 10, 104, 0, 104, 0, 21101,
           867961824000, 0, 1, 21101, 0, 434, 0, 1106, 0, 446, 21102, 1, 983925674344, 1, 21101, 0, 445, 0, 1106, 0,
           446, 99, 109, 2, 21201, -1, 0, 1, 21102, 40, 1, 2, 21101, 477, 0, 3, 21102, 467, 1, 0, 1106, 0, 510, 109, -2,
           2106, 0, 0, 0, 1, 0, 0, 1, 109, 2, 3, 10, 204, -1, 1001, 472, 473, 488, 4, 0, 1001, 472, 1, 472, 108, 4, 472,
           10, 1006, 10, 504, 1101, 0, 0, 472, 109, -2, 2106, 0, 0, 0, 109, 4, 1201, -1, 0, 509, 1207, -3, 0, 10, 1006,
           10, 527, 21102, 1, 0, -3, 21202, -3, 1, 1, 21201, -2, 0, 2, 21102, 1, 1, 3, 21102, 1, 546, 0, 1106, 0, 551,
           109, -4, 2105, 1, 0, 109, 5, 1207, -3, 1, 10, 1006, 10, 574, 2207, -4, -2, 10, 1006, 10, 574, 22101, 0, -4,
           -4, 1105, 1, 642, 21202, -4, 1, 1, 21201, -3, -1, 2, 21202, -2, 2, 3, 21101, 0, 593, 0, 1105, 1, 551, 22102,
           1, 1, -4, 21101, 1, 0, -1, 2207, -4, -2, 10, 1006, 10, 612, 21102, 1, 0, -1, 22202, -2, -1, -2, 2107, 0, -3,
           10, 1006, 10, 634, 21201, -1, 0, 1, 21101, 634, 0, 0, 105, 1, 509, 21202, -2, -1, -2, 22201, -4, -2, -4, 109,
           -5, 2106, 0, 0]

# initiate the intcomp - modified to run until halted or run out of inputs
# mem_out = copy.copy(program)  # memory outside of running intcopm
# inputs_out = []  # input list
# pos_out = 0  # starting position
# rel_pos_out = 0  # relative position for relative mode
intcomp1 = intcomp(copy.copy(program) )



# initiate state and outputs list
outputs = []

# inititate board
position = (0, 0)
vector = (0, 1)
trace = {}  # defaultdict(constant_factory())
trace[position] = 1
# print(vector)
# exit(0)


while intcomp1.state not in ["halted","error"]:

    # color of tile under
    try:
        color = trace[position]
    except KeyError:
        trace[position] = -1
        color = trace[position]

    if color == -1:
        color = 0

    inputs_out = [color]

    # print("trace:", position, trace[position])

    # consume first input and run the intcomp
    # mem_out, inputs_out, pos_out, rel_pos_out, last_output, state = stepper_computer(mem_out, inputs_out, pos_out,rel_pos_out)
    last_output = intcomp1.run(inputs_out, finish = 2)
    # print(last_output)
    if intcomp1.state == "halted":
        break

    # paint the tile
    trace[position] = last_output[0]

    # raport
    # print("lastOUT:", last_output)
    outputs.append(last_output)

    # turn and move
    if last_output[1] == 0:  # turn left
        vector = (-vector[1], vector[0])
    else:
        vector = (vector[1], -vector[0])
    position = (position[0] + vector[0], position[1] + vector[1])

    # raport
    # print(position)

    # halt if intcomp halted

    # print(last_output)
    # outputs.append(last_output[0])

print("rawoutputs", outputs)

print("outputtrace:", trace)

x = Counter(trace.values())

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
