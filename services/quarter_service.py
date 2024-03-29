from .bit_service import BitService


class QuarterService:
    def __init__(self, bit_service: BitService):
        self.bit_service = bit_service

    def double_round(self, matrix: list[list[int]], reverse=False) -> list[list[int]]:
        if reverse:
            return self.column_round(self.row_round(matrix, reverse), reverse)
        return self.row_round(self.column_round(matrix, reverse))

    def row_round(self, matrix: list[list[int]], reverse=False) -> list[list[int]]:
        func = self.quarter_round
        if reverse:
            func = self.reversed_quarter_round
        m = matrix
        z_00, z_01, z_02, z_03 = func(*m[0])
        z_11, z_12, z_13, z_10 = func(
            m[1][1], m[1][2],
            m[1][3], m[1][0],
        )
        z_22, z_23, z_20, z_21 = func(
            m[2][2], m[2][3],
            m[2][0], m[2][1],
        )
        z_33, z_30, z_31, z_32 = func(
            m[3][3], m[3][0],
            m[3][1], m[3][2],
        )
        return [
            [z_00, z_01, z_02, z_03],
            [z_10, z_11, z_12, z_13],
            [z_20, z_21, z_22, z_23],
            [z_30, z_31, z_32, z_33],
        ]

    def column_round(self, matrix: list[list[int]], reverse=False) -> list[list[int]]:
        func = self.quarter_round
        if reverse:
            func = self.reversed_quarter_round
        m = matrix
        y_00, y_10, y_20, y_30 = func(
            m[0][0], m[1][0],
            m[2][0], m[3][0],
        )
        y_11, y_21, y_31, y_01 = func(
            m[1][1], m[2][1],
            m[3][1], m[0][1],
        )
        y_22, y_32, y_02, y_12 = func(
            m[2][2], m[3][2],
            m[0][2], m[1][2],
        )
        y_33, y_03, y_13, y_23 = func(
            m[3][3], m[0][3],
            m[1][3], m[2][3],
        )
        return [
            [y_00, y_01, y_02, y_03],
            [y_10, y_11, y_12, y_13],
            [y_20, y_21, y_22, y_23],
            [y_30, y_31, y_32, y_33],
        ]

    def quarter_round(self, y_0: int, y_1: int, y_2: int, y_3: int) -> list[int]:
        z_1 = self._compute_common_quarter_value(y_1, y_0, y_3, 7)
        z_2 = self._compute_common_quarter_value(y_2, z_1, y_0, 9)
        z_3 = self._compute_common_quarter_value(y_3, z_2, z_1, 13)
        z_0 = self._compute_common_quarter_value(y_0, z_3, z_2, 18)
        return [z_0, z_1, z_2, z_3]

    def reversed_quarter_round(
            self, z_0: int, z_1: int,
            z_2: int, z_3: int) -> list[int]:
        y_0 = self._compute_common_quarter_value(z_0, z_2, z_3, 18)
        y_3 = self._compute_common_quarter_value(z_3, z_1, z_2, 13)
        y_2 = self._compute_common_quarter_value(z_2, y_0, z_1, 9)
        y_1 = self._compute_common_quarter_value(z_1, y_0, y_3, 7)
        return [y_0, y_1, y_2, y_3]

    def _quarter_matrix(self, matrix: list[list[int]]) -> list[list[int]]:
        result = []
        for i, line in enumerate(matrix):
            quartered_line = self.quarter_round(*(line[i:] + line[:i]))
            result.append(quartered_line[-i:] + quartered_line[:-i])
        return result

    def _compute_common_quarter_value(
            self,
            xor_addend: int,
            mod_addend: int,
            mod_augend: int,
            shift: int) -> int:
        mod_sum = self.bit_service.mod_sum(mod_addend, mod_augend)
        xor_augend = self.bit_service.cycle_left_shift(mod_sum, shift)
        z = self.bit_service.mod_xor(xor_addend, xor_augend)
        return z
