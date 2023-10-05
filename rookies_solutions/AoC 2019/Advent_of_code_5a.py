import pandas as pd
import easygui
import os
import math
import copy
from pathlib import PureWindowsPath


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


def stepper_computer(mem, starting_pos=0):
    pos = starting_pos
    input_1 = mem[1]
    input_2 = mem[2]

    while True:
        # print("starting at position ", pos)
        # print("next 4 positions in mem are", mem[pos:pos + 4])
        jump = False
        opcode, modes = decode_opcode(mem[pos])
        if opcode == 99:
            length = 1
            break
        elif opcode == 1:  # addition
            length = 4
            pointers = init_command(pos, length, modes, mem)
            mem[pointers[2]] = mem[pointers[1]] + mem[pointers[0]]
            # print("new value at final adress should be:", int(mem[pointers[1]]) + int(mem[pointers[0]]))
            # print("new value at final adress is:", mem[pointers[2]])
        elif opcode == 2:  # multiplication
            length = 4
            pointers = init_command(pos, length, modes, mem)
            mem[pointers[2]] = int(mem[pointers[1]]) * int(mem[pointers[0]])

        elif opcode == 3:  # input
            length = 2
            pointers = init_command(pos, length, modes, mem)
            mem[pointers[0]] = int(input("provide input\n"))
            # mem[pointers[0]] = int(100 * input_1 + input_2)
            # mem[parameters[1]] = mem[0]
        elif opcode == 4:  # output
            length = 2
            pointers = init_command(pos, length, modes, mem)
            print("output", mem[pointers[0]])

        elif opcode == 5:  # output
            length = 3
            pointers = init_command(pos, length, modes, mem)
            if mem[pointers[0]] != 0:
                pos = mem[pointers[1]]
                jump = True
        elif opcode == 6:  # output
            length = 3
            pointers = init_command(pos, length, modes, mem)
            if mem[pointers[0]] == 0:
                pos = mem[pointers[1]]
                jump = True
        elif opcode == 7:  # output
            length = 4
            pointers = init_command(pos, length, modes, mem)
            if mem[pointers[0]] < mem[pointers[1]]:
                mem[pointers[2]] = 1
            else:
                mem[pointers[2]] = 0
        elif opcode == 8:  # output
            length = 4
            pointers = init_command(pos, length, modes, mem)
            if mem[pointers[0]] == mem[pointers[1]]:
                mem[pointers[2]] = 1
            else:
                mem[pointers[2]] = 0
        else:
            length = 0
            print("no valid opcode detected exiting")
            exit(0)
        # print("moving to next step\n")
        if jump == False:
            pos = pos + length

        # print(opcode)
    return mem


string = '12345532'
print([int(x) for x in string])

# exit(0)

# Ask user to select input file
# path = easygui.fileopenbox('Please select input file')


path = PureWindowsPath(r"C:\Users\boda9003\Desktop\Python_playground\Advent of Code\Inputs\stepper_computer_5.csv")

# Load selected file

# input read out
input_file = pd.read_csv(path, header=None, sep=";", dtype=str)

starting_file = input_file.values.astype("int")[0].tolist()

# starting_file[0] = 1
# starting_file[1] = 12
# starting_file[2] = 2

program = [3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
           1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
           999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99]

program = starting_file

z = stepper_computer(program)

# print(z)

# rint(operating_file[0])

exit(0)
z = 0

while int(operating_file[0]) != 19690720 and z < 100:

    x = 0
    while int(operating_file[0]) != 19690720 and x < 100:

        # changing the data frame into numpy vector

        # reset the program

        # "initialise the program"
        operating_file = copy.copy(starting_file[0])
        operating_file[1] = z
        operating_file[2] = x

        position = 0
        zero = 0
        jeden = 0
        dwa = 0
        trzy = 0
        # execute program
        while int(operating_file[position]) != 99:
            zero = int(operating_file[position])
            jeden = int(operating_file[position + 1])
            dwa = int(operating_file[position + 2])
            trzy = int(operating_file[position + 3])
            if int(zero) == 1:
                operating_file[trzy] = int(operating_file[jeden]) + int(operating_file[dwa])
            elif zero == 2:
                operating_file[int(trzy)] = int(operating_file[int(jeden)]) * int(operating_file[int(dwa)])
            position = position + 4
        print("noun: ", z, " and:", x, " resulted in output ", int(operating_file[0]))
        x = x + 1
    z = z + 1

input("press enter to exit")
