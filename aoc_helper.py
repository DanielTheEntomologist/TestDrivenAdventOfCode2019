def read_lines(file):
    with open(file,mode="r") as file:
        lines = file.readlines()
    lines = [line.strip("\n") for line in lines]
    return lines