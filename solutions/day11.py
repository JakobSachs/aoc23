# ------------------------------------------------ #
# Day 00 -- Template
# Author: Jakob Sachs
# ------------------------------------------------ #


def task1() -> bool:
    lines = input.splitlines()
    #lines = test_input.splitlines()

    new_lines = []
    for l in lines:
        new_lines.append(list(l))
        if all([c == "." for c in l]): # duplicate empty lines
            new_lines.append(list(l))
    
    lines = new_lines

    new_cols = []
    for i in range(len(lines[0])):
        new_cols.append([l[i] for l in lines])
        if all([l[i] == "." for l in lines]):
            new_cols.append([l[i] for l in lines])
    
    # flip back to lines
    lines = []
    for i in range(len(new_cols[0])):
        lines.append([l[i] for l in new_cols])
    
    
    # find each galaxy (marked with #)
    galaxies = []
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if lines[y][x] == "#":
                galaxies.append((x,y))
    

    # compute the distance between each galaxy
    distances = {}
    for i in range(len(galaxies)):
        for j in range(i+1, len(galaxies)):
            x1, y1 = galaxies[i]
            x2, y2 = galaxies[j]
            d = abs(x2-x1) + abs(y2-y1)
            distances[(i,j)] = d
            distances[(j,i)] = d
            print(f"{i+1} -> {j+1}: {d}")
    logger.info(f"SOLUTION 1: {sum(distances.values())//2}")

    


    return False


def task2() -> bool:
    lines = input.splitlines()
    lines = test_input.splitlines()

    # find indices of empty lines
    empty_lines = []
    for i in range(len(lines)):
        if all([c == "." for c in lines[i]]):
            empty_lines.append(i)
    # find indices of empty columns
    empty_cols = []
    for i in range(len(lines[0])):
        if all([l[i] == "." for l in lines]):
            empty_cols.append(i)
    

    # find each galaxy (marked with #)
    galaxies = []
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if lines[y][x] == "#":
                galaxies.append((x,y))

    distances = {}
    for i in range(len(galaxies)):
        for j in range(i+1, len(galaxies)):
            x1, y1 = galaxies[i]
            x2, y2 = galaxies[j]
            
            # check how many empty lines and cols are between the two galaxies
            empty_lines_between = 0
            for l in empty_lines:
                if l > y1 and l < y2: # if the empty line is between the two galaxies
                    empty_lines_between += 1 # add one to the counter
            empty_cols_between = 0
            for c in empty_cols: # same for columns
                if c > x1 and c < x2: # if the empty line is between the two galaxies
                    empty_cols_between += 1


            d = abs(x2-x1) + abs(y2-y1)

            # add 10 for each empty line or column between the two galaxies
            d += (empty_lines_between + empty_cols_between)*100
            distances[(i,j)] = d
            distances[(j,i)] = d
            print(f"{i+1} -> {j+1}: {d}")

    logger.info(f"SOLUTION 2: {sum(distances.values())//2}")
    return False


# ------------------------------------------------ #
# Setup for the challenge (always identical)
# ------------------------------------------------ #

import coloredlogs, logging, os

logger = logging.getLogger(__name__)
input = ""
test_input = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""


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
