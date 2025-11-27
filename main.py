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
from View.Palette import WHITE, GREEN

if (len(sys.argv) == 2) and os.path.isfile(sys.argv[1]):
    Instructions.populate_instructions_from_file(sys.argv[1])
else:
    Instructions.populate_instructions_from_file('resources/instructions.txt')

lines = Instructions.machine
current_instruction_index = 0

root = tk.Tk()
root.title("H.K.I.A.C.")
root.resizable(False, False)
canvas = tk.Canvas(root, width=1220, height=950, bg="black")
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
        x_coord = 1047
        y_coord = 20

        label = tk.Label(
            root,
            image=tk_img,
            borderwidth=0,
            highlightthickness=0,
            padx=0,
            pady=0
        )
        label.place(x=x_coord, y=y_coord)

    def draw_hints():
        draw.terminal_text(35, 3, f"[{Arrows.UP}][{Arrows.DOWN}]", 'WHITE')

    def draw_alu_panel():
        x_coord = 1
        y_coord = 21
        x_padding = 4
        y_padding = 6

        draw.panel(x_coord, y_coord, x_coord + 42, y_coord + 12, SnapObjects.ALU_PANEL)

        # draw.logic_gate(x_coord + 2 + (2 * x_padding),  y_coord + 2,                SnapObjects.LOGIC_GATE_XOR, [0, 0, 0])
        # draw.logic_gate(x_coord + 2,                y_coord + 2 + y_padding,        SnapObjects.LOGIC_GATE_AND, [0, 0, 0])
        # draw.logic_gate(x_coord + 2 + x_padding,        y_coord + 2 + y_padding,        SnapObjects.LOGIC_GATE_AND, [0, 0, 0])
        # draw.logic_gate(x_coord + 2 + (2 * x_padding),  y_coord + 2 + y_padding,        SnapObjects.LOGIC_GATE_XOR, [0, 0, 0])
        # draw.logic_gate(x_coord + (x_padding / 2),  y_coord + 2 + (2 * y_padding),  SnapObjects.LOGIC_GATE_OR, [0, 0, 0])

    def draw_memory_panel(): #TODO this is very static. Need it to be malleable, rubbery, maybe flubbery
        x_coord = 22
        y_coord = 1

        draw.panel(x_coord, y_coord, x_coord + 10, y_coord + 6, SnapObjects.MEMORY_PANEL)

        memory.store([0, 1], [0, 0, 0, 1, 0])

        memory_indexes = [
            memory.read([0, 0]),
            memory.read([0, 1]),
            memory.read([1, 0]),
            memory.read([1, 1])
        ]

        draw.switch_mapper_board(x_coord, y_coord + 1, [0, 1], SnapObjects.MEMORY_SWITCH_MAPPER)

        for i, memory_index in enumerate(memory_indexes):
            for j, bit in enumerate(memory_index):
                switch_value = str(bit) == "1"
                draw.switch(x_coord + 5 + j, y_coord + 1 + i, SnapObjects.MEMORY_SWITCH, switch_value)

    def draw_register_panel():
        x_coord = 22
        y_coord = 9

        draw.panel(x_coord, y_coord, x_coord + 10, y_coord + 4, SnapObjects.REGISTER_PANEL)
        draw.terminal_text(x_coord+1, y_coord+2, 'R0', 'RED')
        draw.terminal_text(x_coord+1, y_coord+3, 'R1', 'RED')
        draw.terminal_text(x_coord+1, y_coord+4, 'R2', 'RED')

    def draw_io_panel():
        x_coord = 34
        y_coord = 1

        draw.panel(x_coord, y_coord, x_coord + 9, y_coord + 18, SnapObjects.IO_PANEL)

    def draw_flag_panel():
        x_coord = 22
        y_coord = 15

        draw.panel(x_coord, y_coord, x_coord + 10, y_coord + 4, SnapObjects.FLAG_PANEL)

        draw.logic_gate(x_coord + 4, y_coord + 1, SnapObjects.LOGIC_GATE_OR, [1, 0, 1])

    def draw_instruction_panel():
        x_coord = 1
        y_coord = 1

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
    draw_io_panel()
    draw_instruction_panel()
    draw_hints()
    draw_alu_panel()
    draw_memory_panel()
    draw_register_panel()
    draw_flag_panel()












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
