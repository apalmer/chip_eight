import chip_eight

import sys
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

if(len(sys.argv) > 1):
    rom = dir_path + "/../roms/" + sys.argv[1]
else:
    rom = dir_path + "/../roms/BLINKY"

chip_eight.boot()
chip_eight.load(rom)
chip_eight.run()