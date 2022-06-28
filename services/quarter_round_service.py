from .bit_service import BitService


class QuarterRoundService:
    def __init__(self, bit_service: BitService):
        self.bit_service = bit_service

    def do(self, y_0: int, y_1: int, y_2: int, y_3: int) -> list[int]:
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
