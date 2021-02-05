# 4096 Bytes of Main Memory
MAX_MEMORY = 4096 
# 16 General Purpose Registers 
NUM_REGISTERS = 16
# Each General Purpose Register is 1 Byte wide
REGISTER_SIZE = 1
# Special I Register is 2 Bytes wide
I_SIZE = 2
# Program Counter is 2 Bytes wide
PC_SIZE = 2

# ROMS are loaded into memory starting at address 512
ROMOFFSET = 512
# each OP Code is 2 Bytes
OPERATION_SIZE = 2

class Machine():
    def __init__(self):
        self.memory = bytearray(MAX_MEMORY)
        self.V = bytearray(NUM_REGISTERS)
        self.I = bytearray(I_SIZE)
        self.PC = ROMOFFSET
        self.SP = 0
        self.delay_register = 0 
        self.sound_register = 0

    def initialize(self):
        self.__init__()

    def loadRom(self, rom):
        for index, byte in enumerate(rom):
            self.memory[ROMOFFSET + index] = byte

    def execute_operation(self, operation):
        print(operation)

    def process_operation(self):
        next_pc = self.PC + OPERATION_SIZE
        op_code = self.memory[self.PC:next_pc]
        offset = self.execute_operation(op_code)
        if offset:
            next_pc = self.PC + offset
        self.PC = next_pc
        return op_code

    def process_program(self):
        terminate = False
        while not terminate:
            operation = self.process_operation()
            if self.PC > MAX_MEMORY:
                terminate = True
            if operation == b'\x00\x00':
                terminate = True