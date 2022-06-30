import pytest
from services import BitService


class TestBitService:
    def setup(self):
        self.service = BitService(
            operations_mask=0xFFFF_FFFF,
            operations_bit_size=32,
        )

    @pytest.mark.parametrize(
        "y, shift, result",
        [
            (0xFFFF_0000, 16, 0x0000_FFFF),
            (0xFFFF_0000, 8, 0xFF00_00FF),
            (0xFFFF_0000, 4, 0xFFF0_000F),
            (0x00FF_0000, 4, 0x0FF0_0000),
        ]
    )
    def test_cycle_four_byte_shift(self, y: int, shift: int, result: int):
        assert self.service.cycle_left_shift(y, shift) == result

    @pytest.mark.parametrize(
        "addend, augend, result",
        [
            (0xFFFF_FFFF, 1, 0),
            (0xFFFF_FFFF, 2, 1),
            (0xFFFF_0000, 0x0000_FFFF, 0xFFFF_FFFF),
        ]
    )
    def test_mod_sum(self, addend: int, augend: int, result: int):
        assert self.service.mod_sum(addend, augend) == result

    @pytest.mark.parametrize(
        "addend, augend, result",
        [
            (0xFFFF_FFFF, 0xFFFF_FFFF_FFFF, 0),
            (0xFFFF_FFFF, 2, 0xFFFF_FFFD),
        ]
    )
    def test_mod_xor(self, addend: int, augend: int, result: int):
        assert self.service.mod_xor(addend, augend) == result
