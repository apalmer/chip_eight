import os

from chip_eight import Computer

class TestComputer:

    @staticmethod
    def test_execute_program():
        sut = Computer()
        sut.initialize()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        rom = dir_path + "/../roms/IBM"
        rom_data = open(rom,"rb").read()
        sut.load_rom(rom_data)

        #sut.execute_progam()
