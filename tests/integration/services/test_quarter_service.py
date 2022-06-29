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
            (
                0, 0, 0, 0,
                [0, 0, 0, 0]
            ),
            (
                1, 0, 0, 0,
                [0x0800_8145, 0x0000_0080, 0x0001_0200, 0x2050_0000]
            ),
            (
                0, 1, 0, 0,
                [0x8800_0100, 0x0000_0001, 0x0000_0200, 0x0040_2000]
            ),
            (
                0, 0, 1, 0,
                [0x8004_0000, 0x0000_0000, 0x0000_0001, 0x0000_2000]
            ),
            (
                0, 0, 0, 1,
                [0x0004_8044, 0x0000_0080, 0x0001_0000, 0x2010_0001]
            ),
            (
                0xe7e8_c006, 0xc4f9_417d, 0x6479_b4b2, 0x68c6_7137,
                [0xe876_d72b, 0x9361_dfd5, 0xf146_0244, 0x9485_41a3]
            ),
            (
                0xd391_7c5b, 0x55f1_c407, 0x52a5_8a7a, 0x8f88_7a3b,
                [0x3e2f_308c, 0xd90a_8f36, 0x6ab2_a923, 0x2883_524c]
            ),
        ]
    )
    def test_quarter_round(
            self,
            y_0: int, y_1: int,
            y_2: int, y_3: int,
            result: list[int]):
        assert self.service.quarter_round(y_0, y_1, y_2, y_3) == result

    @pytest.mark.parametrize(
        "vector, result",
        [
            (
                [
                    0x00000001, 0x00000000, 0x00000000, 0x00000000,
                    0x00000001, 0x00000000, 0x00000000, 0x00000000,
                    0x00000001, 0x00000000, 0x00000000, 0x00000000,
                    0x00000001, 0x00000000, 0x00000000, 0x00000000,
                ],
                [
                    0x08008145, 0x00000080, 0x00010200, 0x20500000,
                    0x20100001, 0x00048044, 0x00000080, 0x00010000,
                    0x00000001, 0x00002000, 0x80040000, 0x00000000,
                    0x00000001, 0x00000200, 0x00402000, 0x88000100,
                ]
            ),
            (
                [
                    0x08521bd6, 0x1fe88837, 0xbb2aa576, 0x3aa26365,
                    0xc54c6a5b, 0x2fc74c2f, 0x6dd39cc3, 0xda0a64f6,
                    0x90a2f23d, 0x067f95a6, 0x06b35f61, 0x41e4732e,
                    0xe859c100, 0xea4d84b7, 0x0f619bff, 0xbc6e965a
                ],
                [
                    0xa890d39d, 0x65d71596, 0xe9487daa, 0xc8ca6a86,
                    0x949d2192, 0x764b7754, 0xe408d9b9, 0x7a41b4d1,
                    0x3402e183, 0x3c3af432, 0x50669f96, 0xd89ef0a8,
                    0x0040ede5, 0xb545fbce, 0xd257ed4f, 0x1818882d
                ],
            )
        ]
    )
    def test_row_round(self, vector: list[int], result: list[int]):
        assert self.service.row_round(vector) == result

    @pytest.mark.parametrize(
        "vector, result",
        [
            (
                [
                    0x00000001, 0x00000000, 0x00000000, 0x00000000,
                    0x00000001, 0x00000000, 0x00000000, 0x00000000,
                    0x00000001, 0x00000000, 0x00000000, 0x00000000,
                    0x00000001, 0x00000000, 0x00000000, 0x00000000,
                ],
                [
                    0x10090288, 0x00000000, 0x00000000, 0x00000000,
                    0x00000101, 0x00000000, 0x00000000, 0x00000000,
                    0x00020401, 0x00000000, 0x00000000, 0x00000000,
                    0x40a04001, 0x00000000, 0x00000000, 0x00000000,
                ]
            ),
            (
                [
                    0x08521bd6, 0x1fe88837, 0xbb2aa576, 0x3aa26365,
                    0xc54c6a5b, 0x2fc74c2f, 0x6dd39cc3, 0xda0a64f6,
                    0x90a2f23d, 0x067f95a6, 0x06b35f61, 0x41e4732e,
                    0xe859c100, 0xea4d84b7, 0x0f619bff, 0xbc6e965a,
                ],
                [
                    0x8c9d190a, 0xce8e4c90, 0x1ef8e9d3, 0x1326a71a,
                    0x90a20123, 0xead3c4f3, 0x63a091a0, 0xf0708d69,
                    0x789b010c, 0xd195a681, 0xeb7d5504, 0xa774135c,
                    0x481c2027, 0x53a8e4b5, 0x4c1f89c5, 0x3f78c9c8,
                ],
            )
        ]
    )
    def test_column_round(self, vector: list[int], result: list[int]):
        assert self.service.column_round(vector) == result
