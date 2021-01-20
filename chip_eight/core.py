ROMOFFSET = 0x200
MAX_MEMORY = 0x1000
OPERATION_SIZE = 0x002

class Machine():
    def __init__(self):
        self.memory = bytearray(MAX_MEMORY)
        self.PC = ROMOFFSET

    def initialize(self):
        self.__init__()

    def loadRom(self, rom):
        for index, byte in enumerate(rom):
            self.memory[ROMOFFSET + index] = byte

    def execute_operation(self, operation):
        print(operation)

    def process_operation(self):
        next_pc = self.PC + OPERATION_SIZE
        operation = self.memory[self.PC:next_pc]
        self.execute_operation(operation)
        self.PC = next_pc
        return operation
