# ------------------------------------------------ #
# Day 04 -- Scratchcards
# Author: Jakob Sachs
# ------------------------------------------------ #

from typing import Tuple


def parse_card(line: str) -> Tuple[int,Tuple[list[int],list[int]]]:
    id = int(line.split(":")[0].replace("Card",""))
    sections = line.split(":")[1].split("|")
    winning = [int(n) for n in sections[0].split(" ") if len(n.strip()) > 0]
    have = [int(n) for n in sections[1].split(" ") if len(n.strip()) > 0]
    return id,(winning,have)

def task1() -> bool:
    cards = [ parse_card(l) for l in input.splitlines() if len(l) > 0]
    
    # evalute the points for each card
    total = 0
    for _,(wins,haves) in cards:
        winnings = 0 
        for h in haves:
            if h in wins:
                winnings += 1
        total += 2**(winnings - 1) if winnings > 0 else 0
    
    logger.info(f"SOLUTION1: {total}")
    return True


def task2() -> bool:
    cards = [ parse_card(l) for l in input.splitlines()]
    counts = [ 1 for _ in range(len(cards))]

    for id,(wins,haves) in cards:
        # find out how many wins each card has
        winnings = 0 
        for h in haves:
            if h in wins:
                winnings += 1
        
        for i in range(winnings):
            counts[id + i] += counts[id-1]

    logger.info(f"SOLUTION2: {sum(counts)}")
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
