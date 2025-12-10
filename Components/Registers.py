from Util.constants import Constants
from Components.Util import get_selector

class Registers:
    def __init__(self):
        reg_slots = 2 ** Constants.REGISTER_INSTRUCTION_SIZE
        self.registers = [[0] * Constants.IMMEDIATE_INSTRUCTION_SIZE] * reg_slots
        self.r3 = [0] * Constants.IMMEDIATE_INSTRUCTION_SIZE

    def read(self, cfg_bits=None):
        if cfg_bits:
            return self.registers[get_selector(cfg_bits)]
        return self.r3

    def write(self, immediate, cfg_bits=None):
        if cfg_bits:
            self.registers[get_selector(cfg_bits)] = immediate
        else:
            self.r3 = immediate