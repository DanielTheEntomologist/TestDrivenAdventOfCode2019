import aoc_helper as hlp

import intcode_vm as intcode
if __name__ == "__main__":
    # Part 1
    file = "inputs/2019_02_a.txt"
    
    
    input = hlp.read_intcode_program(file)

    intcode_vm = intcode.IntCodeVM(input)
    
    # modify memory to put program in "1202 state"
    intcode_vm.memory[1] = 12
    intcode_vm.memory[2] = 2

    intcode_vm.run()
    answer = intcode_vm.memory[0]

    print("Answer to part 1 of Day 1 is: ", answer)

    # answer = fuel_required_to_launch_ship_exponential(input)
    # print("Answer to part 2 of Day 1 is: ", answer)