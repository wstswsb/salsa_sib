import pytest
from cryptoanalysis import BinaryVectorsGenerator


class TestBinaryVectorsGenerator:
    def setup(self):
        self.generator = BinaryVectorsGenerator(bit_length=4)

    @pytest.mark.parametrize(
        "number, positions, expected",
        [
            (0b0000, (0,), 0b0001),
            (0b0000, (1,), 0b0010),
            (0b0000, (2,), 0b0100),
            (0b0000, (3,), 0b1000),
            (0b1111, (0,), 0b1110),
            (0b1111, (1,), 0b1101),
            (0b1111, (2,), 0b1011),
            (0b1111, (3,), 0b0111),
        ]
    )
    def test_invert_bits_on_positions(
            self,
            number: int,
            positions: tuple[int],
            expected: int):
        result = self.generator.invert_bits_at_positions(number, positions)
        assert result == expected

    @pytest.mark.parametrize(
        "number_of_different_bits, expected",
        [
            (
                1,
                [
                    (0b00, 0b01), (0b00, 0b10),
                    (0b01, 0b00), (0b01, 0b11),
                    (0b10, 0b11), (0b10, 0b00),
                    (0b11, 0b10), (0b11, 0b01),
                ]
            ),

            (
                2,
                [
                    (0b00, 0b11), (0b01, 0b10),
                    (0b10, 0b01), (0b11, 0b00)
                ]
            )
        ]
    )
    def test_generate_different_pairs(
            self,
            number_of_different_bits: int,
            expected: tuple[tuple[int]]):
        generator = BinaryVectorsGenerator(bit_length=2)
        values_generator = generator.generate_different_pairs(
            number_of_different_bits
        )
        values = list(values_generator)
        assert set(values) == set(expected)
