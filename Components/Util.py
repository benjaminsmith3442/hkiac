from Util.constants import Constants

def get_selector(input_bits):
    selector = 0
    for i, bit in enumerate(input_bits):
        if bit: selector += 2 ** i
    return selector

def _instruction_section(instruction, _i):
    index_0 = 0 if _i == 0 else Constants.INSTRUCTION_WIDTHS[_i - 1] - 1
    index_1 = index_0 + Constants.INSTRUCTION_WIDTHS[_i]
    return instruction[index_0:index_1]

def get_instruction_opcode(instruction):
    return _instruction_section(instruction, 0)

def get_instruction_memory(instruction):
    return _instruction_section(instruction, 1)

def get_instruction_immediate(instruction):
    return _instruction_section(instruction, 2)

def get_instruction_register(instruction):
    return _instruction_section(instruction, 3)