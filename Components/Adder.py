class Adder:
    def __init__(self):
        self.input = [[],[]]
        self.output = []
        self.inverted = False
        self.carry_in = 0
        self.carry_out = 0

    def read(self):
        return self.output

    def write(self, r1, r2):
        self.input[0] = r1[:]
        self.input[1] = r2[:]

    def execute(self):
        r1 = self.input[0]
        r2 = self.input[1]
        self.output = []

        def _xor(a, b):
            return (a or b) and not (a and b)

        def _full_adder(a, b, cb_in):
            if self.inverted:
                b = not b

            s = _xor(_xor(a, b), cb_in)
            self.carry_out = ((_xor(a, b) * 1) and cb_in) or ((a * 1) and b) * 1

            self.output = [s * 1] + self.output

            if len(r1):
                return _full_adder(r1.pop(), r2.pop(), self.carry_out)

            return None

        _full_adder(r1.pop(), r2.pop(), self.carry_in)

    def invert_adder(self):
        self.inverted = not self.inverted
        self.carry_in = 1 if self.carry_in == 0 else 0
