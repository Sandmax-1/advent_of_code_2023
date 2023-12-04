import os
from pathlib import Path
from typing import List, Set, Tuple


def parse_input(file_name: str) -> List[Tuple[Set[int], Set[int]]]:
    with open(Path(os.getcwd()) / "day_4" / file_name) as f:
        cards: List[Tuple[Set[int], Set[int]]] = []
        for line in f.readlines():
            line = line.split(":")[1]
            wining_nums = set(
                map(int, line.split("|")[0].strip().replace("  ", " ").split(" "))
            )
            actual_nums = set(
                map(int, line.split("|")[1].strip().replace("  ", " ").split(" "))
            )
            cards.append((wining_nums, actual_nums))
    return cards


def get_scores(cards: List[Tuple[Set[int], Set[int]]]) -> int:
    scores = [2 ** (len(card[0].intersection(card[1])) - 1) for card in cards]
    return sum([score for score in scores if score != 0.5])


def get_copied_cards(cards: List[Tuple[Set[int], Set[int]]]) -> int:
    copied_cards = {num: 1 for num in range(1, len(cards) + 1)}
    for number, card in enumerate(cards):
        card_number = number + 1
        winning_numbers = len(card[0].intersection(card[1]))
        for num in range(
            card_number + 1, min(card_number + winning_numbers, len(cards)) + 1
        ):
            copied_cards[num] = copied_cards[num] + copied_cards[card_number]
    return sum(copied_cards.values())


if __name__ == "__main__":
    cards = parse_input("test_input.txt")

    # part 1
    score = get_scores(cards)
    print(score)

    # part 2
    number_of_cards = get_copied_cards(cards)
    print(number_of_cards)
