from collections.abc import Container
from tracemalloc import Snapshot

from Util.constants import Constants
from View.Palette import WHITE, GREY_DARK, BLACK
import copy

_SNAP_SIZE = 27
_PANEL_BUMP_X = 5
_PANEL_BUMP_Y = -10

class DrawTools:
    def __init__(self, canvas):
        self.canvas = canvas

    def __layer_rectangles(self, x1=None, y1=None, x2=None, y2=None, snap_object=None, alignments=None):
        alignments = alignments or [''] * len(snap_object.offsets)

        x1 = self._snap(x1)
        y1 = self._snap(y1)
        x2 = self._snap(x2)
        y2 = self._snap(y2)

        for offset, color, alignment in zip(snap_object.offsets, snap_object.colors, alignments):
            offset_west = 0 if ('W' in alignment) else offset
            offset_east = 0 if ('E' in alignment) else offset
            offset_north = 0 if ('N' in alignment) else offset
            offset_south = 0 if ('S' in alignment) else offset

            self.canvas.create_rectangle(
                x1 + offset_west, y1 + offset_north,
                x2 - offset_east + _SNAP_SIZE, y2 - offset_south + _SNAP_SIZE,
                outline="",
                fill=color
            )

    def switch(self, x, y, snap_object, bit=0, alignments=None):
        so_copy = copy.deepcopy(snap_object)
        if bit:
            so_copy.load_as_active()
        else:
            so_copy.load_as_inactive()
        self.__layer_rectangles(x1=x, y1=y, x2=x, y2=y, snap_object=so_copy, alignments=alignments)

    def panel(self, x1, y1, x2, y2, snap_object):
        so_copy = copy.deepcopy(snap_object)
        self.__layer_rectangles(x1=x1, y1=y1, x2=x2, y2=y2, snap_object=so_copy)
        if so_copy.title.text is not None:
            self.terminal_text(x1 + 2, y1 + 1, so_copy.title.text, so_copy.title.text_color, bump_x=_PANEL_BUMP_X, bump_y=_PANEL_BUMP_Y, box_color=so_copy.title.box_color)

    def __mapper_selector(self, x, y, snap_object):
        so_copy = copy.deepcopy(snap_object)
        east_alignments = ['E'] * len(so_copy['left'].offsets)
        west_alignments = ['W'] * len(so_copy['right'].offsets)
        self.__layer_rectangles(x1=x, y1=y, x2=x, y2=y, snap_object=so_copy['left'], alignments=east_alignments)
        self.__layer_rectangles(x1=x+1, y1=y, x2=x+1, y2=y, snap_object=so_copy['right'], alignments=west_alignments)

    def __horizontal_mapper(self, x, y, snap_object, length, bit=0):
    #     so_copy = copy.deepcopy(snap_object)
    #     if not bit: so_copy.colors[-1] = GREY_DARK
    #     x2 = x + length
    #     self.__layer_rectangles(x1=x, y1=y, x2=x2, y2=y, snap_object=so_copy)
        so_copy = copy.deepcopy(snap_object)
        if bit:
            so_copy.load_as_active()
        else:
            so_copy.load_as_inactive()
        x2 = x + length
        self.__layer_rectangles(x1=x, y1=y, x2=x2, y2=y, snap_object=so_copy)

    def __vertical_mapper(self, x, y, snap_object, length, bit=0):
        so_copy = copy.deepcopy(snap_object)
        if bit:
            so_copy.load_as_active()
        else:
            so_copy.load_as_inactive()
        y2 = y + length
        self.__layer_rectangles(x1=x, y1=y, x2=x, y2=y2, snap_object=so_copy)

    def switch_mapper_board(self, x, y, input_bits, schema):
        x_start = x
        y_start = y
        output_bits = [0] * (2 ** len(input_bits))
        output_index = int("".join(map(str, input_bits)), 2)
        output_bits[output_index] = 1

        for i, bit in enumerate(input_bits):
            self.switch(x_start + i + 1, y + len(output_bits), schema.switch_board_input, bit)

        for i, bit in enumerate(output_bits):
            output_start_x = x_start + len(input_bits) + 1
            self.switch(output_start_x, y + i, schema.mapper_selector_none, bit)

            if bit == 1:
                self.__mapper_selector(output_start_x, y + i, schema.selector)

        for i in range(1, len(input_bits) + 1):
            x = i + x_start
            y = y_start
            rect_count = (2 ** i)
            mapper_height = int(len(output_bits) / rect_count)

            for j in range(rect_count):
                bit_mapped = (j + input_bits[i - 1]) % 2 == 0
                self.__vertical_mapper(x, y, schema, mapper_height - 1, bit_mapped)
                y += mapper_height

    def terminal_text(self, x, y, text, color, bump_x=0, bump_y=0, box_color=None):
        text_id = self.canvas.create_text(
            x * _SNAP_SIZE + bump_x,
            y * _SNAP_SIZE + bump_y,
            text=text,
            font=("Terminal", 16, "bold"),
            fill=color,
            width=20 * len(text),
            anchor="sw",
            justify="left"
        )

        if box_color is not None:
            # self.canvas.create_rectangle()
            x1, y1, x2, y2 = self.canvas.bbox(text_id)
            rect_id = self.canvas.create_rectangle(x1 - _SNAP_SIZE, y1, x2 + _SNAP_SIZE, y2, fill=box_color, outline="") #TODO fix this up a bit
            self.canvas.tag_raise(text_id, rect_id)




    def logic_gate(self, x, y, snap_object, bits):
        sc = copy.deepcopy(snap_object)

        if sc.has_single_input:
            self.__layer_rectangles(x1=x, y1=y, x2=x + 2, y2=y + 2, snap_object=sc)
            self.__layer_rectangles(x1=x, y1=y, x2=x + 2, y2=y + 2, snap_object=sc)
            self.terminal_text(x + 1, y + 2, sc.label, sc.label_color, bump_x=0, bump_y=-5)
            self.switch(x + 1, y, snap_object.input_a, bit=bits[0])
            self.switch(x + 1, y + 2, snap_object.output, bit=bits[1])
        else:
            self.__layer_rectangles(x1=x, y1=y, x2=x + 3, y2=y + 2, snap_object=sc)
            self.__layer_rectangles(x1=x, y1=y, x2=x + 3, y2=y + 2, snap_object=sc)
            self.terminal_text(x + 1, y + 2, sc.label, sc.label_color, bump_x=12, bump_y=-5)
            self.switch(x, y, snap_object.input_a, bit=bits[0], alignments=['', 'NW', ''])
            self.switch(x + 3, y, snap_object.input_b, bit=bits[1], alignments=['', 'NE', ''])
            self.switch(x + 1, y + 2, snap_object.output, bit=bits[2], alignments=['', 'ES', 'E'])
            self.switch(x + 2, y + 2, snap_object.output, bit=bits[2], alignments=['', 'WS', 'W'])





    def draw_free_lines(self, snap_object, nodes):
        sc = copy.deepcopy(snap_object)

        for _sc in [sc.outer_line, sc.inner_line]:
            index = 0

            while index + 1 in nodes:
                x1 = nodes[index]['x']
                y1 = nodes[index]['y']
                x2 = nodes[index + 1]['x']
                y2 = nodes[index + 1]['y']

                if x1 > x2:
                    x1, x2 = x2, x1
                if y1 > y2:
                    y1, y2 = y2, y1

                self.__layer_rectangles(x1=x1, y1=y1, x2=x2, y2=y2, snap_object=_sc)

                index += 1

    @staticmethod
    def _snap(bucket):
        return bucket * _SNAP_SIZE
