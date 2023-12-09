# ------------------------------------------------ #
# Day 09 -- Mirage Maintenance
# Author: Jakob Sachs
# ------------------------------------------------ #

from itertools import groupby
from typing_extensions import NewType


def get_differences(history: list[int]) -> list[int]:
    differences = []
    for i in range(1, len(history)):
        differences.append(history[i] - history[i - 1])
    return differences


def all_equal(iterable):
    g = groupby(iterable)
    return next(g, True) and not next(g, False)


def task1() -> bool:
    lines = input.splitlines()
    # lines = test_input.splitlines()
    histories = [[int(c) for c in l.split(" ")] for l in lines]

    new_values = []

    for hist in histories:
        sequences = [hist]

        # calculate differences until diff is zero
        while not all_equal(sequences[-1]):
            diffs = get_differences(sequences[-1])
            sequences.append(diffs)

        # extrapolate last number (reverse)
        for i in range(len(sequences) - 1, 0, -1):
            sequences[i - 1].append(sequences[i - 1][-1] + sequences[i][-1])
            if i == 1:
                new_values.append(sequences[i - 1][-1])

    logger.info(f"SOLUTION 1: {sum(new_values)}")
    return True


def task2() -> bool:
    lines = input.splitlines()
    # lines = test_input.splitlines()
    histories = [[int(c) for c in l.split(" ")] for l in lines]

    new_values = []

    for hist in histories:
        sequences = [hist]

        # calculate differences until diff is zero
        while not all_equal(sequences[-1]):
            diffs = get_differences(sequences[-1])
            sequences.append(diffs)

        # extrapolate first number (forward)
        for i in range(len(sequences) - 1, 0, -1):
            sequences[i - 1].insert(0, sequences[i - 1][0] - sequences[i][0])
            if i == 1:
                new_values.append(sequences[i - 1][0])
    logger.info(f"SOLUTION 2: {sum(new_values)}")
    return True


# ------------------------------------------------ #
# Setup for the challenge (always identical)
# ------------------------------------------------ #

import coloredlogs, logging, os

logger = logging.getLogger(__name__)
input = ""
test_input = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""


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
