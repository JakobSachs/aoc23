# Author: Jakob Sachs
# ------------------------------------------------ #
# Day 05: IF You Give A Seed A Fertilizer
# ------------------------------------------------ #

from dataclasses import dataclass


@dataclass(eq=True, frozen=True)
class MapRange:
    start: int
    length: int
    dest_start: int

    def end(self):
        return self.start + self.length - 1

    def contains(self, value: int) -> bool:
        return self.start <= value < self.start + self.length

    def map_single_seed(self, value: int) -> int:
        if not self.contains(value):
            return value
        return self.dest_start + (value - self.start)


def test_map_range():
    assert MapRange(0, 10, 100).map_single_seed(5) == 105
    assert MapRange(0, 10, 100).map_single_seed(0) == 100
    assert MapRange(0, 10, 100).map_single_seed(9) == 109
    assert MapRange(0, 10, 100).map_single_seed(10) == 10


def parse_map(lines: list[str]) -> list[MapRange]:
    map = []
    for ml in lines:
        digits = [int(d) for d in ml.split(" ")]
        if len(digits) != 3:
            raise Exception("Map line has wrong number of digits")
        # first is dest start, second source start, third length
        map.append(MapRange(digits[1], digits[2], digits[0]))
    return map


def test_parse_map():
    assert parse_map(["0 15 37"]) == [MapRange(15, 37, 0)]
    assert parse_map(["0 15 37", "37 52 2"]) == [
        MapRange(15, 37, 0),
        MapRange(52, 2, 37),
    ]


@dataclass(eq=True, frozen=True)
class SeedRange:
    start: int
    length: int

    def end(self):
        return self.start + self.length - 1

    def contains(self, value: int) -> bool:
        return self.start <= value < self.end()

    def map(self, mr: MapRange) -> list["SeedRange"]:
        # Fully outside the map range
        if self.end() < mr.start or self.start > mr.end():
            return [self]

        # Fully inside the map range
        if self.start >= mr.start and self.end() <= mr.end():
            return [SeedRange(mr.map_single_seed(self.start), self.length)]

        # Middle of the range
        if self.start < mr.start and self.end() > mr.end():
            return [
                SeedRange(self.start, mr.start - self.start),
                SeedRange(mr.map_single_seed(mr.start), mr.end() - mr.start + 1),
                SeedRange(mr.end() + 1, self.end() - mr.end()),
            ]

        # Start of the range
        if self.start < mr.start:
            return [
                SeedRange(self.start, mr.start - self.start),
                SeedRange(mr.map_single_seed(mr.start), self.end() - mr.start + 1),
            ]

        # End of the range
        if self.end() > mr.end():
            return [
                SeedRange(mr.map_single_seed(self.start), mr.end() - self.start + 1),
                SeedRange(mr.end() + 1, self.end() - mr.end()),
            ]

        # Should never happen
        raise Exception("Unexpected case in SeedRange.map")


def test_seed_range():
    assert SeedRange(0, 10).map(MapRange(0, 10, 100)) == [SeedRange(100, 10)]

    # test half in
    a = set(SeedRange(0, 10).map(MapRange(0, 5, 100)))
    b = set([SeedRange(100, 5), SeedRange(5, 5)])
    assert a == b

    # test half out
    a = set(SeedRange(0, 10).map(MapRange(5, 5, 100)))
    b = set([SeedRange(0, 5), SeedRange(100, 5)])
    assert a == b

    # test full overlap
    a = set(SeedRange(0, 10).map(MapRange(0, 15, 100)))
    b = set([SeedRange(100, 10)])
    assert a == b

    # test outside
    a = set(SeedRange(0, 10).map(MapRange(20, 5, 100)))
    b = set([SeedRange(0, 10)])
    assert a == b

    # test middle
    a = set(SeedRange(0, 15).map(MapRange(5, 5, 100)))
    b = set([SeedRange(0, 5), SeedRange(100, 5), SeedRange(10, 5)])
    assert a == b


# ------------------------------------------------ #


def task1() -> bool:
    lines = input.splitlines()
    seeds = [int(x) for x in lines[0].split(":")[1].split()]
    maps: list[list[MapRange]] = []
    last_i = -1
    for i, l in enumerate(lines[3:]):
        if "map" in l:
            map_lines = lines[last_i + 4 : i + 2]
            last_i = i
            maps.append(parse_map(map_lines))

    last_lines = lines[last_i + 4 :]
    maps.append(parse_map(last_lines))

    for map in maps:
        new_seeds = []
        for s in seeds:
            mapped = False

            for mr in map:
                if mapped:
                    break
                if mr.contains(s):
                    new_seeds.append(mr.map_single_seed(s))
                    mapped = True

            if not mapped:
                new_seeds.append(s)

        seeds = new_seeds

    logger.info(f"SOLUTION1: {min(seeds)}")
    return True


def task2() -> bool:
    lines = input.splitlines()
    lines = test_input.splitlines()

    seed_digits = [int(x) for x in lines[0].split(":")[1].split()]
    seed_ranges: list[SeedRange] = []

    for i in range(0, len(seed_digits), 2):
        seed_ranges.append(SeedRange(seed_digits[i], seed_digits[i + 1]))

    maps: list[list[MapRange]] = []
    last_i = -1
    for i, l in enumerate(lines[3:]):
        if "map" in l:
            map_lines = lines[last_i + 4 : i + 2]
            last_i = i
            maps.append(parse_map(map_lines))

    last_lines = lines[last_i + 4 :]
    maps.append(parse_map(last_lines))

    for i, map in enumerate(maps):
        print(f"\n\nmap {i}")
        new_seed_ranges = []

        # map each seed range
        for sr in seed_ranges:
            for mr in map:
                new_seed_ranges.extend(sr.map(mr))
                # print(f"mapped {sr} to {new_seed_ranges} with {mr}\n")

        new_seed_ranges.sort(key=lambda x: x.start)
        seed_ranges = new_seed_ranges
        # print(seed_ranges)

    logger.info(f"SOLUTION2: {min([s.start for s in seed_ranges ])}")
    return False


# ------------------------------------------------ #
# Setup for the challenge (always identical)
# ------------------------------------------------ #

import coloredlogs, logging, os

logger = logging.getLogger(__name__)
input = ""
test_input = """seeds: 79 14 55 13

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
56 93 4
"""


def setup():
    # setup logging
    coloredlogs.install(level="DEBUG", logger=logger)

    # read input
    global input
    day = os.path.basename(__file__).split(".")[0]
    path = os.path.join(os.path.dirname(__file__), f"../inputs/{day}.txt")
    try:
        with open(path, "r") as f:
            input = f.read()
    except FileNotFoundError:
        logger.error(f"Input file for {day} not found! [{path}]")
        return False

    return True


if __name__ == "__main__":
    if setup():
        task1()
        task2()
