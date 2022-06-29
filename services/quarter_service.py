from .bit_service import BitService


class QuarterService:
    def __init__(self, bit_service: BitService):
        self.bit_service = bit_service

    def double_round(self, matrix: list[list[int]]) -> list[list[int]]:
        return self.row_round(self.column_round(matrix))

    def row_round(self, vector: list[int]) -> list[int]:
        v = vector

        z_0, z_1, z_2, z_3 = self.quarter_round(v[0], v[1], v[2], v[3])
        z_5, z_6, z_7, z_4 = self.quarter_round(v[5], v[6], v[7], v[4])
        z_10, z_11, z_8, z_9 = self.quarter_round(v[10], v[11], v[8], v[9])
        z_15, z_12, z_13, z_14 = self.quarter_round(v[15], v[12], v[13], v[14])

        return [
            z_0, z_1, z_2, z_3,
            z_4, z_5, z_6, z_7,
            z_8, z_9, z_10, z_11,
            z_12, z_13, z_14, z_15
        ]

    def column_round(self, vector: list[int]) -> list[int]:
        v = vector
        y_0, y_4, y_8, y_12 = self.quarter_round(v[0], v[4], v[8], v[12])
        y_5, y_9, y_13, y_1 = self.quarter_round(v[5], v[9], v[13], v[1])
        y_10, y_14, y_2, y_6 = self.quarter_round(v[10], v[14], v[2], v[6])
        y_15, y_3, y_7, y_11 = self.quarter_round(v[15], v[3], v[7], v[11])
        return [
            y_0, y_1, y_2, y_3,
            y_4, y_5, y_6, y_7,
            y_8, y_9, y_10, y_11,
            y_12, y_13, y_14, y_15
        ]

    def quarter_round(self, y_0: int, y_1: int, y_2: int, y_3: int) -> list[int]:
        z_1 = self._compute_common_z(y_1, y_0, y_3, 7)
        z_2 = self._compute_common_z(y_2, z_1, y_0, 9)
        z_3 = self._compute_common_z(y_3, z_2, z_1, 13)
        z_0 = self._compute_common_z(y_0, z_3, z_2, 18)
        return [z_0, z_1, z_2, z_3]

    def _compute_common_z(
            self,
            xor_addend: int,
            mod_addend: int,
            mod_augend: int,
            shift: int) -> int:
        mod_sum = self.bit_service.mod_sum(mod_addend, mod_augend)
        xor_augend = self.bit_service.cycle_left_shift(mod_sum, shift)
        z = self.bit_service.mod_xor(xor_addend, xor_augend)
        return z
