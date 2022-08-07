from random import randbytes, randint
from services import EncryptionService, ConversionService


class StatisticsService:
    def __init__(
            self,
            encryption_service: EncryptionService,
            conversion_service: ConversionService):
        self.encryption_service = encryption_service
        self.conversion_service = conversion_service

    def generate_i0_i1(self) -> tuple[int, int]:
        i0_int = randint(0, 2**32)
        i1_int = randint(0, 2**32)
        return i0_int, i1_int

    def generate_i0_i1_stroke(self, i0: int, i1: int) -> tuple[int, int]:
        i1_stroke = i1 ^ (1 << 31)
        assert i1 ^ i1_stroke == 0x8000_0000
        return i0, i1_stroke

    def generate_i0_i1_i0_stoke_i1_stroke_bytes(self) -> tuple[bytes, bytes]:
        i0, i1 = self.generate_i0_i1()
        i0_stoke, i1_stroke = self.generate_i0_i1_stroke(i0, i1)
        convert_func = self.conversion_service.int_to_bytes_from_little_endian
        index_bytes = convert_func(i0) + convert_func(i1)
        index_stroke_bytes = convert_func(i0_stoke) + convert_func(i1_stroke)
        return index_bytes, index_stroke_bytes

    def generate(self, number_of_texts: int, key: bytes):
        salsa_statistics = []
        for _ in range(number_of_texts):
            nonce = randbytes(8)
            index, index_stroke = self.generate_i0_i1_i0_stoke_i1_stroke_bytes()
            encrypted_0 = self.encryption_service.salsa20_round(
                key=key,
                nonce=nonce,
                index=index
            )
            encrypted_1 = self.encryption_service.salsa20_round(
                key=key,
                nonce=nonce,
                index=index_stroke,
            )
            salsa_statistics.append(
                {
                    "key": self.conversion_service.bytes_to_ints(key),
                    "nonce": self.conversion_service.bytes_to_ints(nonce),
                    "text_0_index": self.conversion_service.bytes_to_ints(index),
                    "text_1_index": self.conversion_service.bytes_to_ints(index_stroke),
                    "encrypted_0": self.conversion_service.bytes_to_matrix(encrypted_0),
                    "encrypted_1": self.conversion_service.bytes_to_matrix(encrypted_1),
                }
            )
        return salsa_statistics
