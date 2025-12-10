from Util.constants import Constants
from Components.Util import get_selector

class Memory:
    def __init__(self):
        mem_slots = 2 ** Constants.MEMORY_INSTRUCTION_SIZE
        self.memory_registers = [[0] * Constants.IMMEDIATE_INSTRUCTION_SIZE] * mem_slots

    def read(self, cfg_bits):
        return self.memory_registers[get_selector(cfg_bits)]

    def write(self, immediate, cfg_bits):
        self.memory_registers[get_selector(cfg_bits)] = immediate
