import copy
import math
import os
import sys
import tkinter as tk
from PIL import ImageTk

from Components.Util import get_instruction_memory, get_instruction_immediate
from Util.AsmParser import Instructions
from Util.constants import Constants
from Components.Memory import Memory
from Components.Registers import Registers
from PIL import Image
import View.DrawTools as DrawTools
import View.SnapObjects as SnapObjects
from View.Palette import WHITE, BLACK, ORANGE, TEAL, GREY_LIGHTER

if (len(sys.argv) == 2) and os.path.isfile(sys.argv[1]):
    Instructions.populate_instructions_from_file(sys.argv[1])
else:
    Instructions.populate_instructions_from_file('resources/instructions.txt')

lines = Instructions.machine
current_instruction_index = 0

root = tk.Tk()
root.title("H.K.I.A.C.")
root.resizable(False, False)
canvas = tk.Canvas(root, width=1450, height=725, bg=BLACK)
canvas.pack()

instruction_switch_layout = []
INSTRUCTION_SWITCHES = [
    SnapObjects.OPCODE_SWITCH,
    SnapObjects.MEMORY_SWITCH,
    SnapObjects.NUMERIC_SWITCH,
    SnapObjects.REGISTER_AB_SWITCH
]
for i, width in enumerate(Constants.INSTRUCTION_WIDTHS):
    for j in range(width):
        instruction_switch_layout.append(INSTRUCTION_SWITCHES[i])


hkiac_img = Image.open("resources/hkiac_text3.png")
tk_img = ImageTk.PhotoImage(hkiac_img)


