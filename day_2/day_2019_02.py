import os
import sys
# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import aoc_helper.aoc_helper as hlp
from intcode_vm import IntCodeVM

def run_vm_with_noun_and_verb(program, noun, verb):
    vm = IntCodeVM(program)
    vm.memory[1] = noun
    vm.memory[2] = verb
    vm.run()
    return vm.memory[0]


if __name__ == "__main__":
    # Part 1
    file = "inputs/2019_02_a.txt"
        
    program = hlp.read_intcode_program(file)
    

    intcode_vm = IntCodeVM(program)
    
    # modify memory to put program in "1202 state"
    intcode_vm.memory[1] = 12
    intcode_vm.memory[2] = 2

    intcode_vm.run()
    answer = intcode_vm.memory[0]

    print("Answer to part 1 of Day 1 is: ", answer)


    # Using concurrent.futures.ProcessPoolExecutor 
    # to run the program with all possible combinations of noun and verb
    
    from itertools import product

    inputs = product(range(100), range(100))
    
    import concurrent.futures

    with concurrent.futures.ProcessPoolExecutor() as executor:
        
        futures = {executor.submit(run_vm_with_noun_and_verb, program, noun, verb): (noun,verb) for noun, verb in inputs}

        for future in concurrent.futures.as_completed(futures):
            noun,verb = futures[future]
            result = future.result()
            if result == 19690720:
                print("Answer to part 2 of Day 1 is: ", 100*noun+verb)
                for future in futures:
                    future.cancel()   
                break
    