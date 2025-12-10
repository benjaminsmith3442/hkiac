from View.Palette import *

class _SnapObject:
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
    class InnerLine(_SnapObject):
        def __init__(self, color):
            super().__init__([7], [color])

    class OuterLine(_SnapObject):
        def __init__(self):
            super().__init__([0], [BLACK])

    def __init__(self, color):
        self.inner_line = FreeLines.InnerLine(color)
        self.outer_line = FreeLines.OuterLine()


class SwitchBoard(_SnapObject):
    def __init__(self, color):
        super().__init__(
            offsets=[0, 4, 9],
            colors=[color, BLACK, WHITE],
            inactive_colors=[color, BLACK, BLACK]
        )
        self.load_as_active()


class Selector(_SnapObject):
    class HalfSelector(_SnapObject):
        def __init__(self, colors, alignments):
            super().__init__(
                offsets=[0, 4, 10],
                colors=colors,
                alignments=alignments
            )

    def __init__(self, background_color=BLACK, switch_color=GREY_DARK, prong_color=WHITE):
        super().__init__(
            offsets=[0, 4, 9],
            colors=[background_color, switch_color, switch_color]
        )

        self.__first_half_colors = [background_color, switch_color, prong_color]
        self.__second_half_colors = [background_color, background_color, prong_color]
        self.selector = {}
        self.next_x = 0
        self.next_y = 0

    def _define_halves(self, first_half, second_half):
        self.selector['first_rectangle'] = Selector.HalfSelector(self.__first_half_colors, [first_half, '', first_half])
        self.selector['second_rectangle'] = Selector.HalfSelector(self.__second_half_colors, [second_half] * 3)

    def aim_down(self):
        self._define_halves('S', 'N')
        self.next_y = 1
        return self

    def aim_up(self):
        self._define_halves('N', 'S')
        self.next_y = -1
        return self

    def aim_right(self):
        self._define_halves('E', 'W')
        self.next_x = 1
        return self

    def aim_left(self):
        self._define_halves('W', 'E')
        self.next_x = -1
        return self

    def load_as_active(self): pass
    def load_as_inactive(self): pass


class SwitchMapper(_SnapObject):
    def __init__(self, color, switch_board_input):
        super().__init__(
            offsets=[0, 9],
            colors=[BLACK, BLACK],
            inactive_colors=[BLACK, color]
        )
        self.switch_board_input = switch_board_input
        self.selector = Selector().aim_right()
        self.load_as_active()


class LogicGate(_SnapObject):
    class GateSwitch(_SnapObject):
        def __init__(self, alignments):
            super().__init__(
                [0, 7, 7],
                colors=[GREY_DARK, BLACK, WHITE],
                inactive_colors=[GREY_DARK, BLACK, BLACK],
                alignments=alignments
            )
            self.load_as_inactive()

    def __init__(self):
        super().__init__(
            [0, 7],
            [GREY_DARK, BLACK]
        )
        self.input_a = None
        self.input_b = None
        self.output = None
        self.label_color = GREY_LIGHT
        self.label = ""
        self.has_single_input = None

    def set_as_not(self):
        self.input_a = LogicGate.GateSwitch(['', 'N', ''])
        self.output = LogicGate.GateSwitch(['', 'S', ''])
        self.label = "NOT"
        self.has_single_input = True
        return self

    def _build_double_input(self, label):
        self.input_a = LogicGate.GateSwitch(['', 'NW', ''])
        self.input_b = LogicGate.GateSwitch(['', 'NE', ''])
        self.output = LogicGate.GateSwitch(['', 'S', ''])
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


class Panel(_SnapObject):
    def __init__(self, color=GREY, title_text=None, title_color=WHITE):
        offsets = [0] if title_text is None else [0, 2, 14, 16]
        colors = [color] if title_text is None else [color, BLACK, color, BLACK]

        super().__init__(
            offsets=offsets,
            colors=colors
        )

        self.text = title_text
        self.text_color = title_color


SWITCH              =   SwitchBoard(GREY)
SWITCH_INACTIVE     =   SwitchBoard(GREY_DARKER)
OPCODE_SWITCH       =   SwitchBoard(WHITE)
JUMP_SWITCH         =   SwitchBoard(GREEN)
MEMORY_SWITCH       =   SwitchBoard(TEAL)
INPUT_SWITCH        =   SwitchBoard(TEAL)
NUMERIC_SWITCH      =   SwitchBoard(GREY_LIGHTER)
REGISTER_AB_SWITCH  =   SwitchBoard(RED)
REGISTER_C_SWITCH   =   SwitchBoard(ORANGE)
FLAG_SWITCH         =   SwitchBoard(ORANGE)
COUNTER_SWITCH      =   SwitchBoard(GREEN)
CARRY_SWITCH        =   SwitchBoard(PURPLE)
ZERO_SWITCH         =   SwitchBoard(BLUE)

INSTRUCTION_SWITCH_MAPPER   =   SwitchMapper(GREEN, COUNTER_SWITCH)
MEMORY_SWITCH_MAPPER        =   SwitchMapper(TEAL, MEMORY_SWITCH)
REGISTER_SWITCH_MAPPER      =   SwitchMapper(RED, REGISTER_AB_SWITCH)

LOGIC_GATE_XOR  =   LogicGate().set_as_xor()
LOGIC_GATE_AND  =   LogicGate().set_as_and()
LOGIC_GATE_OR   =   LogicGate().set_as_or()
LOGIC_GATE_NOT  =   LogicGate().set_as_not()

INPUT_PRONG     =   Selector(GREY_DARKISH, TEAL, LIGHT_BLUE).aim_down()
OUTPUT_PRONG    =   Selector(GREY_DARKISH, ORANGE, YELLOW).aim_up()

ALU_PANEL           =   Panel(title_text='A. L. U.')
MEMORY_PANEL        =   Panel(title_text='M E M O R Y')
REGISTER_PANEL      =   Panel(title_text='R E G I S T E R S')
FLAG_PANEL          =   Panel(title_text='F L A G S')
INSTRUCTION_PANEL   =   Panel(title_text='I N S T R U C T I O N S')
BLACKOUT            =   Panel(color=BLACK)
GREY_PANEL          =   Panel(color=GREY_DARKISH)

CARRY_IN_FREELINE = FreeLines(PURPLE)
INPUT_A_FREELINE = FreeLines(RED)
INPUT_B_FREELINE = FreeLines(RED)
REGISTER_2_FREELINE = FreeLines(ORANGE)
ZERO_FLAG_FREELINE = FreeLines(BLUE)
CARRY_FLAG_FREELINE = FreeLines(PURPLE)
