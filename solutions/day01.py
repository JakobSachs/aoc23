# ------------------------------------------------ #
# Day 01 -- Trebuchet?!
# Author: Jakob Sachs
# ------------------------------------------------ #


import enum


def task1() -> bool:
    values = input.split("\n")
    sum = 0
    for v in values:
        if len(v) == 0:
            continue
        digits = list(filter(lambda c: c.isdigit(), v))
        sum += int(digits[0]) * 10
        sum += int(digits[-1])

    logger.info(f"SOLUTION1: {sum}")
    return True


def task2() -> bool:
    literaL_digits = [
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
    ]

    values = input.split("\n")
    sum = 0
    for v in values:
        if len(v) == 0:
            continue
        digits = []
        for i, c in enumerate(v):
            if c.isdigit():
                digits.append(int(c))
                continue

            for d, ld in enumerate(literaL_digits):
                res = v.find(ld, i)
                if res == i:
                    digits.append(d + 1)

        sum += digits[0] * 10
        sum += digits[-1]

    logger.info(f"SOLUTION1: {sum}")
    return True


# ------------------------------------------------ #
# Setup for the challenge (always identical)
# ------------------------------------------------ #

import coloredlogs, logging, os

logger = logging.getLogger(__name__)
input = None


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
