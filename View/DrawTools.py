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

            # print('W', offset_west, 'E', offset_east, 'N', offset_north, 'S', offset_south)

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

    # def __horizontal_mapper(self, x, y, snap_object, length, bit=0):
    #     so_copy = copy.deepcopy(snap_object)
    #     if not bit: so_copy.colors[-1] = GREY_DARK
    #     x2 = x + length
    #     self.__layer_rectangles(x1=x, y1=y, x2=x2, y2=y, snap_object=so_copy)

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

    def logic_gate(self, x, y, snap_object, bits=None):
        bits = bits or [0, 0, 0]
        so_copy = copy.deepcopy(snap_object)
        label_color = None

        if bits[-1] == 1:
            so_copy.load_as_active()
            label_color = so_copy.active_label_color
        else:
            so_copy.load_as_inactive()
            label_color = so_copy.inactive_label_color

        self.__layer_rectangles(x1=x, y1=y, x2=x + 3, y2=y + 2, snap_object=so_copy)
        self.__layer_rectangles(x1=x, y1=y, x2=x + 3, y2=y + 2, snap_object=so_copy)
        self.terminal_text(x + 1, y + 2, so_copy.label, label_color, bump_x=12, bump_y=-5)
        self.switch(x, y, snap_object.switch_a, bit=bits[0], alignments=['NW', 'NW', 'N'])
        self.switch(x + 3, y, snap_object.switch_b, bit=bits[1], alignments=['NE', 'NE', 'N'])
        self.switch(x + 1, y + 2, snap_object.switch_c, bit=bits[2], alignments=['', 'SE', 'SE'])
        self.switch(x + 2, y + 2, snap_object.switch_c, bit=bits[2], alignments=['', 'SW', 'SW'])

    # self.mapped_tiles[node_key - 2] = {
    #     'x': node_a['x'],
    #     'y': node_a['y'],
    #     'line_alignment': line_alignment,
    #     'elbow_alignment': elbow_alignment,
    #     'length': distance,
    #     'direction': direction
    # }

    # def draw_free_lines(self, snap_object):
    #     so_copy = copy.deepcopy(snap_object)
    #
    #     for tile in so_copy.tile_map:
    #         x_elbow = 0
    #         x1_line = 0
    #         x2_line = 0
    #         y_elbow = 0
    #         y1_line = 0
    #         y2_line = 0
    #
    #         #TODO a lot of this can seriously go into the map itself
    #         # print('line',tile['line_alignment'])
    #         # print('elbow',tile['elbow_alignment'])
    #         # print('')
    #
    #         if tile['direction'] == Constants.DOWN:
    #             x_elbow = tile['length']
    #             y_elbow = tile['y'] + tile['length']
    #             x1_line = tile['x']
    #             y1_line = tile['y']
    #             x2_line = tile['x']
    #             y2_line = tile['y'] + tile['length'] - 1
    #
    #         if tile['direction'] == Constants.UP:
    #             x_elbow = tile['length']
    #             y_elbow = tile['y'] - tile['length']
    #             x1_line = tile['x']
    #             y1_line = tile['y'] - tile['length'] + 1
    #             x2_line = tile['x']
    #             y2_line = tile['y']
    #
    #         if tile['direction'] == Constants.LEFT:
    #             x_elbow = tile['x'] - tile['length']
    #             y_elbow = tile['length']
    #             x1_line = tile['x'] - tile['length'] + 1
    #             y1_line = tile['y']
    #             x2_line = tile['x']
    #             y2_line = tile['y']
    #
    #         if tile['direction'] == Constants.RIGHT:
    #             x_elbow = tile['x'] + tile['length']
    #             y_elbow = tile['length']
    #             x1_line = tile['x']
    #             y1_line = tile['y']
    #             x2_line = tile['x'] + tile['length'] + 1
    #             y2_line = tile['y']
    #
    #         # print(tile['x'],', ',tile['y'],',',tile['x'] + x_line, ',', tile['y'] + y_line)
    #
    #         self.__layer_rectangles(
    #             x1=x1_line,
    #             y1=tile['y'] + y1_line,
    #             x2=tile['x'] + x2_line,
    #             y2=tile['y'] + y2_line,
    #             snap_object=so_copy,
    #             alignments=['', tile['line_alignment']]
    #         )

            # self.__layer_rectangles(
            #     x1=tile['x'] + x_length,
            #     y1=tile['y'] + y_length,
            #     x2=tile['x'] + x_length,
            #     y2=tile['y'] + y_length,
            #     snap_object=so_copy,
            #     alignments=tile['elbow_alignment']
            # )



    # def hkiac(self, x, y, tk, img):
    #     x_coord = 1440
    #     y_coord = 20
    #
    #     label = tk.Label(
    #         root,
    #         image=tk_img,
    #         borderwidth=0,
    #         highlightthickness=0,
    #         padx=0,
    #         pady=0
    #     )
    #     label.place(x=x_coord, y=y_coord)

    @staticmethod
    def _snap(bucket):
        return bucket * _SNAP_SIZE
