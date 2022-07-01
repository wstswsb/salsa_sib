import pytest
from faker import Faker

from services import (
    EncryptionService,
    QuarterService,
    BitService,
    ConversionService,
)
faker = Faker()
Faker.seed(12345)


class TestEncryptionService:
    def setup(self):
        self.bit_service = BitService(
            operations_mask=0xFFFF_FFFF,
            operations_bit_size=32,
        )
        self.quarter_service = QuarterService(self.bit_service)
        self.conversion_service = ConversionService()
        self.service = EncryptionService(
            bit_service=self.bit_service,
            quarter_service=self.quarter_service,
            conversion_service=self.conversion_service,
        )
        self.faker = Faker()

    @pytest.mark.parametrize(
        "sequence, result",
        [
            (
                bytes(
                    [
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    ]
                ),
                bytes(
                    [
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    ]
                )
            ),
            (
                bytes(
                    [
                        211, 159, 13, 115, 76, 55, 82, 183, 3, 117, 222, 37, 191, 187, 234, 136,
                        49, 237, 179, 48, 1, 106, 178, 219, 175, 199, 166, 48, 86, 16, 179, 207,
                        31, 240, 32, 63, 15, 83, 93, 161, 116, 147, 48, 113, 238, 55, 204, 36,
                        79, 201, 235, 79, 3, 81, 156, 47, 203, 26, 244, 243, 88, 118, 104, 54,
                    ]
                ),
                bytes(
                    [
                        109, 42, 178, 168, 156, 240, 248, 238, 168, 196, 190, 203, 26, 110, 170, 154,
                        29, 29, 150, 26, 150, 30, 235, 249, 190, 163, 251, 48, 69, 144, 51, 57,
                        118, 40, 152, 157, 180, 57, 27, 94, 107, 42, 236, 35, 27, 111, 114, 114,
                        219, 236, 232, 135, 111, 155, 110, 18, 24, 232, 95, 158, 179, 19, 48, 202,
                    ]
                )
            ),
            (
                bytes(
                    [
                        88, 118, 104, 54, 79, 201, 235, 79, 3, 81, 156, 47, 203, 26, 244, 243,
                        191, 187, 234, 136, 211, 159, 13, 115, 76, 55, 82, 183, 3, 117, 222, 37,
                        86, 16, 179, 207, 49, 237, 179, 48, 1, 106, 178, 219, 175, 199, 166, 48,
                        238, 55, 204, 36, 31, 240, 32, 63, 15, 83, 93, 161, 116, 147, 48, 113,
                    ]
                ),
                bytes(
                    [
                        179, 19, 48, 202, 219, 236, 232, 135, 111, 155, 110, 18, 24, 232, 95, 158,
                        26, 110, 170, 154, 109, 42, 178, 168, 156, 240, 248, 238, 168, 196, 190, 203,
                        69, 144, 51, 57, 29, 29, 150, 26, 150, 30, 235, 249, 190, 163, 251, 48,
                        27, 111, 114, 114, 118, 40, 152, 157, 180, 57, 27, 94, 107, 42, 236, 35,
                    ]
                )
            ),
            (
                bytes(
                    [
                        101, 120, 112, 97, 1, 2, 3, 4,
                        5, 6, 7, 8,
                        9, 10, 11, 12,
                        13, 14, 15, 16, 110, 100, 32, 51, 101, 102, 103, 104, 105, 106, 107, 108,
                        109, 110, 111, 112, 113, 114, 115, 116, 50, 45, 98, 121, 201, 202, 203, 204,
                        205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 116, 101, 32, 107
                    ]
                ),
                bytes(
                    [
                        69, 37, 68, 39, 41, 15, 107, 193, 255, 139, 122, 6, 170, 233, 217, 98,
                        89, 144, 182, 106, 21, 51, 200, 65, 239, 49, 222, 34, 215, 114, 40, 126,
                        104, 197, 7, 225, 197, 153, 31, 2, 102, 78, 76, 176, 84, 245, 246, 184,
                        177, 160, 133, 130, 6, 72, 149, 119, 192, 195, 132, 236, 234, 103, 246, 74
                    ]
                )
            ),
        ]
    )
    def test_salsa20_hash(self, sequence: bytes, result: bytes):
        assert self.service.salsa20_hash(sequence) == result

    @pytest.mark.skip("Slow calculations")
    def test_salsa20_hash_1000000(self):
        sequence = bytes(
            [
                6, 124, 83, 146, 38, 191, 9, 50, 4, 161, 47, 222, 122, 182, 223, 185,
                75, 27, 0, 216, 16, 122, 7, 89, 162, 104, 101, 147, 213, 21, 54, 95,
                225, 253, 139, 176, 105, 132, 23, 116, 76, 41, 176, 207, 221, 34, 157, 108,
                94, 94, 99, 52, 90, 117, 91, 220, 146, 190, 239, 143, 196, 176, 130, 186,
            ]
        )
        expected = bytes(
            [
                8, 18, 38, 199, 119, 76, 215, 67, 173, 127, 144, 162, 103, 212, 176, 217,
                192, 19, 233, 33, 159, 197, 154, 160, 128, 243, 219, 65, 171, 136, 135, 225,
                123, 11, 68, 86, 237, 82, 20, 155, 133, 189, 9, 83, 167, 116, 194, 78,
                122, 127, 195, 185, 185, 204, 188, 90, 245, 9, 183, 248, 226, 85, 245, 104,
            ]
        )
        result = sequence
        for i in range(1_000_000):
            result = self.service.salsa20_hash(result)
        assert result == expected

    def test_salsa20_round_32_byte_key(self):
        key = bytes(
            [
                1, 2, 3, 4,
                5, 6, 7, 8,
                9, 10, 11, 12,
                13, 14, 15, 16,
                201, 202, 203, 204,
                205, 206, 207, 208,
                209, 210, 211, 212,
                213, 214, 215, 216
            ]
        )
        nonce = bytes(
            [
                101, 102, 103, 104,
                105, 106, 107, 108,
            ]
        )
        number = bytes(
            [
                109, 110, 111, 112,
                113, 114, 115, 116,
            ]
        )
        result = bytes(
            [
                69, 37, 68, 39, 41, 15, 107, 193, 255, 139, 122, 6, 170, 233, 217, 98,
                89, 144, 182, 106, 21, 51, 200, 65, 239, 49, 222, 34, 215, 114, 40, 126,
                104, 197, 7, 225, 197, 153, 31, 2, 102, 78, 76, 176, 84, 245, 246, 184,
                177, 160, 133, 130, 6, 72, 149, 119, 192, 195, 132, 236, 234, 103, 246, 74
            ]
        )
        assert self.service.salsa20_round(key, nonce, number) == result

    def test_salsa20_round_16_byte_key(self):
        key = bytes(
            [
                1, 2, 3, 4,
                5, 6, 7, 8,
                9, 10, 11, 12,
                13, 14, 15, 16,
            ]
        )
        nonce = bytes(
            [
                101, 102, 103, 104,
                105, 106, 107, 108,
            ]
        )
        number = bytes(
            [
                109, 110, 111, 112,
                113, 114, 115, 116,
            ]
        )
        result = bytes(
            [
                39, 173, 46, 248, 30, 200, 82, 17, 48, 67, 254, 239, 37, 18, 13, 247,
                241, 200, 61, 144, 10, 55, 50, 185, 6, 47, 246, 253, 143, 86, 187, 225,
                134, 85, 110, 246, 161, 163, 43, 235, 231, 94, 171, 51, 145, 214, 112, 29,
                14, 232, 5, 16, 151, 140, 183, 141, 171, 9, 122, 181, 104, 182, 177, 193
            ]
        )
        assert self.service.salsa20_round(key, nonce, number) == result

    @pytest.mark.parametrize(
        "message",
        [
            "some text",
            "некоторый текст",
            "текст с некоторыми символами !\"№;%:?*()\\1234567890-=+'",
            "очень длинный текст" * 1000,
            *[faker.pystr(max_chars=1000) for _ in range(1000)]
        ]
    )
    def test_encrypt_decrypt_16_byte_key(self, message: str):
        key = 5316911983139663491615228241121378303
        nonce = 666

        message_bytes = message.encode("utf8")
        key_bytes = key.to_bytes(length=16, byteorder="little")
        nonce_bytes = nonce.to_bytes(length=8, byteorder="little")
        encrypted = self.service.encrypt(message_bytes, key_bytes, nonce_bytes)
        decrypted = self.service.decrypt(encrypted, key_bytes, nonce_bytes)
        assert decrypted == message_bytes

    @pytest.mark.parametrize(
        "message",
        [
            "some text",
            "некоторый текст",
            "текст с некоторыми символами !\"№;%:?*()\\1234567890-=+'",
            "очень длинный текст" * 1000,
            *[faker.pystr(max_chars=1000) for _ in range(1000)]
        ]
    )
    def test_encrypt_decrypt_32_byte_key(self, message: str):
        key = 57896044618658097711785482504343953976634992332820282019728792003956564819967
        nonce = 666
        message_bytes = message.encode("utf8")
        key_bytes = key.to_bytes(length=32, byteorder="little")
        nonce_bytes = nonce.to_bytes(length=8, byteorder="little")
        encrypted = self.service.encrypt(message_bytes, key_bytes, nonce_bytes)
        decrypted = self.service.decrypt(encrypted, key_bytes, nonce_bytes)
        assert decrypted == message_bytes
