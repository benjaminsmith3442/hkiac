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
    GREY_DARK, VERY_LIGHT_GREY, GREY_1, lime_green, dark_olive, almost_black
)

#TODO A lot of the exact same method signature. Add inheritance. No rush. Just whenever

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
        self.switch_a = LogicGate.Switch([GREY, BLACK, WHITE], [GREY, BLACK, BLACK], ['NW', 'NW', 'N'])
        self.switch_b = LogicGate.Switch([GREY, BLACK, WHITE], [GREY, BLACK, BLACK], ['NE', 'NE', 'N'])
        self.switch_c = LogicGate.Switch([GREY, BLACK, WHITE], [GREY, BLACK, BLACK], ['S', 'S', 'S'])
        self.label = label
        self.load_as_active()

    def load_as_active(self):
        self.colors = self.active_colors

    def load_as_inactive(self):
        self.colors = self.inactive_colors

class Panel:
    class Title:
        def __init__(self, title_text, title_color):
            self.colors = [BLACK]
            self.offsets = [0]
            self.text = title_text
            self.text_color = title_color

    def __init__(self, colors, title_text, title_color):
        self.colors = colors
        self.offsets = [0, 2, 14, 16]
        self.colors_panel = colors
        self.title = Panel.Title(title_text, title_color)

#TODO   a lot of these probably have static logic that can come from the initializer.
#       Im looking at you Panel objects 0_0
SWITCH              =   SwitchBoard([GREY, BLACK, WHITE], [GREY, BLACK, BLACK])
SWITCH_INACTIVE     =   SwitchBoard([GREY_DARKER, BLACK, WHITE],[GREY_DARKER, BLACK, BLACK])
OPCODE_SWITCH       =   SwitchBoard([ORANGE, BLACK, WHITE],[ORANGE, BLACK, BLACK])
MEMORY_SWITCH       =   SwitchBoard([LIGHT_BLUE, BLACK, WHITE], [LIGHT_BLUE, BLACK, BLACK])
NUMERIC_SWITCH      =   SwitchBoard([GREEN, BLACK, WHITE], [GREEN, BLACK, BLACK])
REGISTER_SWITCH     =   SwitchBoard([RED, BLACK, WHITE], [RED, BLACK, BLACK])
# FLAG_SWITCH         =   SwitchBoard([PURPLE, BLACK, BLACK])
# PERIPHERAL_SWITCH   =   SwitchBoard([ORANGE, BLACK, BLACK])
COUNTER_SWITCH      =   SwitchBoard([GREY, BLACK, WHITE], [GREY, BLACK, BLACK])

NUMERIC_SWITCH_MAPPER   =   SwitchMapper([BLACK, BLACK], [BLACK, GREY_DARK], COUNTER_SWITCH, [BLACK, GREY_DARK, GREY_DARK])

LOGIC_GATE_XOR = LogicGate(WHITE, BLACK,[GREEN, BLACK],[GREY, BLACK],"XOR")
LOGIC_GATE_AND = LogicGate(WHITE, BLACK,[GREEN, BLACK],[GREY, BLACK], "AND")
LOGIC_GATE_OR = LogicGate(WHITE, BLACK, [GREEN, BLACK],[GREY, BLACK], "OR")

ALU_PANEL = Panel([GREEN, BLACK, GREEN, BLACK], 'ARITHMETIC LOGIC UNIT', WHITE)
MEMORY_PANEL = Panel([LIGHT_BLUE, BLACK, LIGHT_BLUE, BLACK], 'MEMORY', WHITE)
REGISTER_PANEL = Panel([RED, BLACK, RED, BLACK], 'REGISTERS', WHITE)
