# Part One
from typing import List

TEST_INPUT = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""


def move_rocks(row: List[str], reverse=True) -> List[str]:
    return list("#".join(["".join(sorted(list(x), reverse=reverse)) for x in "".join(row).split("#")]))


def tilt_north(input: List[List[str]]) -> List[List[str]]:
    for i in range(len(input[0])):
        column = [row[i] for row in input]
        tilted_column = move_rocks(column)
        for j in range(len(input)):
            input[j][i] = tilted_column[j]
    return input


def count_total_load(input: List[List[str]]) -> int:
    count = 0
    for index, row in enumerate(input):
        rocks_count = len(list(filter(lambda x: x == "O", row)))
        multiplier = len(input) - index
        count += rocks_count * multiplier
    return count


def part_one(input: str) -> int:
    parsed_input = list(map(lambda x: list(x), input.splitlines()))
    tilted = tilt_north(parsed_input)
    return count_total_load(tilted)


assert part_one(TEST_INPUT) == 136

with open("Input.txt") as file:
    print(part_one(file.read()))


# Part Two

def tilt_west(input: List[List[str]]) -> List[List[str]]:
    return [move_rocks(row) for row in input]


def tilt_south(input: List[List[str]]) -> List[List[str]]:
    for i in range(len(input[0])):
        column = [row[i] for row in input]
        tilted_column = move_rocks(column, reverse=False)
        for j in range(len(input)):
            input[j][i] = tilted_column[j]
    return input


def tilt_east(input: List[List[str]]) -> List[List[str]]:
    return [move_rocks(row, reverse=False) for row in input]


def cycle(input: List[List[str]]) -> List[List[str]]:
    return tilt_east(tilt_south(tilt_west(tilt_north(input))))


def part_two(input: str) -> int:
    parsed_input = list(map(lambda x: list(x), input.splitlines()))
    cycled = parsed_input

    seen = []
    for i in range(1, 1000000001):
        cycled = cycle(cycled)
        joined = "\n".join([" ".join(row) for row in cycled])
        if joined in seen:
            index = seen.index(joined)
            cycle_loop = seen[index:]
            remaining_cycles = 1000000000 - i
            index_billionth = remaining_cycles % len(cycle_loop)
            split = [x.split(" ") for x in cycle_loop[index_billionth].split("\n")]
            total_load = count_total_load(split)
            break
        seen.append(joined)
    return total_load


assert part_two(TEST_INPUT) == 64

with open("Input.txt") as file:
    print(part_two(file.read()))
