# Part One
import math
from typing import List

TEST_INPUT_1 = """-L|F7
7S-7|
L|7||
-L-J|
L|-JF
"""

TEST_INPUT_2 = """7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ"""

connections = {
    "|": [(1, 0), (-1, 0)],
    "-": [(0, 1), (0, -1)],
    "L": [(-1, 0), (0, 1)],
    "J": [(-1, 0), (0, -1)],
    "7": [(1, 0), (0, -1)],
    "F": [(1, 0), (0, 1)],
    ".": [],
    "P": []
}


def parse_input(input: str) -> List[List[str]]:
    return [list(line) for line in input.splitlines()]


def find_starting_location(tiles: List[List[str]]) -> (int, int):
    for x, row in enumerate(tiles):
        for y, row2 in enumerate(row):
            if tiles[x][y] == 'S':
                return x, y


def find_connections_to_starting_point(tiles: List[List[str]], S_location: (int, int)) -> List[tuple]:
    results = []
    for x in range(-1, 2):
        for y in range(-1, 2):
            try:
                tile = tiles[S_location[0] + x][S_location[1] + y]
                tile_connections = connections[tile]
                for dx, dy in tile_connections:
                    if x + dx == 0 and y + dy == 0:
                        results += [(S_location[0] + x, S_location[1] + y)]
            except:
                pass
    return results


def count_steps_in_path(tiles: List[List[str]], start: (int, int), current_position: (int, int)) -> int:
    steps = 1
    previous_position = start
    current_position = current_position
    while tiles[current_position[0]][current_position[1]] != 'S':
        c = connections[tiles[current_position[0]][current_position[1]]]
        next_positions = []
        for dx, dy in c:
            next_positions.append((current_position[0] + dx, current_position[1] + dy))
        for next_position in next_positions:
            if not (next_position[0] is previous_position[0] and next_position[1] is previous_position[1]):
                previous_position = current_position
                current_position = next_position
                break
        steps += 1
    return steps


def find_max_steps(input: str) -> int:
    tiles = parse_input(input)
    S_location = find_starting_location(tiles)
    connections_to_start = find_connections_to_starting_point(tiles, S_location)
    steps_in_path_count = count_steps_in_path(tiles, S_location, connections_to_start[0])
    return int(math.ceil(steps_in_path_count / 2))


assert find_max_steps(TEST_INPUT_1) == 4
assert find_max_steps(TEST_INPUT_2) == 8

with open("Input.txt") as f:
    print(find_max_steps(f.read()))

# Part Two

replacements = {
    "|": [
        [".", "|", "."],
        [".", "|", "."],
        [".", "|", "."]
    ],
    "-": [
        [".", ".", "."],
        ["-", "-", "-"],
        [".", ".", "."]
    ],
    "L": [
        [".", "|", "."],
        [".", "L", "-"],
        [".", ".", "."]
    ],
    "J": [
        [".", "|", "."],
        ["-", "J", "."],
        [".", ".", "."]
    ],
    "7": [
        [".", ".", "."],
        ["-", "7", "."],
        [".", "|", "."]
    ],
    "F": [
        [".", ".", "."],
        [".", "F", "-"],
        [".", "|", "."]
    ],
    ".": [
        [".", ".", "."],
        [".", ".", "."],
        [".", ".", "."]
    ],
    "S": [
        [".", "S", "."],
        ["S", "S", "S"],
        [".", "S", "."]
    ]
}


def make_tiles_bigger(original_tiles: List[List[str]]) -> List[List[str]]:
    new_tiles = []
    for row in original_tiles:
        new_row_1 = []
        new_row_2 = []
        new_row_3 = []
        for tile in row:
            new_row_1 += (replacements[tile][0])
            new_row_2 += (replacements[tile][1])
            new_row_3 += (replacements[tile][2])
        new_tiles.append(new_row_1)
        new_tiles.append(new_row_2)
        new_tiles.append(new_row_3)
    return new_tiles


def mark_path(tiles: List[List[str]], start: (int, int), current_position: (int, int)) -> list[list[str]]:
    previous_position = start
    tiles[previous_position[0]][previous_position[1]] = 'P'
    current_position = current_position
    while tiles[current_position[0]][current_position[1]] != 'P':
        c = connections[tiles[current_position[0]][current_position[1]]]
        tiles[current_position[0]][current_position[1]] = 'P'
        next_positions = []
        for dx, dy in c:
            next_positions.append((current_position[0] + dx, current_position[1] + dy))
        for next_position in next_positions:
            if not (next_position[0] is previous_position[0] and next_position[1] is previous_position[1]) and tiles[next_position[0]][next_position[1]] != 'P':
                previous_position = current_position
                current_position = next_position
                break

    return tiles


