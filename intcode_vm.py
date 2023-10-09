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
        self.position = 0
        self.opcode = None
        self.opcode_length = 4
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
        self.opcode = self.memory[self.position]

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
        pos_arg1 = self.memory[self.position + 1]
        pos_arg2 = self.memory[self.position + 2]
        pos_target = self.memory[self.position + 3]
        arg1 = self.memory[pos_arg1]
        arg2 = self.memory[pos_arg2]
        self.memory[pos_target] = arg1 + arg2
        self.position += self.opcode_length

    def multiply(self):
        """
        Execute a multiplication operation.
        """
        pos_arg1 = self.memory[self.position + 1]
        pos_arg2 = self.memory[self.position + 2]
        pos_target = self.memory[self.position + 3]
        arg1 = self.memory[pos_arg1]
        arg2 = self.memory[pos_arg2]
        self.memory[pos_target] = arg1 * arg2
        self.position += self.opcode_length