# ------------------------------------------------ #
# Day 00 -- Template
# Author: Jakob Sachs
# ------------------------------------------------ #

def task1() -> None:
    pass

def task2() -> None:
    pass


# Setup function for the challenge (always identical)
import coloredlogs, logging

logger = logging.getLogger(__name__)
input = None

def setup():
    # setup logging
    coloredlogs.install(level='DEBUG', logger=logger)
