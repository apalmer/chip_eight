from chip_eight.core import Machine

__machine = Machine()

def boot():
    __machine.initialize()

def load(rom):
    romData = open(rom,"rb").read()
    __machine.loadRom(romData)

def run():
    __machine.process_operation()