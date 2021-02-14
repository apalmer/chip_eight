from chip_eight import Memory

class TestMemory:
   
    @staticmethod 
    def test_length_is_MAX_MEMORY():
        expected = 4096 

        sut = Memory()
        
        assert len(sut) == expected
    
    @staticmethod
    def test_is_iterable():
        sut = Memory()

        for cell in sut:
            assert cell == 0

    @staticmethod
    def test_is_indexable():
        value = 0xFF
        addr = 1024

        sut = Memory()
        sut[addr] = value

        assert sut[addr] == value
    
    @staticmethod
    def test_load():

        ordered = bytearray(range(0x00,0x100,0x01))

        sut = Memory()
        sut.load_rom(ordered)

        actual = sut[sut.ROM_OFFSET:sut.ROM_OFFSET+2]

        assert actual == ordered[0:2]

