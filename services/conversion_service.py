
class ConversionService:
    def bytes_to_int_little_endian(self, sequence: bytes) -> int:
        return int.from_bytes(sequence, "little")

    def int_to_bytes_from_little_endian(self, item: int, length=4) -> bytes:
        return item.to_bytes(length, byteorder="little")

    def bytes_to_ints(self, sequence: bytes) -> list[int]:
        return [
            self.bytes_to_int_little_endian(sequence[i - 4: i])
            for i
            in range(4, len(sequence) + 4, 4)
        ]

    def ints_to_bytes(self, sequence: list[int]) -> bytes:
        return b''.join([
            self.int_to_bytes_from_little_endian(item)
            for item
            in sequence
        ])

    def ints_to_matrix(
            self,
            sequence: list[int]) -> list[list[int]]:
        return [
            sequence[i - 4: i]
            for i
            in range(4, len(sequence) + 1, 4)
        ]

    def matrix_to_ints(self, matrix: list[list[int]]) -> list[int]:
        return [matrix[i][j] for i in range(4) for j in range(4)]

    def bytes_to_matrix(self, sequence: bytes) -> list[list[int]]:
        ints_sequence = self.bytes_to_ints(sequence)
        return self.ints_to_matrix(ints_sequence)

    def matrix_to_bytes(self, matrix: list[list[int]]) -> bytes:
        ints_sequence = self.matrix_to_ints(matrix)
        return self.ints_to_bytes(ints_sequence)

    def split_key_32(self, key: bytes) -> tuple[bytes, bytes]:
        return key[:16], key[16:]
