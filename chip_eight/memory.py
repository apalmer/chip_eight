class Memory(bytearray):
    def __init__(self):
        # 4096 Bytes of Main Memory
        self.MAX_MEMORY = 4096
        # ROMS are loaded into memory starting at address 512
        self.ROM_OFFSET = 512
        # Start of 16 Bytes of memory used as a stack for procedure calls
        self.STACK_START = 52

        bytearray.__init__(self, self.MAX_MEMORY)

    def load_rom(self, rom):
        for index, byte in enumerate(rom):
            self[self.ROM_OFFSET + index] = byte

    def clear(self):
        for index in range(0,len(self)):
            self[index] = 0x00
