from View.Palette import *

class SnapObject:
    def __init__(self, offsets=None, colors=None, alignments=None, inactive_colors=None):
        self.offsets = offsets
        self.colors = colors
        self.alignments = alignments or [''] * len(offsets)
        self.active_colors = colors
        self.inactive_colors = inactive_colors

    def load_as_active(self):
        self.colors = self.active_colors
    def load_as_inactive(self):
        self.colors = self.inactive_colors


class FreeLines:
    class InnerLine(SnapObject):
        def __init__(self, color):
            super().__init__([7], [color])

    class OuterLine(SnapObject):
        def __init__(self):
            super().__init__([0], [BLACK])

    def __init__(self, color):
        self.inner_line = FreeLines.InnerLine(color)
        self.outer_line = FreeLines.OuterLine()


class SwitchBoard(SnapObject):
    def __init__(self, colors, inactive_colors):
        super().__init__(
            offsets=[0, 4, 9],
            colors=colors,
            inactive_colors=inactive_colors
        )
        self.load_as_active()


class SwitchMapper(SnapObject):
    class MapperSelector(SnapObject):
        def __init__(self, colors, alignments):
            super().__init__(
                offsets=[0, 4, 10],
                colors=colors,
                alignments=alignments
            )

    def __init__(self, colors, inactive_colors, switch_board_input, selector):
        super().__init__(
            offsets=[0, 9],
            colors=colors,
            inactive_colors=inactive_colors
        )
        self.switch_board_input = switch_board_input
        self.mapper_selector_none = SwitchBoard(selector, selector)
        self.selector = {
            'left': SwitchMapper.MapperSelector(selector[:2] + [WHITE], ['E'] * 3),
            'right': SwitchMapper.MapperSelector(selector[:1] + [BLACK, WHITE], ['W'] * 3)
        }
        self.load_as_active()


class LogicGate(SnapObject): #TODO you also left off here. Keep going champion
    class GateSwitch(SnapObject):
        def __init__(self, alignments):
            super().__init__([0, 7, 7], colors=[GREY_DARK, BLACK, WHITE], inactive_colors=[GREY_DARK, BLACK, BLACK], alignments=alignments)
            self.load_as_inactive()

    def __init__(self):
        super().__init__([0, 7], [GREY_DARK, BLACK])
        self.input_a = None
        self.input_b = None
        self.output = None
        self.label_color = GREY_LIGHT
        self.label = ""
        self.has_single_input = None

    def set_as_not(self):
        self.input_a = LogicGate.GateSwitch(['N', 'N', 'N'])
        self.output = LogicGate.GateSwitch(['E', 'E', 'E'])
        self.label = "NOT"
        self.has_single_input = True
        return self

    def _build_double_input(self, label):
        self.input_a = LogicGate.GateSwitch(['', 'NW', ''])
        self.input_b = LogicGate.GateSwitch(['', 'NE', ''])
        self.output = LogicGate.GateSwitch(['E', 'E', 'E'])
        self.label = label
        self.has_single_input = False

    def set_as_or(self):
        self._build_double_input("OR")
        return self

    def set_as_and(self):
        self._build_double_input("AND")
        return self

    def set_as_xor(self):
        self._build_double_input("XOR")
        return self


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
REGISTER_AB_SWITCH  =   SwitchBoard([TEST_RED, BLACK, WHITE], [TEST_RED, BLACK, BLACK])
REGISTER_C_SWITCH   =   SwitchBoard([ORANGE, BLACK, WHITE], [ORANGE, BLACK, BLACK])
FLAG_SWITCH         =   SwitchBoard([ORANGE, BLACK, WHITE], [ORANGE, BLACK, BLACK])
# PERIPHERAL_SWITCH   =   SwitchBoard([ORANGE, BLACK, BLACK])
COUNTER_SWITCH      =   SwitchBoard([GREEN, BLACK, WHITE], [GREEN, BLACK, BLACK])
CARRY_SWITCH        =   SwitchBoard([PURPLE, BLACK, WHITE], [PURPLE, BLACK, BLACK])

INSTRUCTION_SWITCH_MAPPER   =   SwitchMapper([BLACK, BLACK], [BLACK, WHITE], COUNTER_SWITCH, [BLACK, GREY_DARK, GREY_DARK])
MEMORY_SWITCH_MAPPER        =   SwitchMapper([BLACK, BLACK], [BLACK, BLUE], MEMORY_SWITCH, [BLACK, GREY_DARK, GREY_DARK])
REGISTER_SWITCH_MAPPER      =   SwitchMapper([BLACK, BLACK], [BLACK, RED], COUNTER_SWITCH, [BLACK, GREY_DARK, GREY_DARK])
OPCODE_SWITCH_MAPPER        =   SwitchMapper([BLACK, BLACK], [BLACK, GREEN], OPCODE_SWITCH, [BLACK, GREY_DARK, GREY_DARK])

LOGIC_GATE_XOR  =   LogicGate().set_as_xor()
LOGIC_GATE_AND  =   LogicGate().set_as_and()
LOGIC_GATE_OR   =   LogicGate().set_as_or()
LOGIC_GATE_NOT  =   LogicGate().set_as_not()

ALU_PANEL           =   Panel([GREY_LIGHT, BLACK, GREY_LIGHT, BLACK], 'ARITHMETIC LOGIC UNIT', WHITE)
MEMORY_PANEL        =   Panel([BLUE, BLACK, BLUE, BLACK], 'MEMORY', LIGHT_BLUE)
REGISTER_PANEL      =   Panel([RED, BLACK, RED, BLACK], 'REGISTERS', TEST_RED)
HKIAC_PANEL         =   Panel([WHITE, BLACK, WHITE, BLACK], None, None)
FLAG_PANEL          =   Panel([GREY_LIGHT, BLACK, GREY_LIGHT, BLACK], 'FLAGS', "violet")
INSTRUCTION_PANEL   =   Panel([GREY_LIGHT, BLACK, GREY_LIGHT, BLACK], 'MACHINE INSTRUCTIONS', WHITE)
OPCODE_PANEL        =   Panel([GREEN, BLACK, GREEN, BLACK], 'CONTROL UNIT', "lime")
BLACKOUT            =   Panel([BLACK, BLACK, BLACK, BLACK], None, None)
IO_PANEL            =   Panel([BLACK, GREY_DARK, GREY_DARK, GREY_DARK], None, None)

# TODO i think separating coordinates to the main file is good. This class should only describe object properties. Not their 'moldable' layout

CARRY_IN_FREELINE = FreeLines(PURPLE)
INPUT_A_FREELINE = FreeLines(TEST_RED)
INPUT_B_FREELINE = FreeLines(TEST_RED)

