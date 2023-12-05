# Part One

TEST_INPUT = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""


class Range:
    def __init__(self,
                 destination_range_start: int,
                 source_range_start: int,
                 range_length: int):
        self.destination_range_start = destination_range_start
        self.source_range_start = source_range_start
        self.range_length = range_length

    def has_corresponding_number(self, value):
        return self.source_range_start <= value < self.source_range_start + self.range_length

    def find_corresponding_number(self, value: int) -> int:
        if self.has_corresponding_number(value):
            return self.destination_range_start + (value - self.source_range_start)
        return value

    @staticmethod
    def parse(text: str) -> "Range":
        text_split = text.split()
        return Range(int(text_split[0]), int(text_split[1]), int(text_split[2]))

    def __str__(self):
        return f"Range({self.destination_range_start}, {self.source_range_start}, {self.range_length})"


assert Range(50, 98, 2).find_corresponding_number(98) == 50
assert Range(50, 98, 2).find_corresponding_number(99) == 51
assert Range(52, 50, 48).find_corresponding_number(50) == 52
assert Range(52, 50, 48).find_corresponding_number(51) == 53


class MapOfTypes:
    def __init__(self,
                 ranges: list[Range]):
        self.ranges = ranges

    def find_corresponding_number(self, value: int) -> int:
        for range in self.ranges:
            if range.has_corresponding_number(value):
                return range.find_corresponding_number(value)
        return value

    @staticmethod
    def parse(text: str) -> "MapOfTypes":
        return MapOfTypes([Range.parse(line) for line in text.splitlines()])

    def __str__(self):
        return "\n".join(str(range) for range in self.ranges)


assert MapOfTypes.parse("50 98 2\n52 50 48").find_corresponding_number(0) == 0
assert MapOfTypes.parse("50 98 2\n52 50 48").find_corresponding_number(1) == 1
assert MapOfTypes.parse("50 98 2\n52 50 48").find_corresponding_number(48) == 48
assert MapOfTypes.parse("50 98 2\n52 50 48").find_corresponding_number(49) == 49
assert MapOfTypes.parse("50 98 2\n52 50 48").find_corresponding_number(50) == 52
assert MapOfTypes.parse("50 98 2\n52 50 48").find_corresponding_number(51) == 53
assert MapOfTypes.parse("50 98 2\n52 50 48").find_corresponding_number(96) == 98
assert MapOfTypes.parse("50 98 2\n52 50 48").find_corresponding_number(97) == 99
assert MapOfTypes.parse("50 98 2\n52 50 48").find_corresponding_number(98) == 50
assert MapOfTypes.parse("50 98 2\n52 50 48").find_corresponding_number(99) == 51


def extract_seeds(lines: list[str]) -> list[int]:
    list_of_seeds = lines[0].split(":")[1].strip()
    return list(map(int, list_of_seeds.split(" ")))


def extract_map(lines: list[str], map_name: str) -> MapOfTypes:
    map_lines = []
    started = False
    for line in lines:
        if started and line != "":
            map_lines.append(line)
        elif line.startswith(f"{map_name} map:"):
            started = True
        elif started and line == "":
            started = False
    return MapOfTypes.parse("\n".join(map_lines))


class Almanac:
    def __init__(self,
                 seeds: list[int],
                 seed_to_soil_map: MapOfTypes,
                 soil_to_fertilizer_map: MapOfTypes,
                 fertilizer_to_water_map: MapOfTypes,
                 water_to_light_map: MapOfTypes,
                 light_to_temperature_map: MapOfTypes,
                 temperature_to_humidity_map: MapOfTypes,
                 humidity_to_location_map: MapOfTypes):
        self.seeds = seeds
        self.seed_to_soil_map = seed_to_soil_map
        self.soil_to_fertilizer_map = soil_to_fertilizer_map
        self.fertilizer_to_water_map = fertilizer_to_water_map
        self.water_to_light_map = water_to_light_map
        self.light_to_temperature_map = light_to_temperature_map
        self.temperature_to_humidity_map = temperature_to_humidity_map
        self.humidity_to_location_map = humidity_to_location_map

    def find_location(self, seed: int) -> int:
        return self.humidity_to_location_map.find_corresponding_number(
            self.temperature_to_humidity_map.find_corresponding_number(
                self.light_to_temperature_map.find_corresponding_number(
                    self.water_to_light_map.find_corresponding_number(
                        self.fertilizer_to_water_map.find_corresponding_number(
                            self.soil_to_fertilizer_map.find_corresponding_number(
                                self.seed_to_soil_map.find_corresponding_number(
                                    seed
                                )
                            )
                        )
                    )
                )
            )
        )

    def find_each_seed_location(self) -> dict[int, int]:
        seed_to_location = {}
        for seed in self.seeds:
            location = self.find_location(seed)
            seed_to_location[seed] = location
        return seed_to_location

    def find_lowest_location_number(self) -> int:
        return min(self.find_each_seed_location().values())

    @staticmethod
    def parse(text: str) -> "Almanac":
        lines = text.splitlines()
        seeds = extract_seeds(lines)
        seed_to_soil_map = extract_map(lines, "seed-to-soil")
        soil_to_fertilizer_map = extract_map(lines, "soil-to-fertilizer")
        fertilizer_to_water_map = extract_map(lines, "fertilizer-to-water")
        water_to_light_map = extract_map(lines, "water-to-light")
        light_to_temperature_map = extract_map(lines, "light-to-temperature")
        temperature_to_humidity_map = extract_map(lines, "temperature-to-humidity")
        humidity_to_location_map = extract_map(lines, "humidity-to-location")
        return Almanac(seeds, seed_to_soil_map, soil_to_fertilizer_map, fertilizer_to_water_map, water_to_light_map, light_to_temperature_map,
                       temperature_to_humidity_map, humidity_to_location_map)


test_almanac = Almanac.parse(TEST_INPUT)
assert test_almanac.find_lowest_location_number() == 35

with open('Input.txt') as f:
    print(Almanac.parse(f.read()).find_lowest_location_number())


# Part Two

def part_two(text: str) -> int:
    lines = text.splitlines()
    seed_ranges = list(map(int, lines[0].split(":")[1].strip().split(" ")))
    maps = [
        extract_map(lines, "seed-to-soil"),
        extract_map(lines, "soil-to-fertilizer"),
        extract_map(lines, "fertilizer-to-water"),
        extract_map(lines, "water-to-light"),
        extract_map(lines, "light-to-temperature"),
        extract_map(lines, "temperature-to-humidity"),
        extract_map(lines, "humidity-to-location")
    ]
    maps.reverse()
    location = 1
    while True:
        seed_for_location = location

        for single_map in maps:
            for single_range in single_map.ranges:
                if single_range.destination_range_start <= seed_for_location < single_range.destination_range_start + single_range.range_length:
                    seed_for_location = single_range.source_range_start + (seed_for_location - single_range.destination_range_start)
                    break

        for x in range(0, len(seed_ranges) - 1, 2):
            if seed_ranges[x] <= seed_for_location < (seed_ranges[x] + seed_ranges[x + 1]):
                return location

        location += 1


assert part_two(TEST_INPUT) == 46

with open('Input.txt') as f:
    print(part_two(f.read()))