def mark_sure_zeros(tiles: List[List[str]]) -> List[List[str]]:
    while True:
        changed_zeros = 0
        for x in range(len(tiles)):
            for y in range(len(tiles[x])):
                tile = tiles[x][y]
                if tile != 'P' and tile != '0':
                    surrounding_tiles = []
                    for dx in range(-1, 2):
                        for dy in range(-1, 2):
                            if 0 <= x + dx < len(tiles) and 0 <= y + dy < len(tiles[x]) and not (dx == 0 and dy == 0):
                                surrounding_tiles.append(tiles[x + dx][y + dy])

                    if len(surrounding_tiles) < 8 or '0' in surrounding_tiles:
                        changed_zeros += 1
                        tiles[x][y] = '0'
        if changed_zeros == 0:
            break
    return tiles


def replace_starting_location(tiles: List[List[str]], S_location: (int, int), connections_to_start: List[tuple]) -> List[List[str]]:
    if (1, 0) in connections_to_start and (-1, 0) in connections_to_start:
        tiles[S_location[0]][S_location[1]] = "|"
    elif (0, 1) in connections_to_start and (0, -1) in connections_to_start:
        tiles[S_location[0]][S_location[1]] = "-"
    elif (-1, 0) in connections_to_start and (0, 1) in connections_to_start:
        tiles[S_location[0]][S_location[1]] = "L"
    elif (-1, 0) in connections_to_start and (0, -1) in connections_to_start:
        tiles[S_location[0]][S_location[1]] = "J"
    elif (1, 0) in connections_to_start and (0, -1) in connections_to_start:
        tiles[S_location[0]][S_location[1]] = "7"
    elif (1, 0) in connections_to_start and (0, 1) in connections_to_start:
        tiles[S_location[0]][S_location[1]] = "F"
    return tiles


def find_connections_to_starting_point(tiles: List[List[str]], S_location: (int, int)) -> List[tuple]:
    results = []
    for x in range(-1, 2):
        for y in range(-1, 2):
            try:
                tile = tiles[S_location[0] + x][S_location[1] + y]
                tile_connections = connections[tile]
                for dx, dy in tile_connections:
                    if x + dx == 0 and y + dy == 0:
                        results += [(x, y)]
            except:
                pass
    return results


def try_get_tile(tiles, x, y):
    try:
        return tiles[x][y]
    except:
        return ""

def try_replace_tile(tiles, x, y, new_tile):
    try:
        tiles[x][y] = new_tile
        return tiles
    except:
        return tiles


def count_dots(tiles: List[List[str]]) -> int:
    result = 0
    for x, row in enumerate(tiles):
        for y, tile in enumerate(row):
            if (tile == '.' and
                    try_get_tile(tiles, x + 1, y) == "." and
                    try_get_tile(tiles, x + 2, y) == "." and
                    try_get_tile(tiles, x, y + 1) == "." and
                    try_get_tile(tiles, x + 1, y + 1) == "." and
                    try_get_tile(tiles, x + 2, y + 1) == "." and
                    try_get_tile(tiles, x, y + 2) == "." and
                    try_get_tile(tiles, x + 1, y + 2) == "." and
                    try_get_tile(tiles, x + 2, y + 2) == "."):
                result += 1
                tiles = try_replace_tile(tiles, x, y, 'X')
                tiles = try_replace_tile(tiles, x+1, y, 'X')
                tiles = try_replace_tile(tiles, x+2, y, 'X')
                tiles = try_replace_tile(tiles, x, y+1, 'X')
                tiles = try_replace_tile(tiles, x+1, y+1, 'X')
                tiles = try_replace_tile(tiles, x+2, y+1, 'X')
                tiles = try_replace_tile(tiles, x, y+2, 'X')
                tiles = try_replace_tile(tiles, x+1, y+2, 'X')
                tiles = try_replace_tile(tiles, x+2, y+2, 'X')
    return result

def replace_not_dots(tiles: List[List[str]]) -> List[List[str]]:
    for x, row in enumerate(tiles):
        for y, tile in enumerate(row):
            if tile != 'P' and tile != '0':
                tiles[x][y] = '.'
    return tiles

def count_tiles_enclosed_by_loop(input: str) -> int:
    tiles = parse_input(input)
    S_location = find_starting_location(tiles)
    connections_to_start = find_connections_to_starting_point(tiles, S_location)
    tiles = replace_starting_location(tiles, S_location, connections_to_start)
    tiles = make_tiles_bigger(tiles)
    S_location = (S_location[0] * 3 + 1, S_location[1] * 3 + 1)
    tiles = mark_path(tiles, S_location, (connections_to_start[0][0] + S_location[0], connections_to_start[0][1] + S_location[1]))
    tiles = mark_sure_zeros(tiles)
    tiles = replace_not_dots(tiles)

    return count_dots(tiles)


assert count_tiles_enclosed_by_loop("""...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........""") == 4

assert count_tiles_enclosed_by_loop("""..........
.S------7.
.|F----7|.
.||....||.
.||....||.
.|L-7F-J|.
.|..||..|.
.L--JL--J.
..........""") == 4

assert count_tiles_enclosed_by_loop(""".F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...""") == 8

assert count_tiles_enclosed_by_loop("""FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L""") == 10

with open("Input.txt") as f:
    print(count_tiles_enclosed_by_loop(f.read()))
