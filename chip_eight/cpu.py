import random
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame

# 16 General Purpose Registers 
NUM_REGISTERS = 16
# Each General Purpose Register is 1 Byte wide
REGISTER_SIZE = 1
# Special I Register is 2 Bytes wide
I_SIZE = 2
# Program Counter is 2 Bytes wide
PC_SIZE = 2
# Stack containts array of 16 2 Byte wide elements
SP_SIZE = 2

# each OP Code is 2 Bytes
OPERATION_SIZE = 2

class Cpu():
    def __init__(self, memory, screen, clock_speed=60):
        self.memory = memory
        self.screen = screen
        self.clock_speed = clock_speed
        self.initialize()
        
        self.operations = {
            0x0000: self.execute_system_operations,
            0x1000: self.operation_JP_addr,
            0x2000: self.operation_CALL_addr,
            0x3000: self.operation_SE_Vx_byte,
            0x4000: self.operation_SNE,
            0x5000: self.operation_SE,
            0x6000: self.operation_LD_Vx_byte,
            0x7000: self.operation_ADD_Vx_byte,
            0x8000: self.execute_logical_operations,
            0x9000: self.operation_OR,
            0xA000: self.operation_LD_I_addr,
            0xB000: self.operation_JP_V0_addr,
            0xC000: self.operation_RND_Vx_byte,
            0xD000: self.operation_DRW_Vx_Vy_nibble,
            0xE000: self.execute_skip_operations,
            0xF000: self.execute_load_operations
        }
        self.system_operations = {
            0x00E0: self.operation_CLS,
            0x00EE: self.operation_RET
        }
        self.logical_operations = {
            0x8000: self.operation_LD_Vx_Vy,
            0x8001: self.operation_OR,
            0x8002: self.operation_AND,
            0x8003: self.operation_XOR_Vx_Vy,
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
            'i' : 0x0000,
            'pc' : self.memory.ROM_OFFSET,
            'sp' : self.memory.STACK_START
        }
        self.delay_register = 0 
        self.sound_register = 0

    def process_operation(self):
        op_code = self.memory[self.registers['pc']:self.registers['pc']+OPERATION_SIZE]
        self.registers['pc'] += OPERATION_SIZE
        self.execute_operation(op_code)
        return op_code

    def process_program(self):
        clock = pygame.time.Clock()
        terminate = False

        while not terminate:
            clock.tick(self.clock_speed)
            print(clock.get_fps())
            operation = self.process_operation()
            if self.registers['pc'] > self.memory.MAX_MEMORY:
                terminate = True
            if operation == b'\x00\x00':
                terminate = True

    def execute_operation(self, op_code):
        args = (op_code[0] << 8) + op_code[1]
        op = args & 0xF000
        operation = self.operations[op]
        return operation(args)

    def execute_system_operations(self, args):
        operation = self.system_operations[args]
        return operation(args)
    
    def execute_logical_operations(self, args):
        key = args & 0xF00F
        operation = self.logical_operations[key]
        return operation(args)

    def execute_skip_operations(self, args):
        key = args & 0xF0FF
        operation = self.skip_operations[key]
        return operation(args)       

    def execute_load_operations(self, args):
        key = args & 0xF0FF
        operation = self.load_operations[key]
        return operation(args)
 
    def operation_ADD_Vx_byte(self, args):
        """
        7xkk - ADD Vx, byte
        Set Vx = Vx + kk.

        Adds the value kk to the value of register Vx, then stores the result in Vx.
        """
        x = (args & 0x0F00) >> 8
        byte = args & 0x00FF 
        self.registers['v'][x] += byte 
        
    def operation_CALL_addr(self, args):
        """
        2nnn - CALL addr
        Call subroutine at nnn.

        The interpreter increments the stack pointer, then puts the current PC on the top of the stack. The PC is then set to nnn.
        """
        addr = args & 0x0FFF
        high_byte = (self.registers['pc'] & 0xFF00) >> 8
        low_byte = self.registers['pc'] & 0x00FF
        self.registers['sp'] += SP_SIZE
        self.memory[self.registers['sp']] = high_byte
        self.memory[self.registers['sp'] + 1] = low_byte
        self.registers['pc'] = addr

    def operation_CLS(self, args):
        """
        00E0 - CLS
        Clear the display.
        """
        self.screen.clear_screen()

    def operation_DRW_Vx_Vy_nibble(self, args):
        """
        Display n-byte sprite starting at memory location I at (Vx, Vy), set VF = collision.

        The interpreter reads n bytes from memory, starting at the address stored in I. These bytes are then displayed as sprites on screen at coordinates (Vx, Vy). Sprites are XORed onto the existing screen. If this causes any pixels to be erased, VF is set to 1, otherwise it is set to 0. If the sprite is positioned so part of it is outside the coordinates of the display, it wraps around to the opposite side of the screen. See instruction 8xy3 for more information on XOR, and section 2.4, Display, for more information on the Chip-8 screen and sprites.
        """
        x = (args & 0x0F00) >> 8
        y = (args & 0x00F0) >> 4
        nibble = args & 0x000F
        sprite_x = self.registers['v'][x]
        sprite_y = self.registers['v'][y]
        sprite_start_addr = self.registers['i']
        sprite_end_addr = sprite_start_addr + nibble
        sprite = self.memory[sprite_start_addr:sprite_end_addr]
        collision = self.screen.draw_sprite(sprite_x,sprite_y,sprite)
        if collision:
            self.registers['v'][0xF]=0x01

    def operation_JP_addr(self, args):
        """
        1nnn - JP addr
        Jump to location nnn.

        The interpreter sets the program counter to nnn.
        """
        addr = args & 0x0FFF
        self.registers['pc'] = addr

    def operation_JP_V0_addr(self, args):
        """
        Bnnn - JP V0, addr
        Jump to location nnn + V0.

        The program counter is set to nnn plus the value of V0.
        """
        addr = args & 0x0FFF
        self.registers['pc'] = addr + self.registers['v'][0x0]
 
    def operation_LD_I_addr(self, args):
        """
        Annn - LD I, addr
        Set I = nnn.

        The value of register I is set to nnn
        """
        addr = args & 0x0FFF
        self.registers['i'] = addr
     
    def operation_LD_Vx_byte(self, args):
        """
        6xkk - LD Vx, byte
        Set Vx = kk.

        The interpreter puts the value kk into register Vx.
        """
        x = (args & 0x0F00) >> 8
        byte = args & 0x00FF
        self.registers['v'][x] = byte

    def operation_LD_Vx_Vy(self, args):
        """
        8xy0 - LD Vx, Vy
        Set Vx = Vy.

        Stores the value of register Vy in register Vx.
        """
        x = (args & 0x0F00) >> 8
        y = (args & 0x00F0) >> 4
        self.registers['v'][x] = self.registers['v'][y]
    
    def operation_RET(self, args):
        """
        00EE - RET
        Return from a subroutine.

        The interpreter sets the program counter to the address at the top of the stack, then subtracts 1 from the stack pointer.
        """
        high_byte = self.memory[self.registers['sp']]
        low_byte = self.memory[self.registers['sp']+1]
        addr = (high_byte << 8) + low_byte
        self.registers['pc'] = addr
        self.registers['sp'] -= SP_SIZE

    def operation_RND_Vx_byte(self, args):
        """
        Cxkk - RND Vx, byte
        Set Vx = random byte AND kk.

        The interpreter generates a random number from 0 to 255, which is then ANDed with the value kk. The results are stored in Vx. See instruction 8xy2 for more information on AND.
        """
        x = (args & 0x0F00) >> 8
        byte = args & 0x0FF
        random_byte = random.randrange(0,256)
        self.registers['v'][x] = random_byte & byte

    def operation_SE_Vx_byte(self, args):
        """
        3xkk - SE Vx, byte
        Skip next instruction if Vx = kk.

        The interpreter compares register Vx to kk, and if they are equal, increments the program counter by 2.
        """
        x = (args & 0x0F00) >> 8 
        byte = args & 0x00FF
        if(self.registers['v'][x] == byte):
            self.registers['pc'] += OPERATION_SIZE

    def operation_XOR_Vx_Vy(self, args):
        """
        8xy3 - XOR Vx, Vy
        Set Vx = Vx XOR Vy.

        Performs a bitwise exclusive OR on the values of Vx and Vy, then stores the result in Vx. An exclusive OR compares the corrseponding bits from two values, and if the bits are not both the same, then the corresponding bit in the result is set to 1. Otherwise, it is 0.
        """
        x = (args & 0x0F00) >> 8
        y = (args & 0x00F0) >> 4
        self.registers['v'][x] ^= self.registers['v'][y]

    # UNFINISHED #################################################################

    def operation_SYS(self, args):
        # addr
        pass

    def operation_SNE(self, args):
        # Vx, byte
        pass

    def operation_SE(self, args):
        # Vx, Vy
        pass

    def operation_OR(self, args):
        # Vx, Vy
        pass

    def operation_AND(self, args):
        # Vx, Vy
        pass

    def operation_ADD(self, args):
        # Vx, Vy
        pass

    def operation_SUB(self, args):
        # Vx, Vy
        pass

    def operation_SHR(self, args):
        # Vx {, Vy}
        pass

    def operation_SUBN(self, args):
        # Vx, Vy
        pass

    def operation_SHL(self, args):
        # Vx {, Vy}
        pass

    def operation_SNE(self, args):
        # Vx, Vy
        pass
        
    def operation_SKP(self, args):
        # Vx
        pass

    def operation_SKNP(self, args):
        # Vx
        pass

    def operation_LD(self, args):
        # Vx, DT
        pass

    def operation_LD(self, args):
        # Vx, K
        pass

    def operation_LD(self, args):
        # DT, Vx
        pass

    def operation_LD(self, args):
        # ST, Vx
        pass

    def operation_ADD(self, args):
        # I, Vx
        pass

    def operation_LD(self, args):
        # F, Vx
        pass

    def operation_LD(self, args):
        # B, Vx
        pass

    def operation_LD(self, args):
        # [I], Vx
        pass

    def operation_LD(self, args):
        # Vx, [I]
        pass