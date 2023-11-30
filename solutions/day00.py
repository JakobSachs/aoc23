# ------------------------------------------------ #
# Day 00 -- Template
# Author: Jakob Sachs
# ------------------------------------------------ #


def task1() -> bool:
    print(input)
    return False


def task2() -> bool:
    return False


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
    path = os.path.join(os.path.dirname(__file__), f"../inputs/{__name__}.txt")
    try:
        with open(path, "r") as f:
            input = f.read()
    except FileNotFoundError:
        logger.error(f"Input file for {__name__} not found!")
        return False

    return True
