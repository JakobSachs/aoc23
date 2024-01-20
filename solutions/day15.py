# ------------------------------------------------ #
# Day 15 -- Lens Library
# Author: Jakob Sachs
# ------------------------------------------------ #


from typing import Tuple


def hash(input: str) -> int:
    val = 0
    for c in input:
        val += ord(c)
        val *= 17
        val %= 256
    return val


def task1() -> bool:
    sequence = input.strip().split(",")
    hashes = map(hash, sequence)
    hash_sum = sum(hashes)

    logger.info("SOLUTION 1: %s", hash_sum)
    return True


def task2() -> bool:
    boxes: list[list[Tuple[int, str]]] = [[] for _ in range(256)]
    sequence = input.strip().split(",")
    labels = [s[:-1] if "-" in s else s.split("=")[0] for s in sequence]
    vals = [-1 if "-" in s else int(s.split("=")[1]) for s in sequence]
    operation = ["-" if "-" in s else "=" for s in sequence]

    for l, v, op in zip(labels, vals, operation):
        h = hash(l)
        if op == "-":
            # check if lens already in box
            present = list(filter(lambda lens: lens[1] == l, boxes[h]))
            if len(present) > 0:
                boxes[h].remove(present[0])
        else:
            # check if lens already in box
            present = list(filter(lambda lens: lens[1] == l, boxes[h]))
            if len(present) == 0:
                boxes[h].append((v, l))
            else:
                idx = boxes[h].index(present[0])
                boxes[h][idx] = (v, l)

    total = sum(
        (box_index + 1) * (item_index + 1) * item[0]
        for box_index, box in enumerate(boxes)
        for item_index, item in enumerate(box)
    )

    logger.info("SOLUTION 2: %s", total)

    return False


# ------------------------------------------------ #
# Setup for the challenge (always identical)
# ------------------------------------------------ #

import coloredlogs, logging, os

logger = logging.getLogger(__name__)
input = ""
test_input = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"


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
