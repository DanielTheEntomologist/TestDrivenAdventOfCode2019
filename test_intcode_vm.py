import pytest

import intcode_vm as intcode

class TestIntcodeVM:
    def test_run(self):
        vm = intcode.IntCodeVM([99])
        vm.run()
        assert vm.state == "HALTED"

    def test_invalid_opcode(self):
        vm = intcode.IntCodeVM([-12331])
        with pytest.raises(ValueError):
            vm.step()    
        assert vm.state == "ERROR"

    def test_add(self):
        vm = intcode.IntCodeVM([1,0,0,0,99])
        vm.run()
        assert vm.memory == [2,0,0,0,99]
        vm = intcode.IntCodeVM([1,1,1,4,99,5,6,0,99])
        vm.run()
        assert vm.memory == [30,1,1,4,2,5,6,0,99]

    def test_multiply(self):
        vm = intcode.IntCodeVM([2,3,0,3,99])
        vm.run()
        assert vm.memory == [2,3,0,6,99]
        vm = intcode.IntCodeVM([2,4,4,5,99,0])
        vm.run()
        assert vm.memory == [2,4,4,5,99,9801]

    