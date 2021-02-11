
# 16 General Purpose Registers 
NUM_REGISTERS = 16
# Each General Purpose Register is 1 Byte wide
REGISTER_SIZE = 1
# Special I Register is 2 Bytes wide
I_SIZE = 2
# Program Counter is 2 Bytes wide
PC_SIZE = 2


# each OP Code is 2 Bytes
OPERATION_SIZE = 2

class Cpu():
    def __init__(self, memory):
        self.memory = memory
        self.initialize()
        
        self.operations = {
            0x0000: self.execute_system_operations,
            0x1000: self.operation_JP,
            0x2000: self.operation_CALL,
            0x3000: self.operation_SE,
            0x4000: self.operation_SNE,
            0x5000: self.operation_SE,
            0x6000: self.operation_LD,
            0x7000: self.operation_ADD,
            0x8000: self.execute_logical_operations,
            0x9000: self.operation_OR,
            0xA000: self.operation_LD,
            0xB000: self.operation_JP,
            0xC000: self.operation_RND,
            0xD000: self.operation_DRW,
            0xE000: self.execute_skip_operations,
            0xF000: self.execute_load_operations
        }
        self.system_operations = {
            0x00E0: self.operation_CLS,
            0x00EE: self.operation_RET
        }
        self.logical_operations = {
            0x8001: self.operation_OR,
            0x8002: self.operation_AND,
            0x8003: self.operation_XOR,
            0x8004: self.operation_ADD,
            0x8005: self.operation_SUB,
            0x8006: self.operation_SHR,
            0x8007: self.operation_SUBN,
            0x800E: self.operation_SHL
        }
        self.skip_operations = {
            0xE09E: self.operation_SKP,
            0xE0A1: self.operation_SKNP
        }
        self.load_operations = {
            0xF007: self.operation_LD,
            0xF00A: self.operation_LD,
            0xF015: self.operation_LD,
            0xF018: self.operation_LD,
            0xF01E: self.operation_LD,
            0xF029: self.operation_LD,
            0xF033: self.operation_LD,
            0xF055: self.operation_LD,
            0xF065: self.operation_LD
        }

    def initialize(self):
        self.memory.clear()
        self.registers = {
            'v' : bytearray(NUM_REGISTERS),
            'i' : bytearray(I_SIZE),
            'pc' : self.memory.ROMOFFSET,
            'sp' : 0
        }
        self.delay_register = 0 
        self.sound_register = 0

    def process_operation(self):
        op_code = self.memory[self.registers['pc']:self.registers['pc']+OPERATION_SIZE]
        self.execute_operation(op_code)
        return op_code

    def process_program(self):
        terminate = False
        while not terminate:
            operation = self.process_operation()
            if self.PC > memory.MAX_MEMORY:
                terminate = True
            if operation == b'\x00\x00':
                terminate = True

    def execute_operation(self, op_code):
        combined = (op_code[0] << 8) + op_code[1]
        op = combined & 0xF000
        args = combined & 0x0FFF
        operation = self.operations[op]
        return operation(args, op_code)

    def execute_system_operations(self, args, op_code):
        operation = self.system_operations[op_code]
        return operation(args, op_code)
    
    def execute_logical_operations(self, args, op_code):
        key = op_code & 0xF00F
        operation = self.logical_operations[key]
        return operation(args, op_code)

    def execute_skip_operations(self, args, op_code):
        key = op_code & 0xF0FF
        operation = self.skip_operations[key]
        return operation(args, op_code)       

    def execute_load_operations(self, args, op_code):
        key = op_code & 0xF0FF
        operation = self.load_operations[key]
        return operation(args, op_code)

    def operation_CLS(self, args, op_code):
        #
        self.registers['pc'] += OPERATION_SIZE

    def operation_RET(self, args, op_code):
        #
        self.registers['pc'] += OPERATION_SIZE

    def operation_SYS(self, args, op_code):
        # addr
        self.registers['pc'] += OPERATION_SIZE

    def operation_JP(self, args, op_code):
        addr = args
        self.registers['pc'] = addr

    def operation_CALL(self, args, op_code):
        # addr
        self.registers['pc'] += OPERATION_SIZE

    def operation_SE(self, args, op_code):
        # Vx, byte
        self.registers['pc'] += OPERATION_SIZE

    def operation_SNE(self, args, op_code):
        # Vx, byte
        self.registers['pc'] += OPERATION_SIZE

    def operation_SE(self, args, op_code):
        # Vx, Vy
        self.registers['pc'] += OPERATION_SIZE

    def operation_LD(self, args, op_code):
        # Vx, byte
        self.registers['pc'] += OPERATION_SIZE

    def operation_ADD(self, args, op_code):
        # Vx, byte
        self.registers['pc'] += OPERATION_SIZE

    def operation_LD(self, args, op_code):
        # Vx, Vy
        self.registers['pc'] += OPERATION_SIZE

    def operation_OR(self, args, op_code):
        # Vx, Vy
        self.registers['pc'] += OPERATION_SIZE

    def operation_AND(self, args, op_code):
        # Vx, Vy
        self.registers['pc'] += OPERATION_SIZE

    def operation_XOR(self, args, op_code):
        # Vx, Vy
        self.registers['pc'] += OPERATION_SIZE

    def operation_ADD(self, args, op_code):
        # Vx, Vy
        self.registers['pc'] += OPERATION_SIZE

    def operation_SUB(self, args, op_code):
        # Vx, Vy
        self.registers['pc'] += OPERATION_SIZE

    def operation_SHR(self, args, op_code):
        # Vx {, Vy}
        self.registers['pc'] += OPERATION_SIZE

    def operation_SUBN(self, args, op_code):
        # Vx, Vy
        self.registers['pc'] += OPERATION_SIZE

    def operation_SHL(self, args, op_code):
        # Vx {, Vy}
        self.registers['pc'] += OPERATION_SIZE

    def operation_SNE(self, args, op_code):
        # Vx, Vy
        self.registers['pc'] += OPERATION_SIZE

    def operation_LD(self, args, op_code):
        # I, addr
        self.registers['pc'] += OPERATION_SIZE

    def operation_JP2(self, args, op_code):
        # V0, addr
        self.registers['pc'] += OPERATION_SIZE

    def operation_RND(self, args, op_code):
        # Vx, byte
        self.registers['pc'] += OPERATION_SIZE

    def operation_DRW(self, args, op_code):
        # Vx, Vy, nibble
        self.registers['pc'] += OPERATION_SIZE

    def operation_SKP(self, args, op_code):
        # Vx
        self.registers['pc'] += OPERATION_SIZE

    def operation_SKNP(self, args, op_code):
        # Vx
        self.registers['pc'] += OPERATION_SIZE

    def operation_LD(self, args, op_code):
        # Vx, DT
        self.registers['pc'] += OPERATION_SIZE

    def operation_LD(self, args, op_code):
        # Vx, K
        self.registers['pc'] += OPERATION_SIZE

    def operation_LD(self, args, op_code):
        # DT, Vx
        self.registers['pc'] += OPERATION_SIZE

    def operation_LD(self, args, op_code):
        # ST, Vx
        self.registers['pc'] += OPERATION_SIZE

    def operation_ADD(self, args, op_code):
        # I, Vx
        self.registers['pc'] += OPERATION_SIZE

    def operation_LD(self, args, op_code):
        # F, Vx
        self.registers['pc'] += OPERATION_SIZE

    def operation_LD(self, args, op_code):
        # B, Vx
        self.registers['pc'] += OPERATION_SIZE

    def operation_LD(self, args, op_code):
        # [I], Vx
        self.registers['pc'] += OPERATION_SIZE

    def operation_LD(self, args, op_code):
        # Vx, [I]
        self.registers['pc'] += OPERATION_SIZE