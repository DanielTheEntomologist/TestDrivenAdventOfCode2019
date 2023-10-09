"""Intcode VM for Advent of Code 2019

This intcode machine may be very similar to the many other
on the internet because it is done with heavy suggestion from
github copilot. Advent of Code solutions are published in countless
GitHub repos, so Copilot is heaviliy trained on AoC solutions.
At the same time it speeds up my work significantly,
so I am willing to accept this not being my 100% original bespoke code.
"""

class IntCodeVM:
    """Emulator for the IntCode computer from Advent of Code 2019

    Attributes:
        memory (list): List representing the program memory.
        position (int): Current position in the program memory.
        opcode (int): Current opcode being executed.
        opcode_length (int): Length of an opcode instruction.
        state (str): Current state of the VM ('INIT', 'RUNNING', 'HALTED', or 'ERROR').

    Methods:
        __init__(program):
            Initializes the IntCodeVM with the provided program.

        run():
            Runs the program until it is halted or an error occurs.

        step():
            Executes a single step of the program.

        halt():
            Sets the state to 'HALTED', indicating that the program has finished executing.

        add():
            Executes an addition operation.

        multiply():
            Executes a multiplication operation.
    """
    
    def __init__(self, program: list[int]):
        """
        Initialize the IntCodeVM with the provided program.

        Args:
            program (list): List of integers representing the program memory.
        """
        self.memory = program
        self.instruction_pointer = 0
        self.opcode = None
        self.instruction_length = 4
        self.state = "INIT"

    def run(self):
        """
        Run the program until it is halted or an error occurs.
        """
        self.state = "RUNNING"
        while self.state == "RUNNING":
            self.step()

    def step(self):
        """
        Execute a single step of the program.
        """
        self.opcode = self.memory[self.instruction_pointer]
        
        if self.opcode == 99:
            self.halt()
            return
        if self.opcode == 1:
            self.add()
            return
        if self.opcode == 2:
            self.multiply()
            return
        
        self.state = "ERROR"
        raise ValueError(f"Invalid opcode: {self.opcode}")

    def halt(self):
        """
        Set the state to 'HALTED', indicating that the program has finished executing.
        """
        self.state = "HALTED"

    def add(self):
        """
        Execute an addition operation.
        """
        # get full instruction from memory
        instruction = self.memory[self.instruction_pointer : self.instruction_pointer+self.instruction_length]
        # get instruction parameters
        instruction_parameters = instruction[1:]
        # get operation argument addresses
        arg1_address = instruction_parameters[0]
        arg2_address = instruction_parameters[1]
        target_address = instruction_parameters[2]
        # get operation arguments
        arg1 = self.memory[arg1_address]
        arg2 = self.memory[arg2_address]
        # perform operation 
        sum = arg1 + arg2
        # store result
        self.memory[target_address] = sum
        # increment instruction pointer
        self.instruction_pointer += self.instruction_length

    def multiply(self):
        """
        Execute a multiplication operation.
        """
        # get full instruction from memory
        instruction = self.memory[self.instruction_pointer : self.instruction_pointer+self.instruction_length]
        # get instruction parameters
        instruction_parameters = instruction[1:]
        # get operation argument addresses
        arg1_address = instruction_parameters[0]
        arg2_address = instruction_parameters[1]
        target_address = instruction_parameters[2]
        # get operation arguments
        arg1 = self.memory[arg1_address]
        arg2 = self.memory[arg2_address]
        # perform operation 
        sum = arg1 * arg2
        # store result
        self.memory[target_address] = sum
        # increment instruction pointer
        self.instruction_pointer += self.instruction_length