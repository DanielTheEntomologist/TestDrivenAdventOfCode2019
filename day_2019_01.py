from math import floor

import aoc_helper as hlp

def fuel_required_to_launch(mass):
    mass = int(mass)
    fuel = max(floor(mass / 3) - 2,0)
    return fuel

def fuel_required_to_launch_exponential(mass):
    
    mass = int(mass)
    
    total_fuel = 0
    fuel = max(floor(mass / 3) - 2,0)
    
    while fuel > 0:
        total_fuel = total_fuel + fuel
        fuel = max(floor(fuel / 3) - 2,0)
    
    return total_fuel

def total_fuel_required(module_masses:list):
    
    total_fuel_required = 0
    for module_mass in module_masses:
        total_fuel_required += fuel_required_to_launch(module_mass)
    
    return total_fuel_required

def total_fuel_required_exponential(module_masses:list):
    
    total_fuel_required = 0
    for module_mass in module_masses:
        total_fuel_required += fuel_required_to_launch_exponential(module_mass)
    
    return total_fuel_required


if __name__ == "__main__":
    file = "inputs/2019_01_a.txt"
    input = hlp.read_lines(file)
    answer = total_fuel_required(input)
    print("Answer to part 1 of Day 1 is: ", answer)

    answer = total_fuel_required_exponential(input)
    print("Answer to part 2 of Day 1 is: ", answer)
