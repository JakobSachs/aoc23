# ------------------------------------------------ #
# Day 08 -- Haunted Wastelanline[0]
# Author: Jakob Sachs
# ------------------------------------------------ #

from itertools import cycle


def greatest_common_divisor(a: int, b: int) -> int:
    while b != 0:
        a, b = b, a % b
    return a


def lowest_common_multiple(a: int, b: int) -> int:
    return a * b // greatest_common_divisor(a, b)


def task1() -> bool:
    lines = input.splitlines()
    instructions = lines[0]

    nodes: dict[str, tuple[str, str]] = {}

    for line in lines[2:]:
        # format: `AAA = (BBB, CCC)`
        # parse each line into a tuple
        name, _, value = line.partition(" = ")
        value = value.strip("()")
        left, right = value.split(", ")
        nodes[name] = (left, right)

    inst = instructions
    current = "AAA"  # start node
    steps = 0
    while True:
        if inst[0] == "L":
            current = nodes[current][0]
        elif inst[0] == "R":
            current = nodes[current][1]
        else:
            logger.error(f"Unknown instruction: {inst[0]}")
            return False

        inst = inst[1:]
        steps += 1
        if inst == "":
            inst = instructions

        if current == "ZZZ":
            break

    logger.info("SOLUTION 1: %s", steps)
    return True


def task2() -> bool:
    lines = input.splitlines()
    instructions = lines[0]

    nodes: dict[str, tuple[str, str]] = {}

    for line in lines[2:]:
        # format: `AAA = (BBB, CCC)`
        # parse each line into a tuple
        name, _, value = line.partition(" = ")
        value = value.strip("()")
        left, right = value.split(", ")
        nodes[name] = (left, right)

    # find cycles
    cycles = {}
    for node in filter(lambda n: n[-1] == "A", nodes):
        steps = 0
        current = node
        for l in cycle(lines[0]):
            if l == "L":
                current = nodes[current][0]
            else:
                current = nodes[current][1]

            instructions = instructions[1:]

            steps += 1
            if current[-1] == "Z":
                break

        cycles[node] = steps

    lowest = 1  # find lowest common multiple of where all the  cycles line up
    for c in cycles.values():
        lowest = lowest_common_multiple(lowest, c)

    logger.info("SOLUTION 2: %s", lowest)

    return True


# ------------------------------------------------ #
# Setup for the challenge (always identical)
# ------------------------------------------------ #

import coloredlogs, logging, os

logger = logging.getLogger(__name__)
input = ""

test_input = """\
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
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
