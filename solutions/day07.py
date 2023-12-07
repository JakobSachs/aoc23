# ------------------------------------------------ #
# Day 07 -- Camel Cards
# Author: Jakob Sachs
# ------------------------------------------------ #
from dataclasses import dataclass
from enum import Enum
import enum


class Card(Enum):
    C_A = 13
    C_K = 12
    C_Q = 11
    C_J = 10
    C_T = 9
    C_9 = 8
    C_8 = 7
    C_7 = 6
    C_6 = 5
    C_5 = 4
    C_4 = 3
    C_3 = 2
    C_2 = 1
    C_JOKER = 0

    def __lt__(self, other):
        return self.value < other.value

    def __eq__(self, other):
        return self.value == other.value

    @staticmethod
    def from_str(s: str) -> "Card":
        if s == "A":
            return Card.C_A
        elif s == "K":
            return Card.C_K
        elif s == "Q":
            return Card.C_Q
        elif s == "J":
            return Card.C_J
        elif s == "T":
            return Card.C_T
        elif s == "X":
            return Card.C_JOKER
        if int(s) > 10:
            raise ValueError("Invalid card value")
        else:
            return Card(int(s) - 1)

    def __hash__(self) -> int:
        return super().__hash__()


def test_Card_from_str():
    assert Card.from_str("A") == Card.C_A
    assert Card.from_str("K") == Card.C_K
    assert Card.from_str("Q") == Card.C_Q
    assert Card.from_str("J") == Card.C_J
    assert Card.from_str("X") == Card.C_JOKER
    assert Card.from_str("T") == Card.C_T
    assert Card.from_str("9") == Card.C_9
    assert Card.from_str("8") == Card.C_8
    assert Card.from_str("7") == Card.C_7
    assert Card.from_str("6") == Card.C_6
    assert Card.from_str("5") == Card.C_5
    assert Card.from_str("4") == Card.C_4
    assert Card.from_str("3") == Card.C_3
    assert Card.from_str("2") == Card.C_2


def test_Card_lt():
    assert Card.C_2 < Card.C_3
    assert Card.C_4 < Card.C_5
    assert Card.C_6 < Card.C_7
    assert Card.C_8 < Card.C_9
    assert Card.C_T < Card.C_J
    assert Card.C_Q < Card.C_K
    assert Card.C_K < Card.C_A


class Type(Enum):
    FIVE_OF_A_KIND = 10
    FOUR_OF_A_KIND = 9
    FULL_HOUSE = 8
    THREE_OF_A_KIND = 7
    TWO_PAIRS = 6
    ONE_PAIR = 5
    HIGH_CARD = 4

class Evaluation:
    type: Type
    suit: Card
    cards: list[Card]
    
    def __init__(self,hand: "Hand") -> None:
        self.cards = hand.cards

        if hand.counts[0][1] == 5:
            self.type = Type.FIVE_OF_A_KIND
            self.suit = hand.counts[0][0]
            
        elif hand.counts[0][1] == 4:
            self.type = Type.FOUR_OF_A_KIND
            self.suit = hand.counts[0][0]
        elif hand.counts[0][1] == 3:
            if hand.counts[1][1] == 2:
                self.type = Type.FULL_HOUSE
                self.suit = hand.counts[0][0]
                self.second_suit = hand.counts[1][0]
            else:
                self.type = Type.THREE_OF_A_KIND
                self.suit = hand.counts[0][0]
        elif hand.counts[0][1] == 2:
            if hand.counts[1][1] == 2:
                self.type = Type.TWO_PAIRS
                self.suit = hand.counts[0][0]
                self.second_suit = hand.counts[1][0]
            else:
                self.type = Type.ONE_PAIR
                self.suit = hand.counts[0][0]
        else:
            self.type = Type.HIGH_CARD
            self.suit = hand.counts[0][0]

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Evaluation):
            return NotImplemented
        
        if self.type != __value.type:
            return False

        if self.suit != __value.suit:
            return False

        for i in range(5):
            if self.cards[i] != __value.cards[i]:
                return False

        return True

    def __lt__(self, __value: object) -> bool:
        if not isinstance(__value, Evaluation):
            return NotImplemented
        if self.type.value != __value.type.value:
            return self.type.value < __value.type.value
        for i in range(5):
            if self.cards[i].value != __value.cards[i].value:
                return self.cards[i].value < __value.cards[i].value
        return False
    
    def __repr__(self) -> str:
        return f"{self.type.name} {self.suit.name} {self.cards}"

        

