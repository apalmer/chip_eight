import chip_eight

class TestMachine:
    def test_load(capsys):
        ordered = bytearray([i for i in range(0x00,0x100,0x01)])
        sut = chip_eight.Machine()
        sut.initialize()
        sut.loadRom(ordered)        
        actual = sut.process_operation()
        assert actual == ordered[0:2]