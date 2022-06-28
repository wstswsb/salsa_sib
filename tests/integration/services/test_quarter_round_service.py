import pytest
from services import QuarterRoundService, BitService


class TestQuarterRoundService:
    def setup(self):
        self.bit_service = BitService(
            block_mask=0xFFFF_FFFF,
            block_bit_size=32,
        )
        self.service = QuarterRoundService(self.bit_service)

    @pytest.mark.parametrize(
        "y_0, y_1, y_2, y_3, result",
        [
            (1, 0, 0, 0, [0x0800_8145, 0x0000_0080, 0x0001_0200, 0x2050_0000])
        ]
    )
    def test_do(
            self,
            y_0: int, y_1: int,
            y_2: int, y_3: int,
            result: list[int]):
        assert self.service.do(y_0, y_1, y_2, y_3) == result
