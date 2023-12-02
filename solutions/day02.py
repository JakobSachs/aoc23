# ------------------------------------------------ #
# Day 02 -- Cube Conundrum
# Author: Jakob Sachs
# ------------------------------------------------ #

from functools import reduce
from typing import TypeAlias


Game: TypeAlias = list[list[int]]


def parse_game(line: str) -> tuple[int, Game]:
    id, info = line.split(":")
    id = int(id[5:])

    sets = []
    sets_str = info.split(";")
    for s in sets_str:
        sets.append([0,0,0])
        for c in s.split(","):
            c = c.strip()
            v, k = c.split(" ")
            if k == "red":
                sets[-1][0] = int(v)
                continue
            if k =="green":
                sets[-1][1] = int(v)
                continue
            
            sets[-1][2] = int(v)


    return id, sets


def task1() -> bool:
    constr = [12, 13, 14]

    games = input.splitlines()
    games = [parse_game(g) for g in games]

    sum = 0
    for id, g in games:
        viable = True

        for s in g:
            if not viable:
                break
            for s_c,c_c in zip(s,constr):
                if s_c > c_c:
                    viable=False


        if viable:
            sum += id

    logger.info(f"SOLUTION1: {sum}")
    return True



def task2() -> bool:
    games = input.splitlines()
    games = [parse_game(g) for g in games]

    sum = 0
    for _, g in games:
        min = [ 0, 0,  0]

        for s in g:
            for i,c in enumerate(s):
                min[i] = max(min[i],c)
                

        sum += min[0]*min[1]*min[2]


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
