from itertools import combinations
from typing import Generator


class BinaryVectorsGenerator:
    def __init__(self, bit_length: int):
        self.bit_length = bit_length
        self.indexes: list[int] = list(range(bit_length))
        self.mask = 2 ** bit_length - 1

    def generate_different_pairs(
            self,
            number_of_different_bits: int) -> Generator[tuple, None, None]:
        for alpha in range(self.mask + 1):
            different_values_generator = self.generate_different_values(
                alpha,
                number_of_different_bits,
            )
            for betta in different_values_generator:
                yield alpha, betta

    def generate_different_values(self, number: int, number_of_different_bits: int):
        for positions in combinations(self.indexes, number_of_different_bits):
            different_value = self.invert_bits_at_positions(number, positions)
            yield different_value

    def invert_bits_at_positions(self, number: int, positions: tuple[int]):
        mask = 0
        for position in positions:
            mask |= (1 << position)
        return number ^ mask
