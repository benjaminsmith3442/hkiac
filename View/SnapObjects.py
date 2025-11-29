from Util.constants import Constants
from View.Palette import (
    WHITE,
    GREY_LIGHT,
    BLACK,
    GREY_DARKER,
    RED,
    LIGHT_BLUE,
    PURPLE,
    YELLOW,
    GREEN,
    ORANGE,
    GREY,
    GREY_DARK, VERY_LIGHT_GREY, GREY_1, lime_green, dark_olive, almost_black, BLUE, TEST_RED
)

#TODO A lot of the exact same method signature. Add inheritance. No rush. Just whenever

# class FreeLines:
#     def __init__(self, color, nodes): #TODO Make tile_map a nested class
#         self.colors = [color, BLACK]
#         self.offsets = [0, 4]
#         self.nodes = nodes
#         self.tile_map = []
#         self.map_tiles()
#
#     def map_tiles(self):
#         node_key = 2
#         first_iteration = True
#
#         while True:
#             node_a = self.nodes[node_key - 2]
#             node_b = self.nodes[node_key - 1]
#             node_c = self.nodes[node_key]
#
#             line_alignment = ''
#             elbow_alignment = ''
#             direction = ''
#             length = 0
#
#             if node_a['x'] == node_b['x']:
#                 length = node_a['y'] - node_b['y']
#
#                 if length > 0:
#                     direction = Constants.UP
#                     elbow_alignment += 'S'
#                 else:
#                     direction = Constants.DOWN
#                     elbow_alignment += 'N'
#                 elbow_alignment += 'W' if node_b['x'] < node_c['x'] else 'E'
#
#                 line_alignment = 'NS'
#
#                 if not first_iteration:
#                     node_a['y'] += -1 if length > 0 else 1
#             else:
#                 length = node_a['x'] - node_b['x']
#
#                 if length > 0:
#                     direction = Constants.LEFT
#                     elbow_alignment += 'E'
#                 else:
#                     direction = Constants.RIGHT
#                     elbow_alignment += 'W'
#                 elbow_alignment += 'S' if node_b['y'] < node_c['y'] else 'N'
#
#                 line_alignment = 'WE'
#
#                 if not first_iteration:
#                     node_a['x'] += -1 if length > 0 else 1
#
#             length = abs(length)
#
#             self.tile_map.append({
#                 'x': node_a['x'],
#                 'y': node_a['y'],
#                 'line_alignment': line_alignment,
#                 'elbow_alignment': elbow_alignment,
#                 'length': length,
#                 'direction': direction
#             })
#
#             node_key += 1
#             first_iteration = False
#
#             if node_key not in self.nodes:
#                 if node_b['x'] == node_c['x']:
#                     length = node_b['y'] - node_c['y']
#                     if length > 0:
#                         direction = Constants.UP
#                     else:
#                         direction = Constants.DOWN
#
#                     line_alignment = 'NS'
#
#                     node_b['y'] += -1 if length > 0 else 1
#                 else:
#                     length = node_b['x'] - node_c['x']
#
#                     if length > 0:
#                         direction = self.up
#                     else:
#                         direction = self.down
#
#                     line_alignment = 'WE'
#
#                     node_b['x'] += -1 if length > 0 else 1
#
#                 length = abs(length)
#
#                 self.tile_map.append({
#                     'x': node_b['x'],
#                     'y': node_b['y'],
#                     'line_alignment': line_alignment,
#                     'elbow_alignment': elbow_alignment,
#                     'length': length,
#                     'direction': direction
#                 })
#
#                 break

class SwitchBoard:
    def __init__(self, active_colors, inactive_colors):
        self.colors = None
        self.active_colors = active_colors
        self.inactive_colors = inactive_colors
        self.offsets = [0, 4, 9]
        self.load_as_active()

    def load_as_active(self):
        self.colors = self.active_colors
    def load_as_inactive(self):
        self.colors = self.inactive_colors

class SwitchMapper:
    class MapperSelector:
        def __init__(self, colors):
            self.colors = colors
            self.offsets = [0, 4, 10]

    def __init__(self, active_colors, inactive_colors, switch_board_input, selector):
        self.colors = None
        self.offsets = [0, 9]
        self.active_colors = active_colors
        self.inactive_colors = inactive_colors
        self.switch_board_input = switch_board_input
        self.mapper_selector_none = SwitchBoard(selector, selector)
        self.selector = {
            'left': SwitchMapper.MapperSelector(selector[:2] + [WHITE]),
            'right': SwitchMapper.MapperSelector(selector[:1] + [BLACK, WHITE])
        }
        self.load_as_active()

    def load_as_active(self):
        self.colors = self.active_colors

    def load_as_inactive(self):
        self.colors = self.inactive_colors

#TODO less hardcoding in here
class LogicGate:
    class Switch:
        def __init__(self, active_colors, inactive_colors, alignments):
            self.colors = None
            self.offsets = [0, 7, 7]
            self.active_colors = active_colors
            self.inactive_colors = inactive_colors
            self.alignments = alignments
            self.load_as_inactive()

        def load_as_active(self):
            self.colors = self.active_colors

        def load_as_inactive(self):
            self.colors = self.inactive_colors

    def __init__(self, active_label_color, inactive_label_color, active_colors, inactive_colors, label):
        self.colors = None
        self.offsets = [0, 7]
        self.active_label_color = active_label_color
        self.inactive_label_color = inactive_label_color
        self.active_colors = active_colors
        self.inactive_colors = inactive_colors
        self.switch_a = LogicGate.Switch([GREY_DARK, BLACK, WHITE], [GREY_DARK, BLACK, BLACK], ['NE', 'NE', 'E'])
        self.switch_b = LogicGate.Switch([GREY_DARK, BLACK, WHITE], [GREY_DARK, BLACK, BLACK], ['NW', 'NW', 'W']) #TODO remove these alignments from class
        self.switch_c = LogicGate.Switch([GREY_DARK, BLACK, WHITE], [GREY_DARK, BLACK, BLACK], ['E', 'E', 'E'])
        self.label = label
        self.load_as_active()

    def load_as_active(self):
        self.colors = self.active_colors

    def load_as_inactive(self):
        self.colors = self.inactive_colors

