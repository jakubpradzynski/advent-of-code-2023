# Part One
EXAMPLE_ENGINE_SCHEMA = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""


def try_get_char(lines: list[str], y: int, x: int) -> str:
    try:
        char = lines[y][x]
    except:
        char = ""
    return char


def get_all_chars_around(lines: list[str], y: int, x: int) -> list[str]:
    chars = []
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            chars.append(try_get_char(lines, y + dy, x + dx))
            chars.append(try_get_char(lines, y + dy, x - dx))
            chars.append(try_get_char(lines, y - dy, x + dx))
            chars.append(try_get_char(lines, y - dy, x - dx))
            chars.append(try_get_char(lines, y, x + dx))
            chars.append(try_get_char(lines, y, x - dx))
            chars.append(try_get_char(lines, y + dy, x))
            chars.append(try_get_char(lines, y - dy, x))
    return list(filter(lambda x: x != "", chars))


def find_part_numbers(engine_schema: str) -> list[int]:
    part_numbers = []
    last_number_digits = []
    is_last_number_a_part_number = False
    lines = engine_schema.splitlines()
    width = len(lines[0])
    height = len(lines)
    for y in range(height):
        for x in range(width):
            if lines[y][x].isdigit():
                last_number_digits.append(lines[y][x])
                chars_around = get_all_chars_around(lines, y, x)
                if len(set(filter(lambda c: not c.isdigit() and not c == ".", chars_around))) >= 1:
                    is_last_number_a_part_number = True
            # Do nothing
            elif len(last_number_digits) > 0:
                if is_last_number_a_part_number:
                    part_numbers.append(int("".join(last_number_digits)))
                last_number_digits = []
                is_last_number_a_part_number = False
    return part_numbers


assert sum(find_part_numbers(EXAMPLE_ENGINE_SCHEMA)) == 4361

with open('Input.txt') as f:
    input_data = f.read()
    part_numbers = find_part_numbers(input_data)
    print(sum(part_numbers))


# Part Two

def find_number_from_digit(lines: list[str], y: int, x: int) -> int:
    line = lines[y]
    width = len(line)
    first_digit_index = x
    last_digit_index = x
    for i in range(x-1, -1, -1):
        if line[i].isdigit():
            first_digit_index = i
        else:
            break
    for i in range(x+1, width):
        if line[i].isdigit():
            last_digit_index = i
        else:
            break
    return int("".join(line[first_digit_index:last_digit_index+1]))


def find_adjacent_numbers(lines: list[str], y: int, x: int) -> list[int]:
    adjacent_numbers = []
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            char = try_get_char(lines, y + dy, x + dx)
            if char.isdigit():
                adjacent_numbers.append(int(find_number_from_digit(lines, y + dy, x + dx)))
    return list(set(adjacent_numbers))


def find_gear_ratios(engine_schema: str) -> list[int]:
    gear_ratios = []
    lines = engine_schema.splitlines()
    width = len(lines[0])
    height = len(lines)
    for y in range(height):
        for x in range(width):
            if lines[y][x] == "*":
                adjacent_numbers = find_adjacent_numbers(lines, y, x)
                if len(adjacent_numbers) == 2:
                    gear_ratios.append(adjacent_numbers[0] * adjacent_numbers[1])
    return gear_ratios


assert sum(find_gear_ratios(EXAMPLE_ENGINE_SCHEMA)) == 467835

with open('Input.txt') as f:
    input_data = f.read()
    gear_ratios = find_gear_ratios(input_data)
    print(sum(gear_ratios))
