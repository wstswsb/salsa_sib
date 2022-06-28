class BitService:
    def __init__(self, block_mask: int, block_bit_size: int):
        self.block_mask = block_mask
        self.block_bit_size = block_bit_size

    def mod_sum(self, addend: int, augend: int) -> int:
        return (addend + augend) & self.block_mask

    def cycle_left_shift(self, value: int, shift: int) -> int:
        right_shift = self.block_bit_size - shift
        return ((value << shift) | (value >> right_shift)) & self.block_mask

    def mod_xor(self, addend: int, augend: int) -> int:
        return (addend ^ augend) & self.block_mask
