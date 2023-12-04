# Part One
import re


def extract_numbers(values_in_string: str) -> list[int]:
    return list(map(lambda x: int(x.strip()), re.findall(r'\S+', values_in_string)))


def calculate_points_from_scratchcard(line: str) -> int:
    card, winning_numbers = line.split("|")
    winning_numbers = extract_numbers(winning_numbers)
    card_id, card_numbers = card.split(":")
    card_numbers = extract_numbers(card_numbers)
    matches = set(card_numbers) & set(winning_numbers)
    score = 0
    for num in matches:
        if score == 0:
            score = 1
        else:
            score *= 2
    return score


assert calculate_points_from_scratchcard("Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53") == 8
assert calculate_points_from_scratchcard("Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19") == 2
assert calculate_points_from_scratchcard("Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1") == 2
assert calculate_points_from_scratchcard("Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83") == 1
assert calculate_points_from_scratchcard("Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36") == 0
assert calculate_points_from_scratchcard("Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11") == 0

with open('Input.txt') as f:
    lines = f.readlines()
    total_points = 0
    for line in lines:
        total_points += calculate_points_from_scratchcard(line)
    print(total_points)

# Part Two

results = {}


def total_scratchcards(text: str) -> int:
    lines = text.splitlines()

    def process_line(idx: int, line: str):
        card, winning_numbers = line.split("|")
        winning_numbers = extract_numbers(winning_numbers)
        card_id, card_numbers = card.split(":")
        card_numbers = extract_numbers(card_numbers)
        matches = set(card_numbers) & set(winning_numbers)
        results[card_id] = results[card_id] + 1 if card_id in results else 1
        for i in range(1, len(matches) + 1):
            process_line(idx + i, lines[idx + i])

    for idx, line in enumerate(lines):
        process_line(idx, line)

    total = 0
    for card_id, instances in results.items():
        total += instances
    return total


assert total_scratchcards("""Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11""") == 30

results = {}

with open('Input.txt') as f:
    print(total_scratchcards(f.read()))
