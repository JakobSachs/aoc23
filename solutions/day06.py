# ------------------------------------------------ #
# Day 06 -- Wait For It 
# Author: Jakob Sachs
# ------------------------------------------------ #

Race = tuple[int,int] # time, distance

def simulate_race(race:Race, waiting:int) -> bool:
    time,dist = race
    if time < waiting:
        raise ValueError("Race time is smaller than waiting time")

    # check if the waiting time is enough
    return waiting * (time - waiting) > dist

def task1() -> bool:
    lines = input.splitlines()
    times = [int(x) for x in lines[0].split(" ") if x.isdigit()]
    distances = [int(x) for x in lines[1].split(" ") if x.isdigit()]

    prod = 1
    for (t,d) in zip(times,distances):
        ways = 0 
        for i in range(t):
            if simulate_race((t,d),i+1):
                ways += 1
        prod *= ways
    
    logger.info(f"SOLUTION 1: {prod}")
    return False


def task2() -> bool:
    lines = input.splitlines()
    # im just hardcoding this one cause im lazy

    # test
    # time = 71530
    # distance = 940200

    time = 56717999
    distance = 334113513502430

    
    lower = 0
    # find lower bound using binary search
    low, high = 0, time
    while low < high:
        mid = (low + high) // 2
        if simulate_race((time, distance), mid):
            lower = mid
            high = mid
        else:
            low = mid + 1

    
    upper = 0
    # find upper bound
    low, high = 0, time
    while low < high:
        mid = (low + high) // 2
        if simulate_race((time, distance), mid):
            upper = mid
            low = mid +1
        else:
            high = mid 
    
    logger.info(f"SOLUTION 2: {upper - lower + 1}")
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
