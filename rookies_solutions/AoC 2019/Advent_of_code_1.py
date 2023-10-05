import pandas as pd
import easygui
import os
import math
from pathlib import Path, PureWindowsPath



def mass_calculator(mass):
    return math.floor(mass/3)-2

# Ask user to select input file
#path = easygui.fileopenbox('Please select input file')


path = PureWindowsPath("C:\\Users\\boda9003\\Desktop\\Python_playground\\Inputs\\rocket_equation.csv")

print(path)
# Load selected file
input_file = pd.read_csv(path, dtype=str)

i=0
fuel=0
print(input_file)


print (int(input_file.values[1]))

for i in range(len(input_file)):
    fuelx=mass_calculator(int(input_file.values[i]))
    fuel=fuel+fuelx
    while mass_calculator(fuelx)>0 :
        fuelx=mass_calculator(fuelx)
        fuel=fuel+fuelx
    i=i+1
    print("Module "+str(i)+" weighs "+str(input_file.values[i-1])+" and will take "+str(fuelx)+" fuel to carry")
    
print("this is the result: "+str(fuel))
print(i)

input("press enter to exit")
