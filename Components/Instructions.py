from Util.constants import Constants

class Instructions:
    def __init__(self):
        pass

    def write_input(self):
        pass

    def read_output(self):
        pass

    def get_component_input(self):
        pass

    def get_component_states(self):
        states = {
            Constants.DEFAULT: "",
            Constants.ACTIVE: ""
        }
        return states

    def get_component_active_state(self):
        pass

    def _build_default_state(self):
        pass

    def _activate_component(self):
        pass

    def _write_output(self):
        pass