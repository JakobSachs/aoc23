# ------------------------------------------------ #
# Day 10 -- Pipe Maze
# Author: Jakob Sachs
# ------------------------------------------------ #

import math

def task1() -> bool:
    lines = input.split("\n")
    #lines = test_input.split("\n")
    # x is going from left to right and y from top to bottom

    # find start position in input
    s = (0,0)
    for x,l in enumerate(lines):
        for y,c in enumerate(l):
            if c == "S":
                s = (x,y)
                break

    d = (0,0)
    # find first step , by checking all 4 directions
    if s[1] < len(lines[s[0]]):
        if lines[s[0]][s[1]+1] in ["-","J","7"]: # right
            d = (0,1)
    if s[0] < len(lines):
        if lines[s[0]+1][s[1]] in ["|","J","L"]: # down
            d = (1,0)
    if s[1] > 0:
        if lines[s[0]][s[1]-1] in ["-","L","F"]: # left
            d = (0,-1)
    if s[0] > 0:
        if lines[s[0]-1][s[1]] in ["|","F","7"]: # up
            d = (-1,0)
    else:
        logger.error("No direction found")
        return False

    # loop until end is reached
    pos = (s[0]+d[0],s[1]+d[1])
    last_pos = s
    path = []
    while pos != s:
        path.append(pos)
        d = (pos[0]-last_pos[0],pos[1]-last_pos[1])
        last_pos = pos
        
        # check all pipe possibilities
        if lines[pos[0]][pos[1]] == "J":
            if d == (0,1): # going right
                pos = (pos[0]-1,pos[1]) # go up
            elif d == (1,0): # going down
                pos = (pos[0],pos[1]-1) # go left
        elif lines[pos[0]][pos[1]] == "L":
            if d == (0,-1): # going left
                pos = (pos[0]-1,pos[1]) # go up
            elif d == (1,0): # going down
                pos = (pos[0],pos[1]+1) # go right
        elif lines[pos[0]][pos[1]] == "F":
            if d == (0,-1): # going left
                pos = (pos[0]+1,pos[1]) # go down
            elif d == (-1,0): # going up
                pos = (pos[0],pos[1]+1) # go right
        elif lines[pos[0]][pos[1]] == "7":
            if d == (0,1): # going right
                pos = (pos[0]+1,pos[1]) 
            elif d == (-1,0): # going up
                pos = (pos[0],pos[1]-1) # go left
        elif lines[pos[0]][pos[1]] == "|":
            if d == (1,0): # going down
                pos = (pos[0]+1,pos[1]) # go down
            elif d == (-1,0): # going up
                pos = (pos[0]-1,pos[1]) # go up
        elif lines[pos[0]][pos[1]] == "-":
            if d == (0,1): # going right
                pos = (pos[0],pos[1]+1) # go right
            elif d == (0,-1): # going left
                pos = (pos[0],pos[1]-1)
        else:
            logger.error(f"No direction found {lines[pos[0]][pos[1]]}")
            return False

    
    
    max_dist = math.ceil(len(path)/2.0)
    logger.info(f"SOLUTION 1: {max_dist}")
    return True


def task2() -> bool:
    return False


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
