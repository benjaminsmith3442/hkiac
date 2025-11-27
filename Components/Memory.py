from Util.constants import Constants

class Memory:
    def __init__(self):
        mem_slots = 2 ** Constants.MEMORY_INSTRUCTION_SIZE
        self.mapped_mode = 0
        self.input = [0] * mem_slots
        self.input_index = 0
        self.memory_registers = [[0] * Constants.IMMEDIATE_INSTRUCTION_SIZE] * mem_slots
        self.output = [0] * Constants.IMMEDIATE_INSTRUCTION_SIZE

    def read(self, selector_map):
        self.input = selector_map[:]
        self.input_index = next((i for i, slot in enumerate(self.input) if slot == 1), 0)
        self.output = self.memory_registers[self.input_index]
        return self.output

    def store(self, selector_map, immediate):
        self.input = selector_map[:]
        self.input_index = next((i for i, slot in enumerate(self.input) if slot == 1), 0)
        self.memory_registers[self.input_index] = immediate
