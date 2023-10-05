import pandas as pd
import easygui
import os
import math
from pathlib import Path, PureWindowsPath



def mass_calculator(mass):
    return math.floor(mass/3)-2

# Ask user to select input file
#path = easygui.fileopenbox('Please select input file')


path = PureWindowsPath("C:\\Users\\boda9003\\Desktop\\Python_playground\\Inputs\\stepper_computer.csv")

print(path)
# Load selected file

#x=list(range(100))
#print(x)

#input read out
input_file = pd.read_csv(path, header=None, sep=";", dtype=str)





#changing the data frame into numpy vector
operating_file=input_file.values.astype("int")

operating_file=operating_file[0]
print("printing processed input:\n",operating_file)

#operating_file=operating_file.transpose()

input("press enter to execute program on above input")
#"initialise the program"

operating_file[1]=12
operating_file[2]=2
position=0

#execute program
while int(operating_file[position])!=99:
        zero=int(operating_file[position])
        jeden=int(operating_file[position+1])
        dwa=int(operating_file[position+2])
        trzy=int(operating_file[position+3])
        if int(zero)==1 :
            operating_file[trzy]=int(operating_file[jeden])+int(operating_file[dwa])
        elif zero==2:
            operating_file[int(trzy)]=int(operating_file[int(jeden)])*int(operating_file[int(dwa)])
        position=position+4

print("this is the output of serial computer on the provided input\n",operating_file)


print("comparison of input to output\n",input_file.values.astype("int")==operating_file)




input("press enter to exit")
