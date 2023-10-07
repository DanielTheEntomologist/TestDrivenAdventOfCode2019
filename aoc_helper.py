def read_lines(file):
    with open(file,mode="r") as file:
        lines = file.readlines()
    lines = [line.strip("\n") for line in lines]
    return lines

def read_integers(file):
    lines = read_lines(file)
    integers = [int(line) for line in lines]
    return integers