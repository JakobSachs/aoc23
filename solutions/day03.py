# ------------------------------------------------ #
# Day 00 -- Template
# Author: Jakob Sachs
# ------------------------------------------------ #

import re
from typing import List, Tuple

OFFSETS = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]


def task1() -> bool:
    lines = input.splitlines()

    # find all numbers with their indices first
    numbers = []
    indices = []
    # also track all non-numbers
    symbols = []
    for l_i, l in enumerate(lines):
        ns = [int(d) for d in re.findall(r"\d+", l)]
        idxs = [(m.start(0), m.end(0)) for m in re.finditer(r"\d+", l)]
        numbers.append(ns)
        indices.append(idxs)

        for i, c in enumerate(l):
            if c not in "0123456789.":
                symbols.append((l_i, i))

    sum = 0
    # iterate over all numbers found and check if theyre valid
    for i, (nrs, ids) in enumerate(zip(numbers, indices)):
        for n, id in zip(nrs, ids):
            valid = False
            # check if theres a non-digit anywhere adjacent along the range
            for o in OFFSETS:
                if valid:
                    break
                for x in range(id[0], id[1]):
                    if (i + o[0], x + o[1]) in symbols:
                        valid = True
                        break

            # valid numbers are added to the sum
            if valid:
                sum += n

    logger.info(f"SOLUTION1: {sum}")

    return True


def task2() -> bool:
    lines = input.splitlines()

    # find all numbers with their indices first
    numbers: list[list[int]] = []
    indices: list[list[Tuple[int, int]]] = []
    # also track all the gears
    gears = []
    for l_i, l in enumerate(lines):
        ns = [int(d) for d in re.findall(r"\d+", l)]
        idxs = [(m.start(0), m.end(0)) for m in re.finditer(r"\d+", l)]
        numbers.append(ns)
        indices.append(idxs)

        for i, c in enumerate(l):
            if c == "*":
                gears.append((l_i, i))

    # iterate over all gears to see if we find two neighboring numbers
    sum = 0
    for g in gears:
        # check if theres a number somewhere adjecent
        neighbors: list[int] = []

        for o in OFFSETS:
            O = (g[0] + o[0], g[1] + o[1])

            # check if we're out of bounds
            if O[0] < 0 or O[1] < 0:
                continue
            if O[0] >= len(lines) or O[1] >= len(lines[0]):
                continue

            # check if theres a number around us
            for y, (nrs, idxs) in enumerate(zip(numbers, indices)):
                for n, (x0, x1) in zip(nrs, idxs):
                    for x in range(x0, x1):
                        if (y, x) == O and n not in neighbors:
                            neighbors.append(n)

        if len(neighbors) == 2:
            sum += neighbors[0] * neighbors[1]

    logger.info(f"SOLUTION2: {sum}")

    return True


# ------------------------------------------------ #
# Setup for the challenge (always identical)
# ------------------------------------------------ #

import coloredlogs, logging, os

logger = logging.getLogger(__name__)
input = ""


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
