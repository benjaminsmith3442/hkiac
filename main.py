import math
import os
import sys
import tkinter as tk
from PIL import ImageTk
from PIL.Image import Palette

import View.Arrows as Arrows
from Util.AsmParser import Instructions
from Util.constants import Constants
from Components.Memory import Memory
from PIL import Image
import View.DrawTools as DrawTools
import View.SnapObjects as SnapObjects
from View.Palette import WHITE, GREEN, TEST_RED, LIGHT_BLUE

# from View.SnapObjects import SPIRAL_FREE_LINE

if (len(sys.argv) == 2) and os.path.isfile(sys.argv[1]):
    Instructions.populate_instructions_from_file(sys.argv[1])
else:
    Instructions.populate_instructions_from_file('resources/instructions.txt')

lines = Instructions.machine
current_instruction_index = 0

root = tk.Tk()
root.title("H.K.I.A.C.")
root.resizable(False, False)
canvas = tk.Canvas(root, width=1425, height=1200, bg="black")
canvas.pack()

instruction_switch_layout = []
INSTRUCTION_SWITCHES = [
    SnapObjects.OPCODE_SWITCH,
    SnapObjects.MEMORY_SWITCH,
    SnapObjects.NUMERIC_SWITCH,
    SnapObjects.REGISTER_SWITCH
]
for i, width in enumerate(Constants.INSTRUCTION_WIDTHS):
    for j in range(width):
        instruction_switch_layout.append(INSTRUCTION_SWITCHES[i])


hkiac_img = Image.open("resources/hkiac.png")
tk_img = ImageTk.PhotoImage(hkiac_img)


