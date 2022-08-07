import pytest
from mock import Mock
from cryptoanalysis import XdpPlusCalculator


class TestXdpPlusCalculator:
    def setup(self):
        self.binary_vectors_generator_mock = Mock()
        self.calculator = XdpPlusCalculator(
            bit_length=32,
            binary_vectors_generator=self.binary_vectors_generator_mock,
        )

    @pytest.mark.parametrize(
        "number, result",
        [
            (0b1, 1),
            (0b10, 1),
            (0b11, 2),
            (0b101, 2),
            (0b111, 3),
            (0b101010, 3),
            (0b0000_1111, 4),
            (0b1010_1010, 4),
            (0xFFFF_FFFF, 32)
        ]
    )
    def test_calculate_hamming_weight(self, number: int, result: int):
        assert self.calculator.calculate_hamming_weight(number) == result

    @pytest.mark.parametrize(
        "alpha, betta, gamma",
        [
            (alpha, betta, gamma)
            for alpha in range(0xF + 1)
            for betta in range(0xF + 1)
            for gamma in range(0xF + 1)
        ]
    )
    def test_xdp(self, alpha, betta, gamma):
        calculator = XdpPlusCalculator(
            bit_length=4,
            binary_vectors_generator=self.binary_vectors_generator_mock,
        )
        expected = calculator.find_slow_xdp(alpha, betta, gamma, bit_length=4)
        result = calculator.find_xdp(alpha, betta, gamma)
        assert result == expected
