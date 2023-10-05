import pytest

import day_2019_01 as d

# I gather the tests in test Class for easier handling. 
class Test_2019_01:
    def test_fuel_required_to_launch(self):

        # examples provided in the puzzles are a 1 step from being turned into tests which is great :-) 
        assert d.fuel_required_to_launch(1969)==654
        assert d.fuel_required_to_launch(100756)==33583
        # I implement wrong rounding and only later catch this since default test did not detect this
        assert d.fuel_required_to_launch(11)==1

    def test_edge_cases(self):

        # I decide that negative fuel does not make sense so a component will require at minimum 0 fuel to launch
        assert d.fuel_required_to_launch(3)==0
        

    def test_negative_mass(self):

        # I decide that negative mass should require 0 fuel to launch
        assert d.fuel_required_to_launch(-30)==0

class Test_2019_01_01:
    def test_total_fuel_required(self):
        module_masses = [1969,100756]

        assert (654+33583) == d.total_fuel_required(module_masses)
        
class Test_2019_01_02:
    def test_fuel_required_to_launch_exponential(self):
        assert d.fuel_required_to_launch_exponential(1969)==966
        assert d.fuel_required_to_launch_exponential(100756)==50346
    
    def test_total_fuel_required_exponential(self):
        module_masses = [1969,100756]

        assert d.total_fuel_required_exponential(module_masses)==966+50346
