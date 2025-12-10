# from Util.constants import Constants
#
# class SlotBitMapper:
#     def __init__(self, width):
#         self.width = width
#         self.bits = []
#         self.sbm_disengaged = []
#         self.sbm_engaged = []
#         self.mapped_slot = []
#         self._build_component()
#
#     def write_input(self, bits):
#         self.bits = bits
#         self._activate_component()
#
#     def read_output(self):
#         return self.mapped_slot
#
#     def get_component_state(self):
#         states = {
#             Constants.DEFAULT: self.sbm_engaged,
#             Constants.ACTIVE: self.sbm_disengaged
#         }
#         return states
#
#     def _build_component(self):
#         for i in range(self.width - 1, -1, -1):
#             mask_group = ([1] * 2 ** i) + ([0] * 2 ** i)
#             mask_group_count = 2 ** (self.width - i - 1)
#
#             mask_groups = []
#             for _i in range(mask_group_count):
#                 mask_groups = mask_groups + mask_group
#
#             self.sbm_disengaged.append(mask_groups)
#
#     def _activate_component(self):
#         for i, layer in enumerate(self.sbm_disengaged):
#             self.sbm_engaged.append(layer[::-1]) if self.bits[i] else self.sbm_engaged.append(layer)
#
#         for branch in zip(*self.sbm_engaged):
#             leaves = 1
#             for leaf in branch:
#                 leaves *= leaf
#
#             self.mapped_slot.append(leaves)