#import pytest
#import pytest_mock
#from pytest_mock import mocker

import chip_eight
 
class TestCpu:

    @staticmethod
    def test_operation_JP_addr():
        expected = 600

        program = bytearray(b'\x12\x58')
        memory = chip_eight.Memory()
        
        sut = chip_eight.Cpu(memory, None)
        sut.initialize()
        memory.load_rom(program)
        
        sut.process_operation()
        
        assert sut.registers['pc'] == expected
        
    @staticmethod
    def test_operation_JP_V0_addr():
        expected = 623

        program = bytearray(b'\xB2\x58')
        memory = chip_eight.Memory()
        
        sut = chip_eight.Cpu(memory, None)
        sut.initialize()
        memory.load_rom(program)
        sut.registers['v'][0] = 23
        
        sut.process_operation()

        assert sut.registers['pc'] == expected
     
    @staticmethod
    def test_operation_XOR_Vx_Vy():

        program = bytearray(b'\x80\x13')
        memory = chip_eight.Memory()
        
        sut = chip_eight.Cpu(memory, None)
        sut.initialize()
        memory.load_rom(program)
        sut.registers['v'][0] = 0b11111111
        sut.registers['v'][1] = 0b11111111
        
        sut.process_operation()

        assert sut.registers['v'][0x0] == 0
    
    @staticmethod
    def test_operation_LD_I_addr():
        expected = 600

        program = bytearray(b'\xA2\x58')
        memory = chip_eight.Memory()
        
        sut = chip_eight.Cpu(memory, None)
        sut.initialize()
        memory.load_rom(program)
        
        sut.process_operation()
        
        assert sut.registers['i'] == expected
    
    @staticmethod
    def test_operation_RND_Vx_byte():

        program = bytearray(b'\xCA\x4F')
        memory = chip_eight.Memory()
        
        sut = chip_eight.Cpu(memory, None)
        sut.initialize()
        memory.load_rom(program)
        sut.registers['v'][10] == 0
        
        sut.process_operation()

        assert sut.registers['v'][0xA] <= 79
        
    @staticmethod
    def test_operation_SE_Vx_byte():
        expected = 516

        program = bytearray(b'\x3A\x12')
        memory = chip_eight.Memory()
        
        sut = chip_eight.Cpu(memory, None)
        sut.initialize()
        memory.load_rom(program)
        sut.registers['v'][10] = 18
        
        sut.process_operation()

        assert sut.registers['pc'] == 516

    @staticmethod
    def test_operation_DRW_Vx_Vy_nibble(mocker):
        
        program = bytearray(b'\x12\x08\xf0\x90\x90\x90\xf0\x00\xD0\x15')
        memory = chip_eight.Memory()
        screen = chip_eight.Screen()
        mocker.patch.object(screen, 'draw_sprite')
        screen.draw_sprite.return_value = 0

        sut = chip_eight.Cpu(memory, screen)
        sut.initialize()
        memory.load_rom(program)
        sut.registers['v'][0] = 1
        sut.registers['v'][1] = 1
        sut.registers['i'] = memory.ROM_OFFSET + 2
        sut.registers['pc'] = memory.ROM_OFFSET + 8 
        
        sut.process_operation()

        screen.draw_sprite.assert_called_with(1,1,bytearray(b'\xf0\x90\x90\x90\xf0'))
        assert sut.registers['v'][0xF] == 0

    @staticmethod
    def test_operation_CLS(mocker):
        
        program = bytearray(b'\x00\xE0')
        memory = chip_eight.Memory()
        screen = chip_eight.Screen()
        mocker.patch.object(screen, 'clear_screen')

        sut = chip_eight.Cpu(memory, screen)
        sut.initialize()
        memory.load_rom(program)
        
        sut.process_operation()

        screen.clear_screen.assert_called_with()

    @staticmethod
    def test_operation_LD_Vx_byte():
        expected = 0xAB

        program = bytearray(b'\x69\xAB')
        memory = chip_eight.Memory()
        
        sut = chip_eight.Cpu(memory, None)
        sut.initialize()
        memory.load_rom(program)
        
        sut.process_operation()

        assert sut.registers['v'][0x9] == expected

    
    @staticmethod
    def test_operation_ADD_Vx_byte():
        expected = 0x7f + 0x80

        program = bytearray(b'\x78\x80')
        memory = chip_eight.Memory()
        
        sut = chip_eight.Cpu(memory, None)
        sut.initialize()
        memory.load_rom(program)
        sut.registers['v'][0x8] = 0x7f
        sut.process_operation()

        assert sut.registers['v'][0x8] == expected

    @staticmethod
    def test_operation_LD_Vx_Vy():
        expected = 0xAB

        program = bytearray(b'\x83\x40')
        memory = chip_eight.Memory()
        
        sut = chip_eight.Cpu(memory, None)
        sut.initialize()
        memory.load_rom(program)
        sut.registers['v'][0x3] = 0x00
        sut.registers['v'][0x4] = expected
        
        sut.process_operation()

        assert sut.registers['v'][0x3] == expected
        
    @staticmethod
    def test_operation_CALL_addr():

        program = bytearray(b'\x20\x10')
        memory = chip_eight.Memory()
        
        sut = chip_eight.Cpu(memory, None)
        sut.initialize()
        memory.load_rom(program)
        
        initial_pc = sut.registers['pc']

        sut.process_operation()

        assert sut.registers['pc'] ==  0x0010
        assert sut.registers['sp'] == memory.STACK_START + 0x02 

        high_byte = memory[sut.registers['sp']]
        low_byte = memory[sut.registers['sp'] + 1]
        addr = (high_byte << 8) + low_byte
        assert addr == initial_pc + 0x02

    @staticmethod
    def test_operation_RET():

        program = bytearray(b'\x00\x00')
        memory = chip_eight.Memory()
        
        sut = chip_eight.Cpu(memory, None)
        sut.initialize()
        memory.load_rom(program)
    
        sut.registers['pc'] = 0x0010
        #set the return op_code at the appriate space in memory
        memory[0x0010] = 0x00
        memory[0x0011] = 0xEE
        sut.registers['sp'] = memory.STACK_START + 0x02
        high_byte = (memory.ROM_OFFSET & 0xFF00) >> 8
        low_byte = memory.ROM_OFFSET & 0x00FF
        memory[sut.registers['sp']] = high_byte
        memory[sut.registers['sp'] + 1] = low_byte

        sut.process_operation()

        assert sut.registers['pc'] == memory.ROM_OFFSET
        assert sut.registers['sp'] == memory.STACK_START