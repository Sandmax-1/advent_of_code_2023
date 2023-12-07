import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple, Union

HAND_VALUES = {1: 1, 2: 2, (2, 2): 3, 3: 4, (3, 2): 5, 4: 6, 5: 7}
CARD_VALUES = {
    "2": 1,
    "3": 2,
    "4": 3,
    "5": 4,
    "6": 5,
    "7": 6,
    "8": 7,
    "9": 8,
    "T": 9,
    "J": 10,
    "Q": 11,
    "K": 12,
    "A": 13,
}


@dataclass()
class Hand:
    hand_str: str
    bid: int
    hand_val: int

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Hand):
            return NotImplemented
        if self.hand_val == other.hand_val:
            for ind in range(0, len(self.hand_str)):
                if CARD_VALUES[self.hand_str[ind]] != CARD_VALUES[other.hand_str[ind]]:
                    return (
                        CARD_VALUES[self.hand_str[ind]]
                        < CARD_VALUES[other.hand_str[ind]]  # noqa: W503
                    )

        return self.hand_val < other.hand_val


def parse_input(file_name: str, is_part_two: bool) -> List[Hand]:
    with open(Path(os.getcwd()) / "day_7" / file_name) as f:
        hands = []
        for line in f.readlines():
            hand_str = line.split(" ")[0].strip()
            bid = int(line.split(" ")[1])

            card_counts: Dict[str, int] = {}
            jokers = 0
            for card in hand_str:
                if is_part_two:
                    card_counts, jokers = deal_with_jokers(card, card_counts, jokers)
                else:
                    card_counts[card] = card_counts.get(card, 0) + 1
            sorted_vals = sorted(card_counts.values(), reverse=True)
            high_val: Union[int, Tuple[int, int]] = 0
            if card_counts:
                high_val = sorted_vals[0] + jokers
            else:
                high_val = jokers
            if len(sorted_vals) > 1 and sorted_vals[1] == 2:
                high_val = (high_val, sorted_vals[1])

            hands.append(Hand(hand_str, bid, HAND_VALUES[high_val]))
    return hands


def deal_with_jokers(
    card: str, card_counts: Dict[str, int], jokers: int
) -> Tuple[Dict[str, int], int]:
    if card != "J":
        card_counts[card] = card_counts.get(card, 0) + 1
    else:
        jokers += 1
    return card_counts, jokers


def get_total(hands: List[Hand]) -> int:
    total = 0
    for rank, hand in enumerate(sorted(hands)):
        total += (rank + 1) * hand.bid
    return total


if __name__ == "__main__":
    file_name = "input.txt"
    hands_part_1 = parse_input(file_name, is_part_two=False)
    hands_part_2 = parse_input(file_name, is_part_two=True)

    # part 1
    print(get_total(hands_part_1))

    # part 2
    CARD_VALUES["J"] = 0
    print(get_total(hands_part_2))
