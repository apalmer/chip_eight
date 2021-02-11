import chip_eight
 
class TestCpu:

    @staticmethod
    def test_operation_JP():
        expected = 600

        program = bytearray(b'\x12\x58')
        memory = chip_eight.Memory()
        
        sut = chip_eight.Cpu(memory)
        sut.initialize()
        memory.load_rom(program)
        
        actual = sut.process_operation()
        
        assert sut.registers['pc'] == expected