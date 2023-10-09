def read_lines(file):
    with open(file,mode="r") as file:
        lines = file.readlines()
    lines = [line.strip("\n") for line in lines]
    return lines

def read_integers(file):
    lines = read_lines(file)
    integers = [int(line) for line in lines]
    return integers

def read_intcode_program(file,separator=","):
    lines = read_lines(file)
    integers = lines[0].split(separator)
    integers = [int(integer) for integer in integers]
    return integers