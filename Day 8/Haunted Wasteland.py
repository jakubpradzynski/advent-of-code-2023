# Part One
import math
from typing import List

TEST_INPUT_1 = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""

TEST_INPUT_2 = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""


class NetworkNode:
    def __init__(self,
                 starting: str,
                 left: str,
                 right: str):
        self.starting = starting
        self.left = left
        self.right = right
        self.left_node = None
        self.right_node = None

    def has_last_letter(self, letter: str) -> bool:
        return self.starting[-1] == letter

    def set_left_node(self, left: "NetworkNode"):
        self.left_node = left

    def set_right_node(self, right: "NetworkNode"):
        self.right_node = right

    @staticmethod
    def parse(line: str) -> "NetworkNode":
        starting, directions = line.split(" = ")
        left, right = directions.split(", ")
        return NetworkNode(starting.strip(), left.strip().lstrip("("), right.strip().rstrip(")"))

    def __str__(self):
        return f"{self.starting} -> {self.left}, {self.right}"


def find_node(nodes: List[NetworkNode], name: str) -> NetworkNode:
    for node in nodes:
        if node.starting == name:
            return node


def fill_nodes_connections(nodes: List[NetworkNode]):
    for node in nodes:
        left_node = find_node(nodes, node.left)
        right_node = find_node(nodes, node.right)
        node.set_left_node(left_node)
        node.set_right_node(right_node)


def calculate_steps(input: str) -> int:
    lines = input.splitlines()
    instructions, network = lines[0], lines[2:]
    nodes = list(map(lambda line: NetworkNode.parse(line), network))
    fill_nodes_connections(nodes)
    aaa_node = find_node(nodes, "AAA")
    current_node = aaa_node
    is_zzz_node = False
    steps = 0
    while not is_zzz_node:
        for direction in instructions:
            steps += 1
            if direction == "R":
                current_node = current_node.right_node
            elif direction == "L":
                current_node = current_node.left_node
            if current_node.starting == "ZZZ":
                is_zzz_node = True
                break
    return steps


assert calculate_steps(TEST_INPUT_1) == 2
assert calculate_steps(TEST_INPUT_2) == 6

with open("Input.txt") as f:
    print(calculate_steps(f.read()))

# Part Two

TEST_INPUT_3 = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""


def find_nodes_with_last_letter(nodes: List[NetworkNode], letter: str) -> List[NetworkNode]:
    found_nodes = []
    for node in nodes:
        if node.has_last_letter(letter):
            found_nodes.append(node)
    return found_nodes


def calculate_steps(input: str) -> int:
    lines = input.splitlines()
    instructions, network = lines[0], lines[2:]
    nodes = list(map(lambda line: NetworkNode.parse(line), network))
    fill_nodes_connections(nodes)
    current_nodes = find_nodes_with_last_letter(nodes, "A")
    steps_from_all_nodes = []
    for n in current_nodes:
        current_node = n
        is_end = False
        steps = 0
        while not is_end:
            for direction in instructions:
                steps += 1
                if direction == "R":
                    current_node = current_node.right_node
                elif direction == "L":
                    current_node = current_node.left_node
                if current_node.has_last_letter("Z"):
                    is_end = True
                    steps_from_all_nodes.append(steps)
                    break
    return math.lcm(*steps_from_all_nodes)


assert calculate_steps(TEST_INPUT_3) == 6

with open("Input.txt") as f:
    print(calculate_steps(f.read()))
