import pytest
from services import QuarterService, BitService


class TestQuarterService:
    def setup(self):
        self.bit_service = BitService(
            block_mask=0xFFFF_FFFF,
            block_bit_size=32,
        )
        self.service = QuarterService(self.bit_service)

    @pytest.mark.parametrize(
        "y_0, y_1, y_2, y_3, result",
        [
            (1, 0, 0, 0, [0x0800_8145, 0x0000_0080, 0x0001_0200, 0x2050_0000])
        ]
    )
    def test_quarter_round(
            self,
            y_0: int, y_1: int,
            y_2: int, y_3: int,
            result: list[int]):
        assert self.service.quarter_round(y_0, y_1, y_2, y_3) == result
