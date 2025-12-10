import copy
import math
import os
import sys
import tkinter as tk
from copy import deepcopy

from PIL import ImageTk
from Util.AsmParser import Instructions
from Util.constants import Constants
from Components.Memory import Memory
from PIL import Image
import View.DrawTools as DrawTools
import View.SnapObjects as SnapObjects
from View.Palette import WHITE, GREEN, TEST_RED, LIGHT_BLUE, ORANGE, PURPLE, LIGHT_GREEN, TEAL, LIGHT_BROWN

class Layout:
    def __init__(self, canvas):
        self.canvas = canvas

    def draw_hkiac_panel(self, x, y):
        label = tk.Label(
            root,
            image=tk_img,
            borderwidth=0,
            highlightthickness=0,
            padx=0,
            pady=0
        )
        label.place(x=20, y=10)

    def draw_alu_panel(self, x, y):  # TODO segment the individual groupings into nested methods. Do the same elsewhere
        x_coord = x
        y_coord = y
        gate_x = x_coord + 1
        gate_y = y_coord + 12
        alu_input_x = x_coord + 1
        alu_input_y = y_coord + 1
        alu_output_x = x_coord + 7
        alu_output_y = y_coord + 23
        carry_x = x_coord + 12
        carry_y = y_coord + 9

        draw.panel(x_coord, y_coord, x_coord + 14, y_coord + 24, SnapObjects.ALU_PANEL)

        register_a = [0, 0, 0, 0, 1]
        register_b = [0, 1, 1, 1, 0]

        alu_inputs = [register_a, register_b]

        for i, alu_input in enumerate(alu_inputs):
            for j, bit in enumerate(alu_input):
                switch_value = bit == 1
                switch_style = SnapObjects.REGISTER_AB_SWITCH if (j == len(alu_input) - 1) else SnapObjects.SWITCH
                draw.switch(alu_input_x + j, alu_input_y + i, switch_style, switch_value)

        register_c = [0, 1, 1, 1, 0]
        for i, bit in enumerate(register_c):
            switch_value = bit == 1
            switch_style = SnapObjects.REGISTER_C_SWITCH if i == 0 else SnapObjects.SWITCH
            draw.switch(alu_output_x + i, alu_output_y, switch_style, switch_value)

        carry = [1, 0]
        for i, bit in enumerate(carry):
            switch_value = bit == 1
            switch_style = SnapObjects.CARRY_SWITCH if i == 0 else SnapObjects.SWITCH
            draw.switch(carry_x + i, carry_y, switch_style, switch_value)

        _carry_in = {
            0: {'x': gate_x + 4, 'y': gate_y + 2},
            1: {'x': gate_x + 4, 'y': gate_y - 2},
            2: {'x': gate_x + 11, 'y': gate_y - 2},
            3: {'x': gate_x + 11, 'y': gate_y + 2}
        }
        _carry_out = {
            0: {'x': gate_x + 10, 'y': gate_y + 6},
            1: {'x': gate_x + 10, 'y': gate_y + 8},
            2: {'x': gate_x + 12, 'y': gate_y + 8},
            3: {'x': gate_x + 12, 'y': gate_y - 2}
        }
        _register_2 = {
            0: {'x': gate_x + 4, 'y': gate_y + 9},
            1: {'x': gate_x + 4, 'y': gate_y + 11},
            2: {'x': gate_x + 5, 'y': gate_y + 11},
        }

        _zero = {
            0: {'x': gate_x + 3, 'y': gate_y + 9},
            1: {'x': gate_x + 3, 'y': gate_y + 11},
            2: {'x': gate_x + 2, 'y': gate_y + 11},
        }

        # _not_input = {
        #     0: {'x': gate_x + 4, 'y': gate_y + 9},
        #     1: {'x': gate_x + 4, 'y': gate_y + 9},
        #     2: {'x': gate_x + 4, 'y': gate_y + 9}
        # }
        # _not_output = {
        #     0: {'x': gate_x + 4, 'y': gate_y + 9},
        #     1: {'x': gate_x + 4, 'y': gate_y + 9},
        #     2: {'x': gate_x + 4, 'y': gate_y + 9}
        # }
        # _not_bypassed = {
        #     0: {'x': gate_x + 4, 'y': gate_y + 9},
        #     1: {'x': gate_x + 4, 'y': gate_y + 9},
        #     2: {'x': gate_x + 4, 'y': gate_y + 9}
        # }
        _a = {
            0: {'x': gate_x, 'y': gate_y + 2},
            1: {'x': gate_x, 'y': gate_y - 4},
            2: {'x': gate_x + 6, 'y': gate_y - 4},
            3: {'x': gate_x + 6, 'y': gate_y - 1}
        }
        _b = {
            0: {'x': gate_x + 3, 'y': gate_y + 2},
            1: {'x': gate_x + 3, 'y': gate_y - 3},
            2: {'x': gate_x + 8, 'y': gate_y - 3},
            3: {'x': gate_x + 8, 'y': gate_y - 11},
            4: {'x': gate_x + 5, 'y': gate_y - 11},
            5: {'x': gate_x + 8, 'y': gate_y - 11},
            6: {'x': gate_x + 8, 'y': gate_y - 3},
            7: {'x': gate_x + 9, 'y': gate_y - 3},
            8: {'x': gate_x + 9, 'y': gate_y - 1}
        }

        draw.draw_free_lines(SnapObjects.INPUT_A_FREELINE, _a)
        draw.draw_free_lines(SnapObjects.INPUT_B_FREELINE, _b)
        draw.draw_free_lines(SnapObjects.CARRY_IN_FREELINE, _carry_in)
        draw.draw_free_lines(SnapObjects.CARRY_IN_FREELINE, _carry_out)
        draw.draw_free_lines(SnapObjects.REGISTER_2_FREELINE, _register_2)
        draw.draw_free_lines(SnapObjects.ZERO_FREELINE, _zero)

        gate_row = 3
        draw.logic_gate(gate_x + 3, gate_y - 8, SnapObjects.LOGIC_GATE_NOT, [0, 1])
        draw.logic_gate(gate_x + 6, gate_y + (0 * gate_row), SnapObjects.LOGIC_GATE_XOR, [1, 1, 1])
        draw.logic_gate(gate_x + 8, gate_y + (1 * gate_row), SnapObjects.LOGIC_GATE_XOR, [1, 1, 1])
        draw.logic_gate(gate_x + 4, gate_y + (1 * gate_row), SnapObjects.LOGIC_GATE_AND, [1, 1, 1])
        draw.logic_gate(gate_x + 0, gate_y + (1 * gate_row), SnapObjects.LOGIC_GATE_AND, [1, 1, 1])
        draw.logic_gate(gate_x + 2, gate_y + (2 * gate_row), SnapObjects.LOGIC_GATE_OR, [1, 1, 1])

    def draw_memory_panel(x, y):  # TODO this is very static. Need it to be malleable, rubbery, maybe flubbery
        x_coord = x
        y_coord = y

        draw.panel(x_coord, y_coord, x_coord + 12, y_coord + 6, SnapObjects.MEMORY_PANEL)

        memory.store([0, 1], [0, 0, 0, 1, 0])

        memory_indexes = [
            memory.read([0, 0]),
            memory.read([0, 1]),
            memory.read([1, 0]),
            memory.read([1, 1])
        ]

        draw.switch_mapper_board(x_coord, y_coord + 1, [0, 1], SnapObjects.MEMORY_SWITCH_MAPPER)

        draw.terminal_text(x_coord + 5, y_coord + 2, "[M0]", TEAL, bump_y=-5)
        draw.terminal_text(x_coord + 5, y_coord + 3, "[M1]", TEAL, bump_y=-5)
        draw.terminal_text(x_coord + 5, y_coord + 4, "[M2]", TEAL, bump_y=-5)
        draw.terminal_text(x_coord + 5, y_coord + 5, "[M3]", LIGHT_BLUE, bump_y=-5)

        for i, memory_index in enumerate(memory_indexes):
            sc = copy.deepcopy(SnapObjects.INPUT_SWITCH) if i == len(memory_indexes) - 1 else copy.deepcopy(
                SnapObjects.MEMORY_SWITCH)
            for j, bit in enumerate(memory_index):
                switch_value = str(bit) == "1"
                draw.switch(x_coord + 7 + j, y_coord + 1 + i, sc, switch_value)

    def draw_register_panel(x, y):
        x_coord = x + 1
        y_coord = y

        draw.panel(x, y, x + 12, y + 5, SnapObjects.REGISTER_PANEL)
        draw.switch_mapper_board(x_coord, y_coord + 1, [0], SnapObjects.REGISTER_SWITCH_MAPPER)
        draw.terminal_text(x_coord + 4, y_coord + 2, '[R0]', LIGHT_BROWN,
                           bump_y=-4)  # TODO Im betting this can go warm n snugly into the mapper board class
        draw.terminal_text(x_coord + 4, y_coord + 3, '[R1]', LIGHT_BROWN, bump_y=-4)
        draw.terminal_text(x_coord + 4, y_coord + 5, '[R2]', ORANGE, bump_y=-4)

        registers = [
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 1, 0]
        ]
        for i, register in enumerate(registers):
            _register_switch = copy.deepcopy(SnapObjects.REGISTER_C_SWITCH) if (
                        i == len(registers) - 1) else copy.deepcopy(SnapObjects.REGISTER_AB_SWITCH)

            row = i if i < 2 else 3

            for j, bit in enumerate(register):
                switch_value = bit == 1
                draw.switch(x_coord + 6 + j, y_coord + 1 + row, _register_switch, switch_value)

    def draw_io_panel(x, y):
        x_coord = x
        y_coord = y

        draw.panel(x_coord, y_coord, x_coord + 10, y_coord + 1, SnapObjects.GREY_PANEL)

        fake_input_bits = [0, 0, 1, 1, 0]
        fake_output_bits = [1, 0, 0, 1, 1]

        for i, bit in enumerate(fake_output_bits):
            draw.prong(i + x + 8, 2, SnapObjects.OUTPUT_PRONG, bit)

        for i, bit in enumerate(fake_input_bits):
            draw.prong(i + x, 1, SnapObjects.INPUT_PRONG, bit)

        draw.terminal_text(x + 5, y + 1, 'INPUT', LIGHT_BLUE, bump_x=7, bump_y=-4)
        draw.terminal_text(x + 7, y + 1, '/', WHITE, bump_x=7, bump_y=-4)
        draw.terminal_text(x + 5, y + 2, 'OUTPUT', ORANGE, bump_x=7, bump_y=-4)

    def draw_flag_panel(x, y):
        x_coord = x
        y_coord = y
        gate_x = x + 4
        gate_y = y + 1

        dummy_bit_Z = 0
        dummy_bit_OV = 1
        dummy_jump = 1

        draw.panel(x_coord, y_coord, x_coord + 12, y_coord + 6, SnapObjects.FLAG_PANEL)
        draw.logic_gate(gate_x, gate_y + 1, SnapObjects.LOGIC_GATE_OR, [1, 0, 1])
        draw.switch(gate_x, gate_y, SnapObjects.REGISTER_C_SWITCH, dummy_bit_Z)
        draw.switch(gate_x + 3, gate_y, SnapObjects.CARRY_SWITCH, dummy_bit_OV)
        draw.switch(gate_x + 1, gate_y + 4, SnapObjects.JUMP_SWITCH, dummy_jump)

        draw.terminal_text(gate_x + 4, gate_y + 1, 'OVERFLOW', PURPLE, bump_x=10, bump_y=-4)
        draw.terminal_text(gate_x - 2, gate_y + 1, 'ZERO', ORANGE, bump_y=-4)
        draw.terminal_text(gate_x + 2, gate_y + 5, 'JUMP', LIGHT_GREEN, bump_x=7, bump_y=-4)

    def draw_instruction_panel(x, y):
        def get_instruction_index_strings():
            instruction_index_strings = []
            for i in range(Constants.INSTRUCTION_COUNT):
                instruction_index_strings.append(('[ ' + (2 - len(str(i))) * ' ') + 'I' + str(i) + ']')

            return instruction_index_strings

        x_coord = x
        y_coord = y

        draw.panel(x_coord, y_coord, x_coord + 22, y_coord + 18, SnapObjects.INSTRUCTION_PANEL)

        instruction_index_strings = get_instruction_index_strings()
        for i, instruction_index_string in enumerate(instruction_index_strings):
            draw.terminal_text(x + 7, y + i + 2, instruction_index_string, LIGHT_GREEN, bump_y=-5)
            draw.terminal_text(x + 7, y + i + 2, instruction_index_string, LIGHT_GREEN, bump_y=-5)

        input_bits = [int(bit) for bit in bin(current_instruction_index)[2:]]
        input_size = int(math.log2(Constants.INSTRUCTION_COUNT))

        for i in range(len(input_bits), input_size):
            input_bits = [0] + input_bits

        draw.switch_mapper_board(x_coord, y_coord + 1, input_bits, SnapObjects.INSTRUCTION_SWITCH_MAPPER)

        for instruction_index, bits in enumerate(lines):
            is_current_instruction = (instruction_index == current_instruction_index)

            if is_current_instruction:
                pass

            for bit_index, bit in enumerate(bits):
                switch = instruction_switch_layout[bit_index] if is_current_instruction else SnapObjects.SWITCH
                switch_value = str(bit) == "1"
                draw.switch(x + 10 + bit_index, y + 1 + instruction_index, switch, switch_value)

        for instruction_index in range(len(lines), Constants.INSTRUCTION_COUNT):
            for bit_index, bit in enumerate(bits):
                draw.switch(x + 10 + bit_index, y + 1 + instruction_index, SnapObjects.SWITCH_INACTIVE, 0)

    def draw_assembly_panel(x, y):
        x_coord = x
        y_coord = y

        draw.panel(x_coord, y_coord, x_coord + 22, y_coord, SnapObjects.GREY_PANEL)

        draw.terminal_text(x + 1, y + 1, f'ASSEMBLY', WHITE, bump_y=-4)
        draw.terminal_text(x + 5, y + 1, f'I{current_instruction_index}', WHITE, bump_y=-4)
        draw.terminal_text(x + 7, y + 1, f'{Instructions.assembly[current_instruction_index]}', WHITE, bump_y=-4)
        draw.terminal_text(x + 16, y + 1, f'INPUT INJECT 0', WHITE, bump_y=-4)

    memory = Memory()

    draw = DrawTools.DrawTools(canvas)
    draw_hkiac_panel(1, 1)
    draw_instruction_panel(1, 5)
    draw_alu_panel(39, 1)
    draw_memory_panel(25, 19)
    draw_register_panel(25, 12)
    draw_flag_panel(25, 4)
    draw_io_panel(25, 1)
    draw_assembly_panel(1, 25)