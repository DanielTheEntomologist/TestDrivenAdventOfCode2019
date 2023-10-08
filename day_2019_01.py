from math import floor

import aoc_helper as hlp

from math import floor

def fuel_required_to_launch_module(mass):
    fuel = floor(mass / 3) - 2
    fuel = max(fuel,0)
    return fuel

def fuel_required_to_launch_module_exponential(module_mass):
    total_fuel = 0
    fuel = fuel_required_to_launch_module(module_mass)
    while fuel > 0:
        total_fuel = total_fuel + fuel
        fuel = fuel_required_to_launch_module(fuel)
    return total_fuel

def fuel_required_to_launch_ship(module_masses:list[int]):
    total_fuel_required = 0
    for module_mass in module_masses:
        total_fuel_required += fuel_required_to_launch_module(module_mass)
    return total_fuel_required

def fuel_required_to_launch_ship_exponential(module_masses:list[int]):
    total_fuel = 0
    for module_mass in module_masses:
        fuel = fuel_required_to_launch_module_exponential(module_mass)
        total_fuel += fuel
    return total_fuel

if __name__ == "__main__":
    file = "inputs/2019_01_a.txt"
    input = hlp.read_integers(file)
    answer = fuel_required_to_launch_ship(input)
    print("Answer to part 1 of Day 1 is: ", answer)

    answer = fuel_required_to_launch_ship_exponential(input)
    print("Answer to part 2 of Day 1 is: ", answer)
