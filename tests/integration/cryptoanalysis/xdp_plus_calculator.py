from cryptoanalysis import BinaryVectorsGenerator, XdpPlusCalculator
from pprint import pprint


class TestXdpPlusCalculator:
    def setup(self):
        self.binary_vectors_generator = BinaryVectorsGenerator(bit_length=32)
        self.xdp_plus_calculator = XdpPlusCalculator(
            bit_length=32,
            binary_vectors_generator=self.binary_vectors_generator,
        )

    def test_find_xdp_most_probability_gamma(self):
        result = self.xdp_plus_calculator.find_xdp_most_probability_gamma(0x9008_0000, 0x8000)
        pprint(result)