class Panel:
    class Title:
        def __init__(self, title_text, title_color):
            self.colors = [BLACK] #TODO am i using this?
            self.offsets = [0]    #TODO or this?
            self.text = title_text
            self.text_color = title_color
            self.box_color = BLACK

    def __init__(self, colors, title_text, title_color):
        self.colors = colors
        self.offsets = [0, 2, 14, 16]
        self.colors_panel = colors
        self.title = Panel.Title(title_text, title_color)

#TODO   a lot of these probably have static logic that can come from the initializer.
#       Im looking at you Panel objects 0_0
SWITCH              =   SwitchBoard([GREY, BLACK, WHITE], [GREY, BLACK, BLACK])
SWITCH_INACTIVE     =   SwitchBoard([GREY_DARKER, BLACK, WHITE],[GREY_DARKER, BLACK, BLACK])
OPCODE_SWITCH       =   SwitchBoard([GREEN, BLACK, WHITE],[GREEN, BLACK, BLACK])
MEMORY_SWITCH       =   SwitchBoard([LIGHT_BLUE, BLACK, WHITE], [LIGHT_BLUE, BLACK, BLACK])
NUMERIC_SWITCH      =   SwitchBoard([WHITE, BLACK, WHITE], [WHITE, BLACK, BLACK])
REGISTER_SWITCH     =   SwitchBoard([TEST_RED, BLACK, WHITE], [TEST_RED, BLACK, BLACK])
FLAG_SWITCH         =   SwitchBoard([ORANGE, BLACK, WHITE], [ORANGE, BLACK, BLACK])
# PERIPHERAL_SWITCH   =   SwitchBoard([ORANGE, BLACK, BLACK])
COUNTER_SWITCH      =   SwitchBoard([GREY, BLACK, WHITE], [GREY, BLACK, BLACK])

INSTRUCTION_SWITCH_MAPPER   =   SwitchMapper([BLACK, BLACK], [BLACK, WHITE], COUNTER_SWITCH, [BLACK, GREY_DARK, GREY_DARK])
MEMORY_SWITCH_MAPPER        =   SwitchMapper([BLACK, BLACK], [BLACK, BLUE], MEMORY_SWITCH, [BLACK, GREY_DARK, GREY_DARK])
REGISTER_SWITCH_MAPPER      =   SwitchMapper([BLACK, BLACK], [BLACK, RED], COUNTER_SWITCH, [BLACK, GREY_DARK, GREY_DARK])
OPCODE_SWITCH_MAPPER        =   SwitchMapper([BLACK, BLACK], [BLACK, GREEN], OPCODE_SWITCH, [BLACK, GREY_DARK, GREY_DARK])

#TODO lot of args with perfect parity in this one. Also make the text class setters like in the Tile class
LOGIC_GATE_XOR  =   LogicGate(WHITE, BLACK,[GREY_DARK, BLACK],[GREY_DARK, BLACK],"XOR")
LOGIC_GATE_AND  =   LogicGate(WHITE, BLACK,[GREY_DARK, BLACK],[GREY_DARK, BLACK], "AND")
LOGIC_GATE_OR   =   LogicGate(WHITE, BLACK, [GREY_DARK, BLACK],[GREY_DARK, BLACK], "OR")

ALU_PANEL           =   Panel([GREY_LIGHT, BLACK, GREY_LIGHT, BLACK], 'ARITHMETIC LOGIC UNIT', WHITE)
MEMORY_PANEL        =   Panel([BLUE, BLACK, BLUE, BLACK], 'MEMORY', LIGHT_BLUE)
REGISTER_PANEL      =   Panel([RED, BLACK, RED, BLACK], 'REGISTERS', TEST_RED)
HKIAC_PANEL         =   Panel([WHITE, BLACK, WHITE, BLACK], None, None)
FLAG_PANEL          =   Panel([PURPLE, BLACK, PURPLE, BLACK], 'FLAGS', "violet")
INSTRUCTION_PANEL   =   Panel([GREY_LIGHT, BLACK, GREY_LIGHT, BLACK], 'MACHINE INSTRUCTIONS', WHITE)
OPCODE_PANEL        =   Panel([GREEN, BLACK, GREEN, BLACK], 'CONTROL LOGIC', "lime")
IO_PANEL            =   Panel([WHITE, BLACK, WHITE, BLACK], None, None)
BLACKOUT            =   Panel([BLACK, BLACK, BLACK, BLACK], None, None)


# spiral = {
#     0: {'x': 5, 'y': 5},
#     1: {'x': 15, 'y': 5},
#     2: {'x': 15, 'y': 15},
#     3: {'x': 5, 'y': 15},
#     4: {'x': 5, 'y': 7}
# }
# SPIRAL_FREE_LINE = FreeLines(WHITE, spiral)

