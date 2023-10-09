"""Intcode VM for Advent of Code 2019

This intcode machine may be very similar to the many other
on the internet because it is done with heavy suggestion from
github copilot. Advent of Code solutions are published in countless
GitHub repos, so Copilot is heaviliy trained on AoC solutions.
At the same time it speeds up my work significantly,
so I am willing to accept this not being my 100% original bespoke code.
"""

class IntCodeVM:
    def __init__(self,program:list[int]):
        self.memory = program

        
        self.position = 0
        
        self.opcode = None
        self.opcode_length = 4
        self.state = "INIT" #init -> running -> halted or error
        
    def run(self):
        self.state = "RUNNING"
        while self.state == "RUNNING":
            self.step()
        
    
    def step(self):
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
        self.state = "HALTED"
    
    def add(self):
        pos_arg1 = self.memory[self.position+1]
        pos_arg2 = self.memory[self.position+2]
        pos_target = self.memory[self.position+3]
        arg1 = self.memory[pos_arg1]
        arg2 = self.memory[pos_arg2]
        self.memory[pos_target] = arg1 + arg2
        self.position += self.opcode_length
    
    def multiply(self):
        pos_arg1 = self.memory[self.position+1]
        pos_arg2 = self.memory[self.position+2]
        pos_target = self.memory[self.position+3]
        arg1 = self.memory[pos_arg1]
        arg2 = self.memory[pos_arg2]
        self.memory[pos_target] = arg1 * arg2
        self.position += self.opcode_length