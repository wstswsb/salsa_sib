from exceptions import InvalidBitLengthException
from .binary_vectors_generator import BinaryVectorsGenerator


class XdpPlusCalculator:
    def __init__(
            self,
            bit_length: int,
            binary_vectors_generator: BinaryVectorsGenerator):
        self.binary_vectors_generator = binary_vectors_generator
        self.bit_length = bit_length
        self.mask = 2 ** bit_length - 1
        self.mask_n_sub_1 = self.mask >> 1

    def calculate_hamming_weight(self, number: int) -> int:
        if number.bit_length() > self.bit_length:
            raise InvalidBitLengthException()
        x = number
        x = x - ((x >> 1) & 0x5555_5555)
        x = (x & 0x3333_3333) + ((x >> 2) & 0x3333_3333)
        x = (x + (x >> 4)) & 0x0F0F_0F0F
        x = x + (x >> 8)
        x = (x + (x >> 16)) & 0x0000_003F
        return x & self.mask

    def equality(self, x: int, y: int, z: int) -> int:
        return (((~x) ^ y) & ((~x) ^ z)) & self.mask

    def find_xdp(self, alpha: int, betta: int, gamma: int) -> float:
        equality = self.equality(alpha << 1, betta << 1, gamma << 1)
        xor_result = (alpha ^ betta ^ gamma ^ (betta << 1)) & self.mask
        if (equality & xor_result) != 0:
            return 0.0
        return 2 ** self._calculate_probability_degree(alpha, betta, gamma)

    def find_xdp_most_probability_gamma(
            self,
            alpha: int,
            betta: int,
            upper_board=4) -> dict:
        xdp_stat = []
        for number_of_different_bits in range(upper_board):
            gamma_generator = self.binary_vectors_generator.generate_different_values(
                alpha,
                number_of_different_bits,
            )
            for gamma in gamma_generator:
                xdp = self.find_xdp(alpha, betta, gamma)
                if not xdp:
                    continue
                xdp_stat.append(
                    {
                        "alpha": alpha,
                        "betta": betta,
                        "gamma": gamma,
                        "probability": xdp,
                    }
                )
        if not xdp_stat:
            return {"alpha": alpha, "betta": betta, "gamma": gamma, "probability": 0}
        xdp_stat.sort(key=lambda x: -x["probability"])
        return xdp_stat[0]

    def find_slow_xdp(
            self, alpha: int, betta: int,
            gamma: int, bit_length: int) -> float:
        max_value = 2 ** bit_length - 1
        total_gamma_number = 0
        right_gamma_number = 0
        for x in range(max_value + 1):
            for y in range(max_value + 1):
                left = (x ^ alpha) + (y ^ betta)
                right = (x + y) ^ gamma
                if (left ^ right) & self.mask == 0:
                    right_gamma_number += 1
                total_gamma_number += 1
        return right_gamma_number / total_gamma_number

    def _calculate_probability_degree(self, alpha: int, betta: int, gamma: int) -> int:
        equality = self.equality(alpha, betta, gamma)
        weight = self.calculate_hamming_weight((~equality) & self.mask_n_sub_1)
        return -weight
