# ------------------------------------------------ #
# Day 01 -- Trebuchet?!
# Author: Jakob Sachs
# ------------------------------------------------ #


def task1() -> bool:
    values_str = input.split("\n")[:-1]

    # While being more elegant, this is also slower
    # values = [ list(filter(lambda c: c.isdigit(), v)) for v in values_str ]
    values = [[int(char) for char in v if char.isdigit()] for v in values_str]
    v_sum = sum([v[0] * 10 + v[-1] for v in values])

    logger.info(f"SOLUTION1: {v_sum}")
    return True


def task2() -> bool:
    literal_digits = [
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

    values = input.split("\n")[:-1]
    sum = 0
    for v in values:
        digits = []
        for i, c in enumerate(v):
            if c.isdigit():  # same as before basiaclly
                digits.append(int(c))
                continue
            for d, ld in enumerate(literal_digits):
                if v.startswith(ld, i):
                    digits.append(d + 1)
                    break

        sum += digits[0] * 10
        sum += digits[-1]

    logger.info(f"SOLUTION1: {sum}")
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