def draw_screen():
    canvas.delete("all")

    def draw_hkiac_panel(x, y):
        label = tk.Label(
            root,
            image=tk_img,
            borderwidth=0,
            highlightthickness=0,
            padx=0,
            pady=0
        )
        label.place(x=20, y=25)


    def draw_alu_panel(x, y):
        def draw_panel(_x, _y):
            draw.panel(_x, _y, _x + 13, _y + 24, SnapObjects.ALU_PANEL)

        def draw_carry_in_flag(_x, _y):
            arrows_x = _x
            arrows_y = _y - 3
            for i in range(3): #TODO probably gotta be smarter in this area with x and y
                grid_coord_x = arrows_x * 27
                grid_coord_y = (i * 27) + (arrows_y * 27)
                points = [
                    0 + grid_coord_x, 0 + grid_coord_y,  # top-left
                    26 + grid_coord_x, 0 + grid_coord_y,  # top-right
                    13 + grid_coord_x, 22 + grid_coord_y  # bottom point (apex, pointing downward)
                ]

                canvas.create_polygon(points, fill="purple", outline="") #TODO move color value elsewhere

            draw.switch(_x, _y, SnapObjects.SWITCH, 1)

        def draw_carry_out_flag(_x, _y): draw.switch(_x, _y, SnapObjects.CARRY_SWITCH, 1)

        def draw_zero_flag(_x, _y): draw.switch(_x, _y, SnapObjects.ZERO_SWITCH, 1)

        def draw_r0_r1(_x, _y):
            for i, reg_input in enumerate([r0, r1]):
                for j, bit in enumerate(reg_input):
                    switch_value = bit == 1
                    switch_style = SnapObjects.REGISTER_AB_SWITCH if (j == len(reg_input) - 1) else SnapObjects.SWITCH
                    draw.switch(_x + j, _y + i, switch_style, switch_value)

        def draw_r2(_x, _y):
            for i, bit in enumerate(r2):
                switch_value = bit == 1
                switch_style = SnapObjects.REGISTER_C_SWITCH if i == 0 else SnapObjects.SWITCH
                draw.switch(_x + i, _y, switch_style, switch_value)

        def draw_logic_gates(_x, _y):
            _row_spacing = 3
            draw.logic_gate(_x + 3, _y - 8, SnapObjects.LOGIC_GATE_NOT, [0, 1])
            draw.logic_gate(_x + 6, _y + (0 * _row_spacing), SnapObjects.LOGIC_GATE_XOR, [1, 1, 1])
            draw.logic_gate(_x + 8, _y + (1 * _row_spacing), SnapObjects.LOGIC_GATE_XOR, [1, 1, 1])
            draw.logic_gate(_x + 4, _y + (1 * _row_spacing), SnapObjects.LOGIC_GATE_AND, [1, 1, 1])
            draw.logic_gate(_x + 0, _y + (1 * _row_spacing), SnapObjects.LOGIC_GATE_AND, [1, 1, 1])
            draw.logic_gate(_x + 2, _y + (2 * _row_spacing), SnapObjects.LOGIC_GATE_OR, [1, 1, 1])

        def draw_logic_routes(_x, _y, is_inverted): #TODO these actually might make sense in the draw tools class as static method returns
            _a = {
                0: {'x': _x - 4, 'y': _y + 13},
                1: {'x': _x - 4, 'y': _y + 7},
                2: {'x': _x, 'y': _y + 7},
                3: {'x': _x, 'y': _y + 6},
                4: {'x': _x, 'y': _y + 7},
                5: {'x': _x + 2, 'y': _y + 7},
                6: {'x': _x + 2, 'y': _y + 10}
            }
            _b = {
                0: {'x': _x - 1, 'y': _y + 13},
                1: {'x': _x - 1, 'y': _y + 8},
                2: {'x': _x + 4, 'y': _y + 8},
                3: {'x': _x + 4, 'y': _y},
                4: {'x': _x + 1, 'y': _y},
                5: {'x': _x + 4, 'y': _y},
                6: {'x': _x + 4, 'y': _y + 8},
                7: {'x': _x + 5, 'y': _y + 8},
                8: {'x': _x + 5, 'y': _y + 10}
            }
            _carry_in = {
                0: {'x': _x, 'y': _y + 13},
                1: {'x': _x, 'y': _y + 9},
                2: {'x': _x + 6, 'y': _y + 9},
                3: {'x': _x + 6, 'y': _y + 4},
                4: {'x': _x + 6, 'y': _y + 9},
                5: {'x': _x + 7, 'y': _y + 9},
                6: {'x': _x + 7, 'y': _y + 13}
            }
            _carry_out = {
                0: {'x': _x + 6, 'y': _y + 17},
                1: {'x': _x + 6, 'y': _y + 18}
            }
            _register_2 = {
                0: {'x': _x, 'y': _y + 20},
                1: {'x': _x, 'y': _y + 22},
                2: {'x': _x + 1, 'y': _y + 22},
            }

            _zero = {
                0: {'x': _x - 1, 'y': _y + 20},
                1: {'x': _x - 1, 'y': _y + 22},
                2: {'x': _x - 2, 'y': _y + 22},
            }

            _not_input = {
                0: {'x': _x, 'y': _y + 2},
                1: {'x': _x, 'y': _y + 2}
            }
            _not_output = {
                0: {'x': _x, 'y': _y + 20},
                1: {'x': _x, 'y': _y + 20},
                2: {'x': _x, 'y': _y + 20}
            }
            _not_bypassed = {
                0: {'x': _x, 'y': _y + 20},
                1: {'x': _x, 'y': _y + 20},
                2: {'x': _x, 'y': _y + 20}
            }

            draw.draw_free_lines(SnapObjects.INPUT_A_FREELINE, _a)
            draw.draw_free_lines(SnapObjects.INPUT_B_FREELINE, _b)
            draw.draw_free_lines(SnapObjects.INPUT_A_FREELINE, _not_input)
            draw.draw_free_lines(SnapObjects.CARRY_IN_FREELINE, _carry_in)
            draw.draw_free_lines(SnapObjects.CARRY_FLAG_FREELINE, _carry_out)
            draw.draw_free_lines(SnapObjects.REGISTER_2_FREELINE, _register_2)
            draw.draw_free_lines(SnapObjects.ZERO_FLAG_FREELINE, _zero)



        r0 = registers.read([0])
        r1 = registers.read([1])
        r2 = registers.read()

        draw_panel(x, y)
        draw_carry_in_flag(x + 11, y + 4)
        draw_carry_out_flag(x + 11, y + 20)
        draw_zero_flag(x + 2, y + 23)
        draw_r0_r1(x + 1, y + 1)
        draw_r2(x + 7, y + 23)
        draw_logic_gates(x + 1, y + 12)
        draw_logic_routes(x + 5, y + 1, is_inverted=False)






    def draw_memory_panel(x, y): #TODO this is very static. Need it to be malleable, rubbery, maybe flubbery
        x_coord = x
        y_coord = y

        draw.panel(x_coord, y_coord, x_coord + 12, y_coord + 6, SnapObjects.MEMORY_PANEL)

        memory_indexes = [
            memory.read([0, 0]),
            memory.read([0, 1]),
            memory.read([1, 0]),
            memory.read([1, 1])
        ]

        draw.switch_mapper_board(x_coord, y_coord + 1, [0, 1], SnapObjects.MEMORY_SWITCH_MAPPER)

        draw.terminal_text(x_coord + 5, y_coord + 2, "[M0]", GREY_LIGHTER, bump_y=-5)
        draw.terminal_text(x_coord + 5, y_coord + 3, "[M1]", GREY_LIGHTER, bump_y=-5)
        draw.terminal_text(x_coord + 5, y_coord + 4, "[M2]", GREY_LIGHTER, bump_y=-5)
        draw.terminal_text(x_coord + 5, y_coord + 5, "[M3]", GREY_LIGHTER, bump_y=-5)


        for i, memory_index in enumerate(memory_indexes):
            sc = copy.deepcopy(SnapObjects.INPUT_SWITCH) if i == len(memory_indexes) - 1 else copy.deepcopy(SnapObjects.MEMORY_SWITCH)
            for j, bit in enumerate(memory_index):
                switch_value = str(bit) == "1"
                draw.switch(x_coord + 7 + j, y_coord + 1 + i, sc, switch_value)


    def draw_register_panel(x, y):
        x_coord = x + 1
        y_coord = y

        draw.panel(x, y, x + 12, y + 5, SnapObjects.REGISTER_PANEL)
        draw.switch_mapper_board(x_coord, y_coord + 1, [0], SnapObjects.REGISTER_SWITCH_MAPPER)
        draw.terminal_text(x_coord+4, y_coord+2, '[R0]', GREY_LIGHTER, bump_y=-4) #TODO Im betting this can go warm n snugly into the mapper board class
        draw.terminal_text(x_coord+4, y_coord+3, '[R1]', GREY_LIGHTER, bump_y=-4)
        draw.terminal_text(x_coord+4, y_coord+5, '[R2]', GREY_LIGHTER, bump_y=-4)


        registers_index = [registers.read([0]), registers.read([1]), registers.read()]

        for i, register in enumerate(registers_index):
            _register_switch = copy.deepcopy(SnapObjects.REGISTER_C_SWITCH) if (i == len(registers_index) - 1) else copy.deepcopy(SnapObjects.REGISTER_AB_SWITCH)

            row = i if i < 2 else 3

            for j, bit in enumerate(register):
                switch_value = bit == 1
                draw.switch(x_coord + 6 + j, y_coord + 1 + row, _register_switch, switch_value)

    def draw_io_panel(x, y):
        x_coord = x
        y_coord = y

        draw.panel(x_coord, y_coord, x_coord + 10, y_coord + 1, SnapObjects.GREY_PANEL)

        fake_input_bits = [0,0,1,1,0]
        fake_output_bits = [1,0,0,1,1]

        for i, bit in enumerate(fake_output_bits):
            draw.prong(i + x + 8, 2, SnapObjects.OUTPUT_PRONG, bit)

        for i, bit in enumerate(fake_input_bits):
            draw.prong(i + x, 1, SnapObjects.INPUT_PRONG, bit)

        draw.terminal_text(x + 5, y + 1, 'INPUT', TEAL, bump_x=7, bump_y=-4)
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
        draw.switch(gate_x, gate_y, SnapObjects.ZERO_SWITCH, dummy_bit_Z)
        draw.switch(gate_x + 3, gate_y, SnapObjects.CARRY_SWITCH, dummy_bit_OV)
        draw.switch(gate_x + 1, gate_y + 4, SnapObjects.JUMP_SWITCH, dummy_jump)

        draw.terminal_text(gate_x + 4, gate_y + 1, 'OVERFLOW', GREY_LIGHTER, bump_x=10, bump_y=-4)
        draw.terminal_text(gate_x - 2, gate_y + 1, 'ZERO', GREY_LIGHTER, bump_y=-4)
        draw.terminal_text(gate_x + 2, gate_y + 5, 'JUMP', GREY_LIGHTER, bump_x=7, bump_y=-4)

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
            draw.terminal_text(x + 7, y + i +2, instruction_index_string, GREY_LIGHTER, bump_y=-5)
            draw.terminal_text(x + 7, y + i +2, instruction_index_string, GREY_LIGHTER, bump_y=-5)

        input_bits = [int(bit) for bit in bin(current_instruction_index)[2:]]
        input_size = int(math.log2(Constants.INSTRUCTION_COUNT))

        for i in range(len(input_bits), input_size):
            input_bits = [0] + input_bits

        draw.switch_mapper_board(x_coord, y_coord + 1, input_bits, SnapObjects.INSTRUCTION_SWITCH_MAPPER)

        for instruction_index, bits in enumerate(lines):
            is_current_instruction = (instruction_index == current_instruction_index)

            if is_current_instruction:#TODO ???
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

        draw.terminal_text(x + 1, y + 1,f'ASSEMBLY', WHITE, bump_y=-4)
        draw.terminal_text(x + 5, y + 1, f'I{current_instruction_index}', WHITE, bump_y=-4)
        draw.terminal_text(x + 7, y + 1,f'{Instructions.assembly[current_instruction_index]}', WHITE, bump_y=-4)
        draw.terminal_text(x + 16, y + 1,f'INPUT INJECT 0', WHITE, bump_y=-4)


    draw = DrawTools.DrawTools(canvas)
    draw_hkiac_panel(1, 1)
    draw_instruction_panel(1, 5)
    draw_alu_panel(39, 1)
    draw_memory_panel(25, 19)
    draw_register_panel(25, 12)
    draw_flag_panel(25, 4)
    draw_io_panel(25,1)
    draw_assembly_panel(1, 25)




    # TODO this is test stuff so delete/move/whatever
    current_memory = get_instruction_memory(lines[current_instruction_index])
    current_immediate = get_instruction_immediate(lines[current_instruction_index])

    print(current_immediate, ", ", current_memory)
    memory.write(current_immediate, current_memory)




def move_highlight(event):
    global current_instruction_index
    if event.keysym == "Up":
        current_instruction_index = max(0, current_instruction_index - 1)
    elif event.keysym == "Down":
        current_instruction_index = min(len(lines) - 1, current_instruction_index + 1)
    draw_screen()

def exit_app(event):
    root.destroy()

root.bind("<Up>", move_highlight)
root.bind("<Down>", move_highlight)
root.bind("<Q>", exit_app)





current_memory = get_instruction_memory(lines[current_instruction_index])
current_immediate = get_instruction_immediate(lines[current_instruction_index])

memory = Memory()
print(current_immediate, ", ", current_memory)
memory.write(current_immediate, current_memory)


registers = Registers()
registers.write([1, 1, 1, 1, 1], [0])
registers.write([1, 0, 0, 1, 1], [1])
registers.write([0, 1, 0, 1, 0])





draw_screen()
root.mainloop()
