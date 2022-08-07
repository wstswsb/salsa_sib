import json
from services import (
    ConversionService,
    EncryptionService,
    QuarterService,
    BitService
)
from cryptoanalysis import StatisticsService

bit_service = BitService(operations_mask=0xFFFF_FFFF, operations_bit_size=32)
conversion_service = ConversionService()
quarter_service = QuarterService(bit_service)
encryption_service = EncryptionService(
    quarter_service,
    bit_service,
    conversion_service,
    rounds=2
)

statistics_service = StatisticsService(encryption_service, conversion_service)

key = b'12345678' * 4
statistics = statistics_service.generate(number_of_texts=10000, key=key)

with open("statistics.json", "w") as file:
    json.dump(statistics, file, indent=2)
