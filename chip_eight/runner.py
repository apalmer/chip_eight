from chip_eight import Computer

__computer = Computer()

def boot():
    __computer.initialize()

def load(rom):
    romData = open(rom,"rb").read()
    __computer.load_rom(romData)

def run():
    __computer.process_program()
