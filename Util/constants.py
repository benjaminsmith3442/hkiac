class Constants:
    _ldr = 'LDR'
    _str = 'STR'
    _add = 'ADD'
    _inv = 'INV'
    _mov = 'MOV'
    _uf = 'UF'
    _jmp = 'JMP'
    _io = 'IO'
    _r1 = 'R1'
    _r2 = 'R2'
    _m1 = 'M1'
    _m2 = 'M2'
    _m3 = 'M3'
    _m4 = 'M4'
    _m5 = 'M5'
    _m6 = 'M6'
    _m7 = 'M7'
    _m8 = 'M8'
    _zero = 'ZERO'
    _overflow = 'OVERFLOW'
    _all = 'ALL'
    _in = 'IN'
    _out = 'OUT'
    _valid_register = [_r1, _r2]
    _valid_memory = [_m1, _m2, _m3, _m4]

    INSTRUCTION_COUNT = 16
    OP_CODE_INSTRUCTION_SIZE = 4
    IMMEDIATE_INSTRUCTION_SIZE = 5
    MEMORY_INSTRUCTION_SIZE = 2
    REGISTER_INSTRUCTION_SIZE = 1
    INSTRUCTION_WIDTHS = [
        OP_CODE_INSTRUCTION_SIZE,  # opcode
        MEMORY_INSTRUCTION_SIZE,  # memory
        IMMEDIATE_INSTRUCTION_SIZE,  # immediate
        REGISTER_INSTRUCTION_SIZE   # register
    ]
    NUMERIC = 'NUMERIC'
    OPCODE_SYNTAX = {
        _ldr:   [_valid_memory,     None,               _valid_register],
        _str:   [_valid_memory,     None,               _valid_register],
        _add:   [None,              None,               None],
        _inv:   [None,              None,               None],
        _mov:   [None,              NUMERIC,            None],
        _uf:    [None,              None,               None],
        _jmp:   [None,              NUMERIC,            None],
        _io:    [None,              None,               None]
    }
    ASM_TO_BIN = {
        # Operation Codes
        _ldr:       [0, 0, 1, 0],
        _str:       [0, 1, 0, 0],
        _add:       [0, 1, 1, 0],
        _inv:       [1, 0, 0, 0],
        _mov:       [1, 0, 1, 0],
        _uf:        [1, 1, 0, 0],
        _jmp:       [1, 1, 1, 0],
        _io:        [0, 0, 0, 0],

        # Registers
        _r1:        [0],
        _r2:        [1],

        # Memory
        _m1:        [0, 0],
        _m2:        [0, 1],
        _m3:        [1, 0],
        _m4:        [1, 1]
    }
    # Binary to Int order
    OPCODE_ORDER = {
        _ldr,
        _str,
        _add,
        _inv,
        _mov,
        _uf,
        _jmp,
        _io
    }

    UP = 'u'
    DOWN = 'd'
    LEFT = 'l'
    RIGHT = 'r'


























    # # Flags
    # _zero:      [1, 0],
    # _overflow:  [0, 1],
    # _all:       [1, 1],
    #
    # # Peripherals
    # _out:       [0],
    # _in:        [1]