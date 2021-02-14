from chip_eight import Computer

__computer = Computer()

def boot():
    __computer.initialize()

def load(rom):
    rom_data = open(rom,"rb").read()
    __computer.load_rom(rom_data)

def run():
    __computer.execute_progam()
