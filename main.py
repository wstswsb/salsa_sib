import json
from click import echo, style
from services import BitService
from cryptoanalysis import XdpPlusCalculator, BinaryVectorsGenerator
from typing import NamedTuple


class ProcessZValue(NamedTuple):
    delta: int
    gamma: int
    probability: float


def present_gamma(gamma_stat: dict[str, int]) -> str:
    to_present = {}
    for key, value in gamma_stat.items():
        if key == "xdp":
            to_present[key] = value
            continue
        to_present[key] = f"0x{value:09_x}"
    return json.dumps(to_present, indent=2)


def present_number_as_colored_hex_str(number: int) -> str:
    hex_num = f"{number:09_x}"
    colored_num = ""
    for digit in hex_num:
        if digit == "_":
            colored_num += digit
        elif digit == "0":
            colored_num += style(digit, "green")
        else:
            colored_num += style(digit, "black", bg="red")
    return "0x" + colored_num


def present_matrix(matrix: list[list[int]]) -> str:
    result = ""
    for line in matrix:
        presented_line = []
        for number in line:
            if not isinstance(number, int):
                presented_line.append(number)
                continue
            presented_line.append(present_number_as_colored_hex_str(number))

        result += "\t".join(presented_line)
        result += "\n"
    return result


def process_z(
        xor_addend: int,
        mod_2_in_32_addend: int,
        mod_2_in_32_augend: int,
        shift: int):
    xdp_stat = xdp_plus_calculator.find_xdp_most_probability_gamma(
        mod_2_in_32_addend,
        mod_2_in_32_augend,
    )
    gamma = xdp_stat["gamma"]
    delta = bit_service.mod_xor(
        xor_addend,
        bit_service.cycle_left_shift(gamma, shift),
    )
    return ProcessZValue(delta, gamma, probability=xdp_stat["probability"])


def reconstruct_matrix_for_present(old_matrix_for_present, new_values_matrix):
    new_matrix_for_present = []
    for i in range(4):
        line = []
        for j in range(4):
            old_value = old_matrix_for_present[i][j]
            if isinstance(old_value, str):
                line.append(old_value)
            else:
                line.append(new_values_matrix[i][j])
        new_matrix_for_present.append(line)
    return new_matrix_for_present


def find_all_z_and_show_log(y0: int, y1: int, y2: int, y3: int) -> tuple[int, int, int, int]:
    colored_y0 = present_number_as_colored_hex_str(y0)
    colored_y1 = present_number_as_colored_hex_str(y1)
    colored_y2 = present_number_as_colored_hex_str(y2)
    colored_y3 = present_number_as_colored_hex_str(y3)
    echo("MatrixColumn = 1\n")
    echo("y0 = " + colored_y0)
    echo("y1 = " + colored_y1)
    echo("y2 = " + colored_y2)
    echo("y3 = " + colored_y3)
    print()

    # __ z1 __ #
    process_z1_value = process_z(y1, y0, y3, shift=7)
    z1 = process_z1_value.delta
    gamma = process_z1_value.gamma
    probability = process_z1_value.probability

    colored_z1 = present_number_as_colored_hex_str(z1)
    colored_gamma = present_number_as_colored_hex_str(gamma)
    echo(f"(y0 +  y3)mod(2**32) = {colored_y0} + {colored_y3} = {colored_gamma} ({probability=})")
    left_equation_part = style(
        "z1 = y1 xor ((y0 + y3) << 7) = ",
        fg="black",
        bg="yellow",
    )
    right_equation_part = f"{colored_z1} ({probability=})\n"
    echo(left_equation_part + right_equation_part)

    # __ z2 __ #
    process_z2_value = process_z(y2, z1, y0, shift=9)
    z2 = process_z2_value.delta
    gamma = process_z2_value.gamma
    probability = process_z2_value.probability

    colored_z2 = present_number_as_colored_hex_str(z2)
    colored_gamma = present_number_as_colored_hex_str(gamma)
    echo(f"(z1 +  y0)mod(2**32) = {colored_z1} + {colored_y0} = {colored_gamma} ({probability=})")
    left_equation_part = style(
        "z2 = y2 xor ((z1 + y0) << 9) = ",
        fg="black",
        bg="yellow",
    )
    right_equation_part = f"{colored_z2} ({probability=})\n"
    echo(left_equation_part + right_equation_part)

    # __ z3 __ #
    process_z3_value = process_z(y3, z2, z1, shift=13)
    z3 = process_z3_value.delta
    gamma = process_z3_value.gamma
    probability = process_z3_value.probability

    colored_z3 = present_number_as_colored_hex_str(z3)
    colored_gamma = present_number_as_colored_hex_str(gamma)
    echo(f"(z2 +  z1)mod(2**32) = {colored_z2} + {colored_z1} = {colored_gamma} ({probability=})")
    left_equation_part = style(
        "z3 = y3 xor ((z2 + z1) << 13) = ",
        fg="black",
        bg="yellow",
    )
    right_equation_part = f"{colored_z3} ({probability=})\n"
    echo(left_equation_part + right_equation_part)

    # __ z0 __ #
    process_z0_value = process_z(y0, z3, z2, shift=18)
    z0 = process_z0_value.delta
    gamma = process_z0_value.gamma
    probability = process_z0_value.probability

    colored_z0 = present_number_as_colored_hex_str(z0)
    colored_gamma = present_number_as_colored_hex_str(gamma)
    echo(f"(z3 +  z2)mod(2**32) = {colored_z3} + {colored_z2} = {colored_gamma} ({probability=})")
    left_equation_part = style(
        "z0 = y0 xor ((z3 + z2) << 18) = ",
        fg="black",
        bg="yellow",
    )
    right_equation_part = f"{colored_z0} ({probability=})\n"
    echo(left_equation_part + right_equation_part)
    return z0, z1, z2, z3


