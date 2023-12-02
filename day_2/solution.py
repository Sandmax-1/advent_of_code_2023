import os
from functools import reduce
from operator import mul
from pathlib import Path
from typing import Dict


def parse_input(file_name: str) -> Dict[int, Dict[str, int]]:
    games = {}
    with open(Path(os.getcwd()) / "day_2" / file_name, "r") as f:
        for game in f.readlines():
            colours: Dict[str, int] = {}
            game_number = game.split(":")[0].split(" ")[-1]
            for round in game.split(":")[1].split(";"):
                for revealed in round.split(","):
                    revealed = revealed.strip()
                    colour = revealed.split(" ")[1]
                    num = int(revealed.split(" ")[0])
                    if colours.get(colour, 0) < num:
                        colours[colour] = num
            games[int(game_number)] = colours
    return games


def evaluate_games(games: Dict[int, Dict[str, int]], maximums: Dict[str, int]) -> int:
    game_sum = 0
    for game_num, game in games.items():
        possible_game = True
        for colour, max_val in maximums.items():
            if game[colour] > max_val:
                possible_game = False
        if possible_game:
            game_sum += game_num
    return game_sum


def get_powers(games: Dict[int, Dict[str, int]]) -> int:
    sum_of_powers = 0
    for game in games.values():
        power = reduce(mul, list(game.values()))
        sum_of_powers += power
    return sum_of_powers


if __name__ == "__main__":
    games = parse_input("input.txt")
    # part 1
    game_sum = evaluate_games(games, {"red": 12, "green": 13, "blue": 14})
    print(game_sum)
    # part 2
    sum_of_powers = get_powers(games)
    print(sum_of_powers)
