from .conversion_service import ConversionService
from .bit_service import BitService
from .quarter_service import QuarterService
from exceptions import InvalidKeyLengthException


class EncryptionService:
    def __init__(
            self,
            quarter_service: QuarterService,
            bit_service: BitService,
            conversion_service: ConversionService):
        self.quarter_service = quarter_service
        self.bit_service = bit_service
        self.conversion_service = conversion_service

    def encrypt(self, message: bytes, key: bytes, nonce: bytes) -> bytes:
        gamma_block_bytes = 64
        message = self.pad(message, gamma_block_bytes)
        return self.crypt(message, key, nonce)

    def decrypt(self, ciphertext: bytes, key: bytes, nonce: bytes) -> bytes:
        decrypted = self.crypt(ciphertext, key, nonce)
        pad_size = self.conversion_service.bytes_to_int_little_endian(decrypted[-64:])
        decrypted = decrypted[:-(64 + pad_size)]
        return decrypted

    def pad(self, sequence: bytes, block_size: int) -> bytes:
        pad_size = block_size - (len(sequence) % block_size)
        sequence += b"0" * pad_size
        sequence += self.conversion_service.int_to_bytes_from_little_endian(pad_size, length=64)
        return sequence

    def crypt(self, message: bytes, key: bytes, nonce: bytes) -> bytes:
        gamma_block_bytes = 64
        gamma_block_count = int(len(message) / gamma_block_bytes)
        message_ints = self.conversion_service.bytes_to_ints(message)
        gamma_ints = []
        for i in range(gamma_block_count):
            num = self.conversion_service.int_to_bytes_from_little_endian(i, length=8)
            round_bytes = self.salsa20_round(key, nonce, num)
            gamma_ints += self.conversion_service.bytes_to_ints(round_bytes)
        result_ints = []
        for i, message_int in enumerate(message_ints):
            result_ints.append(message_int ^ gamma_ints[i])
        return self.conversion_service.ints_to_bytes(result_ints)

    def salsa20_round(self, key: bytes, nonce: bytes, number: bytes) -> bytes:
        sequence = self.expand_key(key, nonce, number)
        return self.salsa20_hash(sequence)

    def salsa20_hash(self, sequence: bytes) -> bytes:
        ints = self.conversion_service.bytes_to_ints(sequence)
        matrix = self.conversion_service.ints_to_matrix(ints)
        for i in range(10):
            matrix = self.quarter_service.double_round(matrix)
        quartered_ints = self.conversion_service.matrix_to_ints(matrix)
        result_ints = [
            self.bit_service.mod_sum(quartered_ints[i], ints[i])
            for i in range(len(ints))
        ]
        return self.conversion_service.ints_to_bytes(result_ints)

    def expand_key(self, key: bytes, nonce: bytes, number: bytes) -> bytes:
        key_length = len(key)
        if key_length == 16:
            return self._expand_key_16(key, nonce, number)
        if key_length == 32:
            return self._expand_key_32(key, nonce, number)
        raise InvalidKeyLengthException(
            f"{key_length = },"
            " but expected in [16, 32]"
        )

    def _expand_key_16(
            self,
            key: bytes,
            nonce: bytes,
            number: bytes) -> bytes:
        t_0 = bytes([101, 120, 112, 97])
        t_1 = bytes([110, 100, 32, 49])
        t_2 = bytes([54, 45, 98, 121])
        t_3 = bytes([116, 101, 32, 107])
        total_bytes = t_0 + key + t_1 + nonce + number + t_2 + key + t_3
        return total_bytes

    def _expand_key_32(
            self,
            key: bytes,
            nonce: bytes,
            number: bytes) -> bytes:
        q_0 = bytes([101, 120, 112, 97])
        q_1 = bytes([110, 100, 32, 51])
        q_2 = bytes([50, 45, 98, 121])
        q_3 = bytes([116, 101, 32, 107])
        k_0, k_1 = self.conversion_service.split_key_32(key)
        total_bytes = q_0 + k_0 + q_1 + nonce + number + q_2 + k_1 + q_3
        return total_bytes
