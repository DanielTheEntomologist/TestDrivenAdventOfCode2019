import pandas as pd
import easygui
import os
import math
import copy
from pathlib import PureWindowsPath
import matplotlib
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
    modes_int = [int(x) for x in r_inst[2:]]

    # print("optained opcode", opcode, " with modes", modes)

    return opcode_int, modes_int


def pointers_get(parameters, modes, pos):
    # INPUT: list of parameters , string of modes
    # OUTPUT: list of addreses on which to perform operations

    # print("read parameters:", parameters)

    pointers = []
    for i, parameter in enumerate(parameters):
        if modes[i] == 0:
            pointers.append(parameter)
        else:
            pointers.append(pos + 1 + i)

    # print("obtained pointers:", pointers)
    return pointers


def init_command(pos, length, modes, mem):
    parameters = mem[pos + 1:pos + length]
    pointers = pointers_get(parameters, modes, pos)
    return pointers


def stepper_computer(mem, input_list, starting_pos=0):
    pos = starting_pos
    #print( "starting pos", pos)
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
        #print("opcode",opcode)
        if opcode == 99:
            length = 1
            #"halting amplifier"
            output_list.append(None)
            return [99], output_list, 0, "halted"
        elif opcode == 1:  # addition
            length = 4
            pointers = init_command(pos, length, modes, mem)
            mem[pointers[2]] = int(mem[pointers[1]]) + int(mem[pointers[0]])
            # print("new value at final adress should be:", int(mem[pointers[1]]) + int(mem[pointers[0]]))
            # print("new value at final adress is:", mem[pointers[2]])
        elif opcode == 2:  # multiplication
            length = 4
            pointers = init_command(pos, length, modes, mem)
            mem[pointers[2]] = int(mem[pointers[1]]) * int(mem[pointers[0]])

        elif opcode == 3:  # input
            length = 2
            pointers = init_command(pos, length, modes, mem)
            try:
                temp = next(input_x)
                mem[pointers[0]] = int(temp)
            except StopIteration:
            #    print("Intcomp waiting for input")
                pos = pos# + length
                return mem, output_list, pos, "waiting for input"
            # int(input("provide input\n"))
            # mem[pointers[0]] = int(100 * input_1 + input_2)
            # mem[parameters[1]] = mem[0]
        elif opcode == 4:  # output
            length = 2
            pointers = init_command(pos, length, modes, mem)
            # print("output", mem[pointers[0]])
            output_list.append(mem[pointers[0]])
            #print("Intcomp returning output")
            pos = pos + length
            return mem, output_list, pos, "waiting to resume after output"
        elif opcode == 5:  #jump if true
            length = 3
            pointers = init_command(pos, length, modes, mem)
            if mem[pointers[0]] != 0:
                pos = mem[pointers[1]]
                jump = True
        elif opcode == 6:  # jump if false
            length = 3
            pointers = init_command(pos, length, modes, mem)
            if mem[pointers[0]] == 0:
                pos = mem[pointers[1]]
                jump = True
        elif opcode == 7:  # less than
            length = 4
            pointers = init_command(pos, length, modes, mem)
            if mem[pointers[0]] < mem[pointers[1]]:
                mem[pointers[2]] = 1
            else:
                mem[pointers[2]] = 0
        elif opcode == 8:  # equal
            length = 4
            pointers = init_command(pos, length, modes, mem)
            if mem[pointers[0]] == mem[pointers[1]]:
                mem[pointers[2]] = 1
            else:
                mem[pointers[2]] = 0
        else:
            length = 0
            print("no valid opcode detected exiting")
            return mem, output_list, pos, "no valid opcode detected exiting"
        # print("moving to next step\n")
        if not jump:
            pos = pos + length

        # print(opcode)
    # return mem,output_list


path = PureWindowsPath(r"C:\Users\boda9003\Desktop\Python_playground\Advent of Code\Inputs\stepper_computer_7.csv")
# input read out
input_file = pd.read_csv(path, header=None, sep=";", dtype=str)
starting_file = input_file.values.astype("int")[0].tolist()

