import pytest
from services import QuarterService, BitService


class TestQuarterService:
    def setup(self):
        self.bit_service = BitService(
            operations_mask=0xFFFF_FFFF,
            operations_bit_size=32,
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
        assert self.service.reversed_quarter_round(*result) == [y_0, y_1, y_2, y_3]

    @pytest.mark.parametrize(
        "matrix, result",
        [
            (
                [
                    [0x00000001, 0x00000000, 0x00000000, 0x00000000],
                    [0x00000001, 0x00000000, 0x00000000, 0x00000000],
                    [0x00000001, 0x00000000, 0x00000000, 0x00000000],
                    [0x00000001, 0x00000000, 0x00000000, 0x00000000],
                ],
                [
                    [0x08008145, 0x00000080, 0x00010200, 0x20500000],
                    [0x20100001, 0x00048044, 0x00000080, 0x00010000],
                    [0x00000001, 0x00002000, 0x80040000, 0x00000000],
                    [0x00000001, 0x00000200, 0x00402000, 0x88000100],
                ]
            ),
            (
                [
                    [0x08521bd6, 0x1fe88837, 0xbb2aa576, 0x3aa26365],
                    [0xc54c6a5b, 0x2fc74c2f, 0x6dd39cc3, 0xda0a64f6],
                    [0x90a2f23d, 0x067f95a6, 0x06b35f61, 0x41e4732e],
                    [0xe859c100, 0xea4d84b7, 0x0f619bff, 0xbc6e965a],
                ],
                [
                    [0xa890d39d, 0x65d71596, 0xe9487daa, 0xc8ca6a86],
                    [0x949d2192, 0x764b7754, 0xe408d9b9, 0x7a41b4d1],
                    [0x3402e183, 0x3c3af432, 0x50669f96, 0xd89ef0a8],
                    [0x0040ede5, 0xb545fbce, 0xd257ed4f, 0x1818882d],
                ],
            )
        ]
    )
    def test_row_round(self, matrix, result):
        assert self.service.row_round(matrix) == result
        assert self.service.row_round(result, reverse=True) == matrix

    @pytest.mark.parametrize(
        "matrix, result",
        [
            (
                [
                    [0x0000_0001, 0x0000_0000, 0x0000_0000, 0x0000_0000],
                    [0x0000_0001, 0x0000_0000, 0x0000_0000, 0x0000_0000],
                    [0x0000_0001, 0x0000_0000, 0x0000_0000, 0x0000_0000],
                    [0x0000_0001, 0x0000_0000, 0x0000_0000, 0x0000_0000],
                ],
                [
                    [0x1009_0288, 0x0000_0000, 0x0000_0000, 0x0000_0000],
                    [0x0000_0101, 0x0000_0000, 0x0000_0000, 0x0000_0000],
                    [0x0002_0401, 0x0000_0000, 0x0000_0000, 0x0000_0000],
                    [0x40a0_4001, 0x0000_0000, 0x0000_0000, 0x0000_0000],
                ]
            ),
            (
                [
                    [0x0852_1bd6, 0x1fe8_8837, 0xbb2a_a576, 0x3aa2_6365],
                    [0xc54c_6a5b, 0x2fc7_4c2f, 0x6dd3_9cc3, 0xda0a_64f6],
                    [0x90a2_f23d, 0x067f_95a6, 0x06b3_5f61, 0x41e4_732e],
                    [0xe859_c100, 0xea4d_84b7, 0x0f61_9bff, 0xbc6e_965a],
                ],
                [
                    [0x8c9d_190a, 0xce8e_4c90, 0x1ef8_e9d3, 0x1326_a71a],
                    [0x90a2_0123, 0xead3_c4f3, 0x63a0_91a0, 0xf070_8d69],
                    [0x789b_010c, 0xd195_a681, 0xeb7d_5504, 0xa774_135c],
                    [0x481c_2027, 0x53a8_e4b5, 0x4c1f_89c5, 0x3f78_c9c8],
                ],
            )
        ]
    )
    def test_column_round(self, matrix, result):
        assert self.service.column_round(matrix) == result
        assert self.service.column_round(result, reverse=True) == matrix

    @pytest.mark.parametrize(
        "matrix, result",
        [
            (
                [
                    [0x0000_0001, 0x0000_0000, 0x0000_0000, 0x0000_0000],
                    [0x0000_0000, 0x0000_0000, 0x0000_0000, 0x0000_0000],
                    [0x0000_0000, 0x0000_0000, 0x0000_0000, 0x0000_0000],
                    [0x0000_0000, 0x0000_0000, 0x0000_0000, 0x0000_0000],
                ],
                [
                    [0x8186_a22d, 0x0040_a284, 0x8247_9210, 0x0692_9051],
                    [0x0800_0090, 0x0240_2200, 0x0000_4000, 0x0080_0000],
                    [0x0001_0200, 0x2040_0000, 0x0800_8104, 0x0000_0000],
                    [0x2050_0000, 0xa000_0040, 0x0008_180a, 0x612a_8020]
                ]
            ),
            (
                [
                    [0xde50_1066, 0x6f9e_b8f7, 0xe4fb_bd9b, 0x454e_3f57],
                    [0xb755_40d3, 0x43e9_3a4c, 0x3a6f_2aa0, 0x726d_6b36],
                    [0x9243_f484, 0x9145_d1e8, 0x4fa9_d247, 0xdc8d_ee11],
                    [0x054b_f545, 0x254d_d653, 0xd942_1b6d, 0x67b2_76c1]
                ],
                [
                    [0xccaa_f672, 0x23d9_60f7, 0x9153_e63a, 0xcd9a_60d0],
                    [0x5044_0492, 0xf07c_ad19, 0xae34_4aa0, 0xdf4c_fdfc],
                    [0xca53_1c29, 0x8e79_43db, 0xac16_80cd, 0xd503_ca00],
                    [0xa74b_2ad6, 0xbc33_1c5c, 0x1dda_24c7, 0xee92_8277]
                ],
            )
        ]
    )
    def test_double_round(self, matrix, result):
        assert self.service.double_round(matrix) == result
