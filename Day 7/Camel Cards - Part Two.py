# Part One
from enum import Enum

TEST_INPUT = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""

card_strengths = {
    "J": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "Q": 11,
    "K": 12,
    "A": 13
}


class Type(Enum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    FULL_HOUSE = 5
    FOUR_OF_A_KIND = 6
    FIVE_OF_A_KIND = 7


class Hand:
    def __init__(self, value: str, bid: int = 0):
        self.value = value
        self.bid = bid
        self.letters_counts = self.counts_letters()
        self.jokers_count = self.value.count("J")
        self.sorted_letters_counts = sorted(self.letters_counts.values())
        self.type = self.get_type()

    @staticmethod
    def parse(text: str) -> "Hand":
        return Hand(text[0:5], int(text[6:].strip()))

    def get_type(self) -> "Type":
        if self.sorted_letters_counts == [5]:
            return Type.FIVE_OF_A_KIND
        elif self.sorted_letters_counts == [1, 4]:
            if self.jokers_count > 0:
                return Type.FIVE_OF_A_KIND
            else:
                return Type.FOUR_OF_A_KIND
        elif self.sorted_letters_counts == [2, 3]:
            if self.jokers_count > 0:
                return Type.FIVE_OF_A_KIND
            else:
                return Type.FULL_HOUSE
        elif self.sorted_letters_counts == [1, 1, 3]:
            if self.jokers_count > 0:
                return Type.FOUR_OF_A_KIND
            else:
                return Type.THREE_OF_A_KIND
        elif self.sorted_letters_counts == [1, 2, 2]:
            if self.jokers_count == 1:
                return Type.FULL_HOUSE
            elif self.jokers_count == 2:
                return Type.FOUR_OF_A_KIND
            else:
                return Type.TWO_PAIR
        elif self.sorted_letters_counts == [1, 1, 1, 2]:
            if self.jokers_count > 0:
                return Type.THREE_OF_A_KIND
            else:
                return Type.ONE_PAIR
        elif self.sorted_letters_counts == [1, 1, 1, 1, 1]:
            if self.jokers_count > 0:
                return Type.ONE_PAIR
            else:
                return Type.HIGH_CARD

    def counts_letters(self) -> dict[str, int]:
        result = {}
        for letter in set(self.value):
            result[letter] = self.value.count(letter)
        return result

    def is_stronger_than(self, other: "Hand") -> bool:
        if self.type.value > other.type.value:
            return True
        elif self.type.value < other.type.value:
            return False
        elif self.type.value == other.type.value:
            for i in range(len(self.value)):
                if card_strengths[self.value[i]] > card_strengths[other.value[i]]:
                    return True
                if card_strengths[self.value[i]] < card_strengths[other.value[i]]:
                    return False
        return False

    def __cmp__(self, other):
        if self.is_stronger_than(other):
            return 1
        elif other.is_stronger_than(self):
            return -1
        else:
            return 0

    def __eq__(self, other):
        return self.__cmp__(other) == 0

    def __lt__(self, other):
        return self.__cmp__(other) == -1

    def __gt__(self, other):
        return self.__cmp__(other) == 1

    def __str__(self):
        return f"{self.type.name} {self.value} {self.bid}"


assert Hand("32T3K").type == Type.ONE_PAIR
assert Hand("KK677").type == Type.TWO_PAIR
assert Hand("T55J5").type == Type.FOUR_OF_A_KIND
assert Hand("KTJJT").type == Type.FOUR_OF_A_KIND
assert Hand("QQQJA").type == Type.FOUR_OF_A_KIND

assert Hand("KK677").is_stronger_than(Hand("32T3K"))
assert Hand("T55J5").is_stronger_than(Hand("KK677"))
assert Hand("QQQJA").is_stronger_than(Hand("T55J5"))
assert Hand("KTJJT").is_stronger_than(Hand("QQQJA"))


def calculate_total_winnings(input_data: str) -> int:
    hands = [Hand.parse(line) for line in input_data.splitlines()]
    hands.sort()
    result = 0
    for i in range(len(hands)):
        result += hands[i].bid * (i + 1)
    return result


assert calculate_total_winnings(TEST_INPUT) == 5905

assert Hand("32T3K").is_stronger_than(Hand("T55J5")) == False

with open('Input.txt') as f:
    print(calculate_total_winnings(f.read()))
