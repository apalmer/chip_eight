
from chip_eight import Memory, Screen, Cpu

class Computer():

    def __init__(self, clock_speed=600):
        self.clock_speed = clock_speed
        self.memory = Memory()
        self.screen = Screen()
        self.cpu = Cpu(self.memory, self.screen, self.clock_speed)

    def initialize(self):
        self.cpu.initialize()
        self.screen.initialize()
    
    def load_rom(self, rom):
        self.memory.load_rom(rom)

    def execute_progam(self):
        self.cpu.process_program()