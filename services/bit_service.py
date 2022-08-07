class BitService:
    def __init__(self, operations_mask: int, operations_bit_size: int):
        self.operations_mask = operations_mask
        self.operations_bit_size = operations_bit_size

    def mod_sum(self, addend: int, augend: int) -> int:
        return (addend + augend) & self.operations_mask

    def mod_sub(self, reduced: int, subtractible: int) -> int:
        result = (reduced - subtractible) & self.operations_mask
        if result < 0:
            result += (2 ** self.operations_mask)
        return result & self.operations_mask

    def cycle_left_shift(self, value: int, shift: int) -> int:
        right_shift = self.operations_bit_size - shift
        result = ((value << shift) | (value >> right_shift))
        return result & self.operations_mask

    def mod_xor(self, addend: int, augend: int) -> int:
        return (addend ^ augend) & self.operations_mask
