import math
import os
import sys
import tkinter as tk
from PIL import ImageTk
from PIL.Image import Palette

import View.Arrows as Arrows
from Util.AsmParser import Instructions
from Util.constants import Constants
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
canvas = tk.Canvas(root, width=1600, height=950, bg="black")
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
        x_coord = 1440
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
        draw.terminal_text(7, 34, f"{Arrows.LEFT} CURRENT INSTRUCTION", WHITE)
        draw.terminal_text(7, 34, f"{Arrows.LEFT} CURRENT INSTRUCTION", WHITE)
        draw.terminal_text(7, 34, f"{Arrows.LEFT} CURRENT INSTRUCTION", WHITE)

    def draw_alu_panel():
        x_coord = 24
        y_coord = 1
        x_padding = 4
        y_padding = 6

        draw.panel(x_coord, y_coord, x_coord + 16, y_coord + 31, SnapObjects.ALU_PANEL)

        draw.logic_gate(x_coord + 2 + (2 * x_padding),  y_coord + 2,                SnapObjects.LOGIC_GATE_XOR, [0, 0, 0])
        draw.logic_gate(x_coord + 2,                y_coord + 2 + y_padding,        SnapObjects.LOGIC_GATE_AND, [0, 0, 0])
        draw.logic_gate(x_coord + 2 + x_padding,        y_coord + 2 + y_padding,        SnapObjects.LOGIC_GATE_AND, [0, 0, 0])
        draw.logic_gate(x_coord + 2 + (2 * x_padding),  y_coord + 2 + y_padding,        SnapObjects.LOGIC_GATE_XOR, [0, 0, 0])
        draw.logic_gate(x_coord + (x_padding / 2),  y_coord + 2 + (2 * y_padding),  SnapObjects.LOGIC_GATE_OR, [0, 0, 0])

    def draw_memory_panel():
        x_coord = 42
        y_coord = 9

        draw.panel(x_coord, y_coord, x_coord + 15, y_coord + 11, SnapObjects.MEMORY_PANEL)

    def draw_register_panel():
        x_coord = 42
        y_coord = 22

        draw.panel(x_coord, y_coord, x_coord + 15, y_coord + 10, SnapObjects.REGISTER_PANEL)




    draw = DrawTools.DrawTools(canvas)
    draw_gi_joe()
    draw_hints()
    draw_alu_panel()
    draw_memory_panel()
    draw_register_panel()


    input_bits = [int(bit) for bit in bin(current_instruction_index)[2:]]
    input_size = int(math.log2(Constants.INSTRUCTION_COUNT))

    for i in range(len(input_bits), input_size):
        input_bits = [0] + input_bits

    draw.switch_mapper_board(0, 1, input_bits, SnapObjects.NUMERIC_SWITCH_MAPPER)

    for instruction_index, bits in enumerate(lines):
        is_current_instruction = (instruction_index == current_instruction_index)

        if is_current_instruction:
            pass

        for bit_index, bit in enumerate(bits):
            switch = instruction_switch_layout[bit_index] if is_current_instruction else SnapObjects.SWITCH
            switch_value = str(bit) == "1"
            draw.switch(8 + bit_index, 1 + instruction_index, switch, switch_value)

    for instruction_index in range(len(lines), Constants.INSTRUCTION_COUNT):
        for bit_index, bit in enumerate(bits):
            draw.switch(8 + bit_index,1 + instruction_index, SnapObjects.SWITCH_INACTIVE, 0)

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