bit_service = BitService(
    operations_mask=0xFFFF_FFFF,
    operations_bit_size=32,
)

binary_vector_generator = BinaryVectorsGenerator(bit_length=32)
xdp_plus_calculator = XdpPlusCalculator(
    bit_length=32,
    binary_vectors_generator=binary_vector_generator,
)

matrix = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0x8000_0000, 0, 0],
    [0, 0, 0, 0],
]
matrix_for_present = [item[:] for item in matrix]
echo(style("Start matrix\n", "cyan"))
echo(present_matrix(matrix_for_present))

# _______________________<start> COLUMN_ROUND 1 _______________________#
echo(style("ColumnRound\n", "cyan"))
y0 = matrix[1][1]
y1 = matrix[2][1]
y2 = matrix[3][1]
y3 = matrix[0][1]

# __ column_1 __ #
z0, z1, z2, z3 = find_all_z_and_show_log(y0, y1, y2, y3)
matrix[2][1] = z1
matrix[3][1] = z2
matrix[0][1] = z3
matrix[1][1] = z0

matrix_for_present = reconstruct_matrix_for_present(matrix_for_present, matrix)
matrix_for_present[1][1] = "?" * 11
echo(style("After ColumnRound matrix (Probability=0.5))\n", "cyan"))
echo(present_matrix(matrix_for_present))
echo(style("Without (?):"))
echo(present_matrix(matrix))
# _______________________<end> COLUMN_ROUND 1 _______________________#

# _______________________<start> ROW_ROUND 2 _______________________#
echo(style("RowRound", "cyan"))
for i in range(4):
    echo(style(f"Line {i}", "cyan"))
    y0 = matrix[i][i]
    y1 = matrix[i][(i + 1) % 4]
    y2 = matrix[i][(i + 2) % 4]
    y3 = matrix[i][(i + 3) % 4]
    z0, z1, z2, z3 = find_all_z_and_show_log(y0, y1, y2, y3)
    matrix[i][i] = z0
    matrix[i][(i + 1) % 4] = z1
    matrix[i][(i + 2) % 4] = z2
    matrix[i][(i + 3) % 4] = z3
echo(style("After RowRound matrix (Probability=0.125))\n", "cyan"))
matrix_for_present = reconstruct_matrix_for_present(matrix_for_present, matrix)
for i in range(4):
    for j in range(4):
        if i == 3 and j == 0:
            continue
        if i == 3 and j == 3:
            continue
        matrix_for_present[i][j] = "?" * 11
echo(present_matrix(matrix_for_present))
echo(style("Without (?):"))
echo(present_matrix(matrix))
