import day_2019_03 as d


class TestWire:
    def test_wire(self):
        wire = d.Wire()
        assert wire.wire == [(0,0)]
        
    def test_add_wire_section(self):
        wire = d.Wire()
        section = "R4"
        expected_wire = [(0,0),(1,0),(2,0),(3,0),(4,0)]
        
        wire.add_wire_section(section)

        print(wire.wire,expected_wire)
        assert len(wire.wire)==len(expected_wire)
        assert wire.wire == expected_wire

    def test_init_with_sections(self):
        wire = d.Wire(["R2","U3"])
        expected_wire = [(0,0),(1,0),(2,0),(2,1),(2,2),(2,3)]
        assert wire.wire == expected_wire
    





# def test_add_wire_section():
#     wire = [(0,0)]
#     section = "R8"
#     expected_wire = [(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0)]
#     # expected_wire = [ np.array(point) for point in expected_wire]
    
#     extended_wire = d.add_wire_section(wire,section)

#     print(extended_wire,expected_wire)
#     assert len(extended_wire)==len(expected_wire)
#     assert tuple(extended_wire) == tuple(expected_wire)



def test_find_points_of_intersection():
    wire1 = [(0,0),(1,1),(2,2)]
    wire2 = [(0,0),(1,2),(2,2)]
    assert tuple(d.find_points_of_intersection(wire1,wire2)) == ((0,0),(2,2))
            
def test_distance_to_closest_intersection():
    
    wire1 = d.Wire(["R75","D30","R83","U83","L12","D49","R71","U7","L72"])
    wire2 = d.Wire(["U62","R66","U55","R34","D71","R55","D58","R83"])
    assert d.distance_to_closest_intersection(wire1.wire,wire2.wire) == 159
    wire1 = d.Wire(["R98","U47","R26","D63","R33","U87","L62","D20","R33","U53","R51"])
    wire2 = d.Wire(["U98","R91","D20","R16","D67","R40","U7","R15","U6","R7"])

    assert d.distance_to_closest_intersection(wire1.wire,wire2.wire) == 135