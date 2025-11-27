from Util.constants import Constants

class Instructions:
    assembly = []
    machine = []

    @classmethod
    def populate_instructions_from_file(cls, filepath):
        with open(filepath, 'r', encoding='utf-8') as instructions:
            for instr in instructions:
                if not instr:
                    continue

                instr = instr.strip().upper()
                cls.assembly.append(instr)
                cls.machine.append(cls._asm_to_bin(instr))

    @classmethod
    def _asm_to_bin(cls, asm_instruction):
        bin_sections = []
        for iw in Constants.INSTRUCTION_WIDTHS:
            bin_sections.append([0] * iw)

        asm_sections = asm_instruction.split()
        opcode = asm_sections[0]
        bin_sections[0] = Constants.ASM_TO_BIN[opcode]
        opcode_syntax = Constants.OPCODE_SYNTAX[opcode]

        _asm_index = 1
        for index, valid_syntax in enumerate(opcode_syntax):
            if valid_syntax is None: continue

            asm_value = asm_sections[_asm_index]
            xop_index = index + 1

            if valid_syntax == Constants.NUMERIC:
                _bin_value = bin(int(asm_value))[2:]
                _padding = "0" * (Constants.INSTRUCTION_WIDTHS[xop_index] - len(_bin_value))
                _bin_formatted = _padding + _bin_value
                _bin_numeric = []
                for char in _bin_formatted:
                    _bin_numeric.append(int(char))

                bin_sections[xop_index] = _bin_numeric
            elif asm_value in valid_syntax:
                bin_sections[xop_index] = Constants.ASM_TO_BIN[asm_value]

            _asm_index += 1

        return [x for sub in bin_sections for x in sub]

    @classmethod
    def _get_skeletal_bin_sections(cls, instruction_widths=Constants.INSTRUCTION_WIDTHS):
        skeletal_instruction = []
        for iw in instruction_widths:
            skeletal_instruction.append([0] * iw)
        return skeletal_instruction