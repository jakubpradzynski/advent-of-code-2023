# Part One
import collections
from enum import Enum

TEST_INPUT = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""

card_strengths = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14
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
        self.type = self.get_type()

    @staticmethod
    def parse(text: str) -> "Hand":
        return Hand(text[0:5], int(text[6:].strip()))

    def get_type(self) -> "Type":
        if self.is_five_of_a_kind():
            return Type.FIVE_OF_A_KIND
        elif self.is_four_of_a_kind():
            return Type.FOUR_OF_A_KIND
        elif self.is_full_house():
            return Type.FULL_HOUSE
        elif self.is_three_of_a_kind():
            return Type.THREE_OF_A_KIND
        elif self.is_two_pair():
            return Type.TWO_PAIR
        elif self.is_one_pair():
            return Type.ONE_PAIR
        elif self.is_high_card():
            return Type.HIGH_CARD

    def is_five_of_a_kind(self) -> bool:
        return len(set(self.value)) == 1

    def is_four_of_a_kind(self) -> bool:
        return len(set(self.value)) == 2 and max(collections.Counter(self.value).values()) == 4

    def is_full_house(self) -> bool:
        return len(set(self.value)) == 2 and max(collections.Counter(self.value).values()) == 3

    def is_three_of_a_kind(self) -> bool:
        return len(set(self.value)) == 3 and max(collections.Counter(self.value).values()) == 3

    def is_two_pair(self) -> bool:
        return len(set(self.value)) == 3 and max(collections.Counter(self.value).values()) == 2

    def is_one_pair(self) -> bool:
        return len(set(self.value)) == 4 and max(collections.Counter(self.value).values()) == 2

    def is_high_card(self) -> bool:
        return len(set(self.value)) == 5

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


assert Hand("AAAAA").type == Type.FIVE_OF_A_KIND
assert Hand("AA8AA").type == Type.FOUR_OF_A_KIND
assert Hand("23332").type == Type.FULL_HOUSE
assert Hand("TTT98").type == Type.THREE_OF_A_KIND
assert Hand("23432").type == Type.TWO_PAIR
assert Hand("A23A4").type == Type.ONE_PAIR
assert Hand("23456").type == Type.HIGH_CARD

assert Hand("AKQJT").is_stronger_than(Hand("AKQJ9")) is True
assert Hand("AKQJ9").is_stronger_than(Hand("AKQJT")) is False
assert Hand("AKQJ9").is_stronger_than(Hand("AKQJ9")) is False
assert Hand("AAQJT").is_stronger_than(Hand("AKQJT")) is True

assert Hand.parse("KK677 28 ").value == "KK677"
assert Hand.parse("KK677 28 ").bid == 28


def calculate_total_winnings(input_data: str) -> int:
    hands = [Hand.parse(line) for line in input_data.splitlines()]
    hands.sort()
    result = 0
    for i in range(len(hands)):
        result += hands[i].bid * (i + 1)
    return result


assert calculate_total_winnings(TEST_INPUT) == 6440

with open('Input.txt') as f:
    print(calculate_total_winnings(f.read()))
