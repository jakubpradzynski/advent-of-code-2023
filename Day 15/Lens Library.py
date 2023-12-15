# Part One
from collections import defaultdict
from typing import List


def hash(value: str) -> int:
    current_value = 0
    for char in value:
        current_value += ord(char)
        current_value *= 17
        current_value %= 256
    return current_value


def sum_hashes(values: List[str]) -> int:
    return sum(list(map(hash, values)))


def part_one(input: str) -> int:
    return sum_hashes(input.split(","))


assert hash("HASH") == 52

assert part_one("rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7") == 1320

with open("Input.txt") as file:
    print(part_one(file.read()))


# Part Two

def part_two(input: str) -> int:
    boxes = defaultdict(dict)
    for x in input.split(","):
        if "-" in x:
            label = x.split("-")[0]
            hash_value = hash(label)
            boxes[hash_value].pop(label, None)
        if "=" in x:
            label = x.split("=")[0]
            focal_length = x.split("=")[1]
            hash_value = hash(label)
            boxes[hash_value][label] = focal_length
    total_focusing_power = 0
    for hash_value, lens_list in boxes.items():
        for i, lens in enumerate(lens_list.items()):
            total_focusing_power += (hash_value + 1) * (i + 1) * int(lens[1])
    return total_focusing_power


assert part_two("rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7") == 145

with open("Input.txt") as file:
    print(part_two(file.read()))
