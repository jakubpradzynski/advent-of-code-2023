# Part One

class Subset:
    def __init__(self, blue_cubes: int, green_cubes: int, red_cubes: int):
        self.blue_cubes = blue_cubes
        self.green_cubes = green_cubes
        self.red_cubes = red_cubes

    @staticmethod
    def parse(text: str):
        blue_cubes = 0
        green_cubes = 0
        red_cubes = 0
        for t in text.split(","):
            t = t.strip()
            amount, color = t.split(" ")
            amount = int(amount)
            if color == "blue":
                blue_cubes = amount
            elif color == "green":
                green_cubes = amount
            elif color == "red":
                red_cubes = amount
        return Subset(blue_cubes, green_cubes, red_cubes)

    def __str__(self):
        return f"Blue Cubes: {self.blue_cubes}, Green Cubes: {self.green_cubes}, Red Cubes: {self.red_cubes}"


class Game:
    def __init__(self, id: int, subsets: list[Subset]):
        self.id = id
        self.subsets = subsets

    @staticmethod
    def parse(text: str):
        game, subset_texts = text.split(":")
        game_id = int(game.split(" ")[1])
        subsets = []
        for subset in subset_texts.split(";"):
            subsets.append(Subset.parse(subset.strip()))
        return Game(game_id, subsets)

    def is_possible(self, blue_cubes_in_bag: int, green_cubes_in_bag: int, red_cubes_in_bag: int) -> bool:
        max_blue_cubes = max(subset.blue_cubes for subset in self.subsets)
        max_green_cubes = max(subset.green_cubes for subset in self.subsets)
        max_red_cubes = max(subset.red_cubes for subset in self.subsets)
        return (max_blue_cubes <= blue_cubes_in_bag and
                max_green_cubes <= green_cubes_in_bag and
                max_red_cubes <= red_cubes_in_bag)

    def minimal_bag(self) -> tuple[int, int, int]:
        max_blue_cubes = max(subset.blue_cubes for subset in self.subsets)
        max_green_cubes = max(subset.green_cubes for subset in self.subsets)
        max_red_cubes = max(subset.red_cubes for subset in self.subsets)
        return max_blue_cubes, max_green_cubes, max_red_cubes

    def __str__(self):
        return f"ID: {self.id} " + " ".join(str(subset) + "" for subset in self.subsets)


assert (Game.parse("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green")
        .is_possible(14, 13, 12))
assert (Game.parse("Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue")
        .is_possible(14, 13, 12))
assert not (Game.parse("Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red")
            .is_possible(14, 13, 12))
assert not (Game.parse("Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red")
            .is_possible(14, 13, 12))
assert (Game.parse("Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green")
        .is_possible(14, 13, 12))

with open('Input.txt') as f:
    lines = f.readlines()
    sum_of_ids = 0
    for line in lines:
        game = Game.parse(line)
        if game.is_possible(14, 13, 12):
            sum_of_ids += game.id
    print(sum_of_ids)

# Part Two

assert Game.parse("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green").minimal_bag() == (6, 2, 4)
assert Game.parse("Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue").minimal_bag() == (4, 3, 1)
assert Game.parse("Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red").minimal_bag() == (6, 13, 20)
assert Game.parse("Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red").minimal_bag() == (15, 3, 14)
assert Game.parse("Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green").minimal_bag() == (2, 3, 6)

with open('Input.txt') as f:
    lines = f.readlines()
    powers = 0
    for line in lines:
        game = Game.parse(line)
        min_bag = game.minimal_bag()
        power = min_bag[0] * min_bag[1] * min_bag[2]
        powers += power
    print(powers)
