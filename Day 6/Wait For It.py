# Part One

TEST_INPUT = """Time:      7  15   30
Distance:  9  40  200"""


def extract_numbers(line: str) -> list[int]:
    split = list(filter(lambda x: x != "", line.split(":")[1].strip().split(" ")))
    return [int(num.strip()) for num in split]


def calculate_margin(text: str) -> int:
    lines = text.splitlines()
    times = extract_numbers(lines[0])
    distances = extract_numbers(lines[1])
    numbers_of_ways = []

    for time, distance in zip(times, distances):
        numbers_of_way = 0
        for i in range(0, distance + 1):
            distance_traveled = i * (time - i)
            if distance_traveled > distance:
                numbers_of_way += 1
        numbers_of_ways.append(numbers_of_way)

    result = 1
    for numbers_of_way in numbers_of_ways:
        result *= numbers_of_way
    return result


assert calculate_margin(TEST_INPUT) == 288

with open('Input.txt') as f:
    print(calculate_margin(f.read()))


# Part Two

def extract_time_and_distance(text: str) -> tuple[int, int]:
    lines = text.splitlines()
    times = extract_numbers(lines[0])
    distances = extract_numbers(lines[1])
    return int("".join(map(str, times))), int("".join(map(str, distances)))


def calculate_number_of_ways(text: str) -> int:
    time, distance = extract_time_and_distance(text)
    numbers_of_ways = 0
    for i in range(0, time + 1):
        distance_traveled = i * (time - i)
        if distance_traveled > distance:
            numbers_of_ways += 1
    return numbers_of_ways


assert calculate_number_of_ways(TEST_INPUT) == 71503

with open('Input.txt') as f:
    print(calculate_number_of_ways(f.read()))
