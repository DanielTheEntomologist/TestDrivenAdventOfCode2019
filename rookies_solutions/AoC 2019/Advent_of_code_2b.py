import pandas as pd
import easygui
import os
import math
import copy
from pathlib import PureWindowsPath


def mass_calculator(mass):
    return math.floor(mass / 3) - 2


# Ask user to select input file
# path = easygui.fileopenbox('Please select input file')


path = PureWindowsPath(r"C:\Users\boda9003\Desktop\Python_playground\Advent of Code\Inputs\stepper_computer.csv")

# Load selected file

# input read out
input_file = pd.read_csv(path, header=None, sep=";", dtype=str)

starting_file = input_file.values.astype("int")
print(starting_file[0])

operating_file = copy.copy(starting_file[0])
print(operating_file[0])

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
