from Util.constants import Constants

class FlagRegisters:
    def __init__(self):
        self.bits = []
        self.sbm_disengaged = []
        self.sbm_engaged = []
        self.mapped_slot = []
        self._build_component()

    def write_input(self, bits):
        self.bits = bits

    def read_output(self):
        return self.mapped_slot

    def configure_component(self):
        pass

    def get_component_state(self):
        pass

    def _build_component(self):
        pass

    def _activate_component(self):
        pass