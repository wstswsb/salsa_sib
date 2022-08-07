import json
from pprint import pprint
from services import (
    ConversionService,
    EncryptionService,
    QuarterService,
    BitService
)

bit_service = BitService(operations_mask=0xFFFF_FFFF, operations_bit_size=32)
conversion_service = ConversionService()
quarter_service = QuarterService(bit_service)
encryption_service = EncryptionService(
    quarter_service,
    bit_service,
    conversion_service,
    rounds=2
)


def sub_matrix_mod_2_in_32(
        reduced: list[list[int]],
        subtractible: list[list[int]]) -> list[list[int]]:
    result = []
    for i in range(len(reduced)):
        reduced_line = reduced[i]
        subtractible_line = subtractible[i]
        result_line = []
        for j in range(len(reduced_line)):
            reduce_tmp = reduced_line[j]
            subtractible_tmp = subtractible_line[j]
            result_line.append(bit_service.mod_sub(reduce_tmp, subtractible_tmp))
        result.append(result_line)
    return result


def count_differences(stat: list[str]):
    differences = {}
    for item in stat:
        if item not in differences:
            differences[item] = 0
        differences[item] += 1
    differences = [(key, value) for key, value in differences.items()]
    differences.sort(key=lambda x: -x[1])
    return differences


def show_most_probabilistic_top_3(differences: list[tuple[str, int]], stat_length: int):
    pprint(
        [
            (value, probability / stat_length)
            for value, probability
            in differences[:5]
        ]
    )


with open("statistics.json") as file:
    statistics_list = json.load(file)

delta_3_0_stat = []
delta_3_3_stat = []

for pair_stat in statistics_list:
    # key = conversion_service.ints_to_bytes([0, 0, 0] + pair_stat["key"][3:])
    # key = conversion_service.ints_to_bytes(pair_stat["key"])
    key = b"qwertyui" * 4
    nonce = conversion_service.ints_to_bytes(pair_stat["nonce"])
    index = conversion_service.ints_to_bytes(pair_stat["text_0_index"])
    index_stroke = conversion_service.ints_to_bytes(pair_stat["text_1_index"])
    salsa_input_0_bytes = encryption_service.expand_key(key, nonce, index)
    salsa_input_1_bytes = encryption_service.expand_key(key, nonce, index_stroke)

    salsa_output_0_matrix = pair_stat["encrypted_0"]
    salsa_output_1_matrix = pair_stat["encrypted_1"]

    salsa_input_0_matrix = conversion_service.bytes_to_matrix(salsa_input_0_bytes)
    salsa_input_1_matrix = conversion_service.bytes_to_matrix(salsa_input_1_bytes)

    r_output_0 = sub_matrix_mod_2_in_32(salsa_output_0_matrix, salsa_input_0_matrix)
    r_output_1 = sub_matrix_mod_2_in_32(salsa_output_1_matrix, salsa_input_1_matrix)

    r_0_reversed = quarter_service.double_round(r_output_0, reverse=True)
    r_1_reversed = quarter_service.double_round(r_output_1, reverse=True)

    delta_3_0 = bit_service.mod_xor(r_0_reversed[3][0], r_1_reversed[3][0])
    delta_3_3 = bit_service.mod_xor(r_0_reversed[3][3], r_1_reversed[3][3])

    delta_3_0_stat.append(f"0x{delta_3_0:09_x}")
    delta_3_3_stat.append(f"0x{delta_3_3:09_x}")

differences_3_0 = count_differences(delta_3_0_stat)
differences_3_3 = count_differences(delta_3_3_stat)

print("differences_3_0")
show_most_probabilistic_top_3(differences_3_0, len(statistics_list))
print()
print("differences_3_3")
show_most_probabilistic_top_3(differences_3_3, len(statistics_list))
