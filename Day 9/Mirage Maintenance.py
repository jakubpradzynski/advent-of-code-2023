# Part One
TEST_INPUT = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""


def prediction_of(numbers: list[int]) -> int:
    if all(x == 0 for x in numbers):
        return 0
    diffs = []
    for i in range(len(numbers) - 1):
        diffs.append(numbers[i + 1] - numbers[i])
    return numbers[-1] + prediction_of(diffs)


def sum_of_next_values_for_each_history(input: str) -> int:
    result = 0
    for line in input.splitlines():
        numbers = list(map(int, line.split(" ")))
        result += prediction_of(numbers)
    return result


assert sum_of_next_values_for_each_history(TEST_INPUT) == 114

with open('Input.txt') as f:
    print(sum_of_next_values_for_each_history(f.read()))


# Part Two
def prediction_of(numbers: list[int]) -> int:
    if all(x == 0 for x in numbers):
        return 0
    diffs = []
    for i in range(len(numbers) - 1):
        diffs.append(numbers[i + 1] - numbers[i])
    return numbers[0] - prediction_of(diffs)


def sum_of_next_values_for_each_history(input: str) -> int:
    result = 0
    for line in input.splitlines():
        numbers = list(map(int, line.split(" ")))
        result += prediction_of(numbers)
    return result


assert sum_of_next_values_for_each_history(TEST_INPUT) == 2

with open('Input.txt') as f:
    print(sum_of_next_values_for_each_history(f.read()))
