# Part One
import itertools

TEST_INPUT = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""


def count_sum_of_the_shortest_paths(input: str, exp: int) -> int:
    world = list(map(lambda x: list(itertools.chain.from_iterable(x)), input.splitlines()))
    star_coordinates = [(i, j) for i in range(len(world)) for j in range(len(world[0])) if world[i][j] == '#']
    insertions = 0
    for i in range(len(world)):
        if "#" not in world[i]:
            for index, star in enumerate(star_coordinates):
                if star[0] >= i + insertions * exp:
                    star_coordinates[index] = (star[0] + exp, star[1])
            insertions += 1
    insertions = 0
    for i in range(len(world[0])):
        column = list(map(lambda x: x[i], world))
        if "#" not in column:
            for index, star in enumerate(star_coordinates):
                if star[1] >= i + insertions * exp:
                    star_coordinates[index] = (star[0], star[1] + exp)
            insertions += 1
    combinations = itertools.combinations(star_coordinates, 2)
    path_lengths = []
    for star1, star2 in combinations:
        path_lengths.append(abs(star1[0] - star2[0]) + abs(star1[1] - star2[1]))
    return sum(path_lengths)


def part_one(input: str) -> int:
    return count_sum_of_the_shortest_paths(input, 1)


assert part_one(TEST_INPUT) == 374

with open("Input.txt") as f:
    print(part_one(f.read()))


# Part Two

def part_two(input: str) -> int:
    return count_sum_of_the_shortest_paths(input, 999_999)


assert count_sum_of_the_shortest_paths(TEST_INPUT, 9) == 1030
assert count_sum_of_the_shortest_paths(TEST_INPUT, 99) == 8410

with open("Input.txt") as f:
    print(part_two(f.read()))
