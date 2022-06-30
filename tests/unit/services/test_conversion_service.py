import pytest
from services import ConversionService


class TestConversionService:
    def setup(self):
        self.service = ConversionService()

    @pytest.mark.parametrize(
        "sequence, result",
        [
            (bytes.fromhex("00 00 00 00"), 0x0000_0000),
            (bytes.fromhex("56 4b 1e 09"), 0x091e_4b56),
            (bytes.fromhex("ff ff ff fa"), 0xfaff_ffff),
        ]
    )
    def test_bytes_to_int_little_endian(self, sequence: bytes, result: int):
        assert self.service.bytes_to_int_little_endian(sequence) == result

    @pytest.mark.parametrize(
        "item, result",
        [
            (0x0000_0000, bytes.fromhex("00 00 00 00")),
            (0x091e_4b56, bytes.fromhex("56 4b 1e 09")),
            (0xfaff_ffff, bytes.fromhex("ff ff ff fa")),
        ]
    )
    def test_int_to_bytes_from_little_endian(self, item: int, result: bytes):
        assert self.service.int_to_bytes_from_little_endian(item) == result

    @pytest.mark.parametrize(
        "sequence, result",
        [
            (
                bytes(
                    [
                        88, 118, 104, 54, 79, 201, 235, 79,
                        3, 81, 156, 47, 203, 26, 244, 243,
                        191, 187, 234, 136, 211, 159, 13, 115,
                        76, 55, 82, 183, 3, 117, 222, 37,
                        86, 16, 179, 207, 49, 237, 179, 48,
                        1, 106, 178, 219, 175, 199, 166, 48,
                        238, 55, 204, 36, 31, 240, 32, 63,
                        15, 83, 93, 161, 116, 147, 48, 113
                    ]
                ),
                [
                    912815704, 1340852559, 798773507, 4092861131,
                    2297084863, 1930272723, 3075618636, 635335939,
                    3484618838, 817098033, 3685902849, 816236463,
                    617363438, 1059123231, 2707247887, 1899008884
                ]
            )
        ]
    )
    def test_bytes_to_ints(self, sequence: bytes, result: list[int]):
        assert self.service.bytes_to_ints(sequence) == result

    @pytest.mark.parametrize(
        "sequence, result",
        [
            (
                [
                    912815704, 1340852559, 798773507, 4092861131,
                    2297084863, 1930272723, 3075618636, 635335939,
                    3484618838, 817098033, 3685902849, 816236463,
                    617363438, 1059123231, 2707247887, 1899008884
                ],
                bytes(
                    [
                        88, 118, 104, 54, 79, 201, 235, 79,
                        3, 81, 156, 47, 203, 26, 244, 243,
                        191, 187, 234, 136, 211, 159, 13, 115,
                        76, 55, 82, 183, 3, 117, 222, 37,
                        86, 16, 179, 207, 49, 237, 179, 48,
                        1, 106, 178, 219, 175, 199, 166, 48,
                        238, 55, 204, 36, 31, 240, 32, 63,
                        15, 83, 93, 161, 116, 147, 48, 113
                    ]
                ),
            )
        ]
    )
    def test_ints_to_bytes(self, sequence: list[int], result: bytes):
        assert self.service.ints_to_bytes(sequence) == result

    def test_ints_to_matrix(self):
        sequence = [
            0, 1, 2, 3,
            4, 5, 6, 7,
            8, 9, 10, 11,
            12, 13, 14, 15,
        ]
        expected = [
            [0, 1, 2, 3],
            [4, 5, 6, 7],
            [8, 9, 10, 11],
            [12, 13, 14, 15]
        ]
        assert self.service.ints_to_matrix(sequence) == expected

    def test_matrix_to_ints(self):
        matrix = [
            [0, 1, 2, 3],
            [4, 5, 6, 7],
            [8, 9, 10, 11],
            [12, 13, 14, 15]
        ]
        expected = [
            0, 1, 2, 3,
            4, 5, 6, 7,
            8, 9, 10, 11,
            12, 13, 14, 15,
        ]
        assert self.service.matrix_to_ints(matrix) == expected

    def test_bytes_to_matrix(self):
        sequence = bytes([
            88, 118, 104, 54, 79, 201, 235, 79,
            3, 81, 156, 47, 203, 26, 244, 243,
            191, 187, 234, 136, 211, 159, 13, 115,
            76, 55, 82, 183, 3, 117, 222, 37,
            86, 16, 179, 207, 49, 237, 179, 48,
            1, 106, 178, 219, 175, 199, 166, 48,
            238, 55, 204, 36, 31, 240, 32, 63,
            15, 83, 93, 161, 116, 147, 48, 113
        ])
        expected = [
            [912815704, 1340852559, 798773507, 4092861131],
            [2297084863, 1930272723, 3075618636, 635335939],
            [3484618838, 817098033, 3685902849, 816236463],
            [617363438, 1059123231, 2707247887, 1899008884],
        ]
        assert self.service.bytes_to_matrix(sequence) == expected

    def test_matrix_to_bytes(self):
        matrix = [
            [912815704, 1340852559, 798773507, 4092861131],
            [2297084863, 1930272723, 3075618636, 635335939],
            [3484618838, 817098033, 3685902849, 816236463],
            [617363438, 1059123231, 2707247887, 1899008884],
        ]
        expected = bytes([
            88, 118, 104, 54, 79, 201, 235, 79,
            3, 81, 156, 47, 203, 26, 244, 243,
            191, 187, 234, 136, 211, 159, 13, 115,
            76, 55, 82, 183, 3, 117, 222, 37,
            86, 16, 179, 207, 49, 237, 179, 48,
            1, 106, 178, 219, 175, 199, 166, 48,
            238, 55, 204, 36, 31, 240, 32, 63,
            15, 83, 93, 161, 116, 147, 48, 113
        ])
        assert self.service.matrix_to_bytes(matrix) == expected
