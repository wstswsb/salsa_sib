from .bit_service import BitService


class QuarterService:
    def __init__(self, bit_service: BitService):
        self.bit_service = bit_service

    def double_round(self, matrix: list[list[int]]) -> list[list[int]]:
        return self.row_round(self.column_round(matrix))

    def row_round(self, matrix: list[list[int]]) -> list[list[int]]:
        return [
            self.quarter_round(*line)
            for line
            in matrix
        ]

    def column_round(self, matrix: list[list[int]]) -> list[list[int]]:
        return [
            self.quarter_round(
                matrix[0][i],
                matrix[1][i],
                matrix[2][i],
                matrix[3][i],
            )
            for i in range(len(matrix))
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