# program = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
# program = [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]
program = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]
program = starting_file

#phases = [9,7,8,5,6]

mem_list = [copy.deepcopy(program) for x in range(5)]
#pos_list = [-2, -2, -2, -2, -2]
pos_list = [0, 0, 0, 0, 0]
last_output = [0]


final = []
max_phase = 0
max_power = 0
for p1 in range(5, 10):
    for p2 in [x for x in range(5, 10) if x not in [p1]]:
        for p3 in [x for x in range(5, 10) if x not in [p1, p2]]:
            for p4 in [x for x in range(5, 10) if x not in [p1, p2, p3]]:
                for p5 in [x for x in range(5, 10) if x not in [p1, p2, p3, p4]]:
                    #  here test the system for phases combination
                    phases = [p1, p2, p3, p4, p5]
                    print(phases)
                    # initiate memeory here
                    mem_list = [copy.deepcopy(program) for x in range(5)]
                    states = [0,0,0,0,0]
                    pos_list = [0,0,0,0,0]
                    last_output = [0]
                    outputs_run = []
                    # initialise phases
                    for j in range(5):
                        mem_list[j], plchldr, pos_list[j],states[j] = stepper_computer(mem_list[j], phases[j], pos_list[j])
                        #print(states[j])
                    while True:
                        #print("trying phases",phases)
                        for j in range(5):
                            #print(mem_list[j])
                            #print("initiating amp",j,"with inputs:",phases[j],"(phase) and:",last_output[0] ,"on position", pos_list[j])
                            #print("in pos list mem",mem_list[j][pos_list[j]])
                            #print("mem list", mem_list[j])
                            #print("initiating amp", j, "with input (signal)", last_output[0], " on position",pos_list[j])
                            #print(mem_list[j])
                            mem_list[j], last_output, pos_list[j],states[j] = stepper_computer(mem_list[j], last_output[0], pos_list[j])
                            #print(last_output)
                            outputs_run.append(copy.copy(last_output))

                        #print([x[0]==99 for x in mem_list])
                        #print(states)
                        if all([x == 'halted' for x in states]):
                            #print(outputs)
                            #if (0 or last_output[0]) > max_power:
                            #    max_power = last_output[0]
                            #    max_phase = phases
                            break
                    print((max(list(filter(None, [x[0] for x in outputs_run])))))

                    final.append(max(list(filter(None, [x[0] for x in outputs_run]))))

                            # print("ran ", i, "module with phase",j,"and input",last_output," Got in return:", max_power[j])
                        #outputs.append(last_output)
print(max(final))
#outputs = list(filter(None, [x[0] for x in outputs]))
#print(outputs)
#print(max(outputs))

#print(max_power, max_phase)

exit(0)
for i in range(5):

    max_phase[i] = 0
    max_phase[i] = 0

    for j in range(5):
        x, last_maximiser = stepper_computer(copy.deepcopy(program), [j, last_output[0]])
        if max_power[j] < last_maximiser[0]:
            max_power[j] = last_maximiser[0]
            max_phase[j] = j
        print("ran ", i, "module with phase", j, "and input", last_output, " Got in return:", max_power[j])
    last_output[0] = max(max_power)
    outputs.append(max(max_power))
    # print(output)
exit(0)

phase = 2
output = []
input = []
for x in range(0, 5, 1):
    z, outputx = stepper_computer(program.copy(), [x, 10000])
    output.append(outputx[0])
    input.append(x)
    print(x, outputx)

# rint(operating_file[0])


# Data for plotting
t = np.array(input)
s = np.array(output)  # 1 + np.sin(2 * np.pi * t)

fig, ax = plt.subplots()
ax.plot(t, s)

ax.set(xlabel='time (s)', ylabel='voltage (mV)',
       title='About as simple as it gets, folks')
ax.grid()

fig.savefig("test.png")
plt.show()
