import os
import sys
# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
print(sys.path)

import aoc_helper.aoc_helper as hlp

class Wire:
    vectors = {"R":(1,0),"L":(-1,0),"U":(0,1),"D":(0,-1)}
    def __init__(self,sections=None):
        self.wire = [(0,0)]
        self.wire_sections = []
        if sections is not None:
            for section in sections:
                self.add_wire_section(section)


    def add_wire_section(self,section):
        
        self.wire_sections.append(section)

        direction = section[0]
        length = int(section[1:])

        vector = Wire.vectors[direction]
        for i in range(length):
            endpoint = self.wire[-1]
            next_endpoint = (endpoint[0]+vector[0],endpoint[1]+vector[1])
            self.wire.append(next_endpoint)




def find_points_of_intersection(wire1,wire2):
    wire1 = set(wire1)
    wire2 = set(wire2)
    intersections = wire1.intersection(wire2)

    return list(intersections)

def distance_to_closest_intersection(wire1,wire2):
    
    intersections = find_points_of_intersection(wire1,wire2)
    # remove tuple (0,0) from intersections
    intersections = [ point for point in intersections if point != (0,0)]

    distances = [ abs(point[0])+abs(point[1]) for point in intersections]
    return min(distances)
    


if __name__ == "__main__":

    file = "inputs/2019_03_a.txt"
    input = hlp.read_lines(file)
    wire1 = Wire(input[0].split(","))
    wire2 = Wire(input[1].split(","))
    # wire1 = Wire(wire1_sections)
    # wire2 = Wire(wire2_sections)

    answer = distance_to_closest_intersection(wire1.wire,wire2.wire)
    print("Answer to part 1 of Day 1 is: ", answer)

    # answer = fuel_required_to_launch_ship_exponential(input)
    # print("Answer to part 2 of Day 1 is: ", answer)