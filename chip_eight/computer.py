class Computer():

    def __init__(self):
        pass
    
    def initialize(self):
        pass
    
    def load_rom(self, rom):
        for index, byte in enumerate(rom):
            self.memory[ROMOFFSET + index] = byte

    def execute_program(self):
        pass