@dataclass
class Hand:
    cards: list[Card]

    def __post_init__(self):
        counts = {}
        for c in self.cards:
            if c in counts:
                counts[c] += 1
            else:
                counts[c] = 1

        self.counts = list(zip(counts.keys(), counts.values()))
        self.counts.sort(key=lambda x: (x[1], x[0].value), reverse=True)

        # see if we have any jokers
        if Card.C_JOKER in counts:
            # find the best card to be
            best_card = Card.C_2
            best_count = 0
            for c in counts.keys():
                if c == Card.C_JOKER:
                    continue
                if counts[c] > best_count:
                    best_card = c
                    best_count = counts[c]

            # if all jokers:
            if best_count == 0:
                best_card = Card.C_A
                best_count = 5
                self.counts = [(best_card, best_count)]
            else: # if not all jokers, add jokers to count
                idx = self.counts.index((best_card, best_count))
                self.counts[idx] = (best_card, best_count + counts[Card.C_JOKER])
            
            # remove jokers from counts
            for i,c in enumerate(self.counts):
                if c[0] == Card.C_JOKER:
                    self.counts.pop(i)
                    break


    


            # sort again
            self.counts.sort(key=lambda x: (x[1], x[0].value), reverse=True)


    def evaluate(self) -> Evaluation:
        return Evaluation(self)

def test_hand():
    h = Hand([Card.C_2, Card.C_2, Card.C_2, Card.C_2, Card.C_2])
    assert h.evaluate().type == Type.FIVE_OF_A_KIND

    h = Hand([Card.C_2, Card.C_2, Card.C_2, Card.C_2, Card.C_3])
    assert h.evaluate().type == Type.FOUR_OF_A_KIND

    h = Hand([Card.C_2, Card.C_2, Card.C_2, Card.C_3, Card.C_3])
    assert h.evaluate().type == Type.FULL_HOUSE

    h = Hand([Card.C_2, Card.C_2, Card.C_2, Card.C_3, Card.C_4])
    assert h.evaluate().type == Type.THREE_OF_A_KIND

    h = Hand([Card.C_2, Card.C_2, Card.C_3, Card.C_3, Card.C_4])
    assert h.evaluate().type == Type.TWO_PAIRS

    h =  Hand([Card.C_2, Card.C_2, Card.C_3, Card.C_4, Card.C_5])
    assert h.evaluate().type == Type.ONE_PAIR

    h = Hand([Card.C_2, Card.C_3, Card.C_4, Card.C_5, Card.C_6])
    assert h.evaluate().type == Type.HIGH_CARD

def task1() -> bool:
    games_str = input.splitlines()
    #games_str = test_input.splitlines()
    games: list[tuple[Evaluation, int]] = [
        (Hand([Card.from_str(c) for c in g.split(" ")[0]]).evaluate(), int(g.split(" ")[1]))
        for g in games_str
    ]
    games.sort(key=lambda x: x[0])

    winnings = 0 

    for r,(g,bid) in enumerate(games):
        winnings += bid*(r+1)
    
    logger.info(f"SOLUTION 1: {winnings}")
    return True


def task2() -> bool:
    games_str = input.splitlines()
    #games_str = test_input.splitlines()
    games: list[tuple[Evaluation, int]] = [
        (Hand([Card.from_str(c.replace("J","X")) for c in g.split(" ")[0]]).evaluate(), int(g.split(" ")[1]))
        for g in games_str
    ]
    games.sort(key=lambda x: x[0])

    winnings = 0 

    for r,(_,bid) in enumerate(games):
        winnings += bid*(r+1)
    
    logger.info(f"SOLUTION 2: {winnings}")
    return True


# ------------------------------------------------ #
# Setup for the challenge (always identical)
# ------------------------------------------------ #

import coloredlogs, logging, os

logger = logging.getLogger(__name__)
input = ""
test_input = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""


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