def draw_screen():
    canvas.delete("all")

    def draw_gi_joe():
        x_coord = 1263
        y_coord = 53

        label = tk.Label(
            root,
            image=tk_img,
            borderwidth=0,
            highlightthickness=0,
            padx=0,
            pady=0
        )
        label.place(x=x_coord, y=y_coord)

    def draw_hkiac_panel(x, y):
        x_coord = x
        y_coord = y

        draw.panel(x_coord, y_coord, x_coord + 18, y_coord + 12, SnapObjects.HKIAC_PANEL)

    def draw_hints(): pass
        # draw.terminal_text(35, 3, f"[{Arrows.UP}][{Arrows.DOWN}]", 'WHITE')

    def draw_opcode_panel(x,y):
        x_coord = x
        y_coord = y

        draw.panel(x_coord, y_coord, x_coord + 9, y_coord + 18, SnapObjects.OPCODE_PANEL)

        TEMP = [0, 0, 1, 1]
        draw.switch_mapper_board(x_coord, y_coord + 1, TEMP, SnapObjects.OPCODE_SWITCH_MAPPER)

        for i, opcode in enumerate(Constants.OPCODE_ORDER):
            opcode = opcode + ((3 - len(opcode)) * ' ')
            draw.terminal_text(x_coord + 7, 3 + i, f"[{opcode}]", "lime", bump_y=-5)

        null_opcodes = 2 ** Constants.OP_CODE_INSTRUCTION_SIZE - len(Constants.OPCODE_ORDER)
        available_opcodes = 2 ** Constants.OP_CODE_INSTRUCTION_SIZE

        for i in range(null_opcodes, available_opcodes):
            null_opcode = 3 * ' '
            draw.terminal_text(x_coord + 7, 3 + i, f"[{null_opcode}]", "lime", bump_y=-5)

    def draw_alu_panel(x, y):
        x_coord = x
        y_coord = y
        gate_x = x_coord + 4
        gate_y = y_coord + 4

        draw.panel(x_coord, y_coord, x_coord + 19, y_coord + 16, SnapObjects.ALU_PANEL)


        gate_row = 3
        draw.logic_gate(gate_x + 6, gate_y + (0 * gate_row), SnapObjects.LOGIC_GATE_XOR, [1, 1, 1])
        draw.logic_gate(gate_x + 0, gate_y + (1 * gate_row), SnapObjects.LOGIC_GATE_XOR, [1, 1, 1])
        draw.logic_gate(gate_x + 4, gate_y + (1 * gate_row), SnapObjects.LOGIC_GATE_AND, [1, 1, 1])
        draw.logic_gate(gate_x + 8, gate_y + (1 * gate_row), SnapObjects.LOGIC_GATE_AND, [1, 1, 1])
        draw.logic_gate(gate_x + 2, gate_y + (2 * gate_row), SnapObjects.LOGIC_GATE_OR, [1, 1, 1])

    def draw_memory_panel(x, y): #TODO this is very static. Need it to be malleable, rubbery, maybe flubbery
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

        draw.terminal_text(x_coord + 5, y_coord + 2, "[M0]", LIGHT_BLUE, bump_y=-5)
        draw.terminal_text(x_coord + 5, y_coord + 3, "[M1]", LIGHT_BLUE, bump_y=-5)
        draw.terminal_text(x_coord + 5, y_coord + 4, "[M2]", LIGHT_BLUE, bump_y=-5)
        draw.terminal_text(x_coord + 5, y_coord + 5, "[M3]", LIGHT_BLUE, bump_y=-5)


        for i, memory_index in enumerate(memory_indexes):
            for j, bit in enumerate(memory_index):
                switch_value = str(bit) == "1"
                draw.switch(x_coord + 7 + j, y_coord + 1 + i, SnapObjects.MEMORY_SWITCH, switch_value)

    def draw_register_panel(x, y):
        x_coord = x
        y_coord = y

        draw.panel(x_coord, y_coord, x_coord + 8, y_coord + 4, SnapObjects.REGISTER_PANEL)
        draw.terminal_text(x_coord+1, y_coord+2, '[R0]', TEST_RED) #TODO Im betting this can go warm n snugly into the mapper board class
        draw.terminal_text(x_coord+1, y_coord+3, '[R1]', TEST_RED)
        draw.terminal_text(x_coord+1, y_coord+4, '[R2]', TEST_RED)

        registers = [
            [0, 0, 0, 1, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 1, 0]
        ]
        for i, register in enumerate(registers):
            for j, bit in enumerate(register):
                switch_value = bit == 1
                draw.switch(x_coord + 3 + j, y_coord + 1 + i, SnapObjects.REGISTER_SWITCH, switch_value)

    def draw_io_panel(x, y):
        x_coord = x
        y_coord = y

        draw.panel(x_coord, y_coord, x_coord + 3, y_coord + 12, SnapObjects.IO_PANEL)
        # draw.draw_free_lines(SPIRAL_FREE_LINE)

    def draw_flag_panel(x, y):
        x_coord = x
        y_coord = y

        draw.panel(x_coord, y_coord, x_coord + 18, y_coord + 4, SnapObjects.FLAG_PANEL)

        draw.logic_gate(x_coord + 4, y_coord + 1, SnapObjects.LOGIC_GATE_OR, [1, 0, 1])

    def draw_instruction_panel(x, y):
        x_coord = x
        y_coord = y

        draw.panel(x_coord, y_coord, x_coord + 19, y_coord + 18, SnapObjects.INSTRUCTION_PANEL)

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
                draw.switch(8 + bit_index, 2 + instruction_index, switch, switch_value)

        for instruction_index in range(len(lines), Constants.INSTRUCTION_COUNT):
            for bit_index, bit in enumerate(bits):
                draw.switch(8 + bit_index, 2 + instruction_index, SnapObjects.SWITCH_INACTIVE, 0)

    def stage_bits_from_instruction(): #TODO this is very temporary
        pass



    memory = Memory()


    draw = DrawTools.DrawTools(canvas)
    draw_gi_joe()
    draw_hkiac_panel(33, 1)
    draw_instruction_panel(1, 1)
    draw_hints()
    draw_alu_panel(1, 21)
    draw_memory_panel(33, 21)
    draw_register_panel(33, 29)
    draw_flag_panel(33, 15)
    draw_opcode_panel(22,1)
    # draw_io_panel(49,21)













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

draw_screen()
root.mainloop()
