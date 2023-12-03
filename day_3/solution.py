import os
from dataclasses import dataclass
from functools import reduce
from operator import mul
from pathlib import Path
from typing import List, Tuple, Union


@dataclass()
class Position:
    x1: int
    x2: int
    y1: int
    y2: int
    value: Union[int, str]

    def __repr__(self) -> str:
        return str(f"Position(x={self.x1}, y={self.y1}, val={self.value})")

    def __hash__(self) -> int:
        return hash((self.x1, self.x2, self.y1, self.y2, self.value))


def parse_input(file_name: str) -> Tuple[List[Position], List[Position]]:
    numbers: List[Position] = []
    symbols: List[Position] = []
    with open(Path(os.getcwd()) / "day_3" / file_name, "r") as f:
        stop = 0
        for y, line in enumerate(f.readlines()):
            line = line.strip()
            for x, char in enumerate(line):
                if stop > 0:
                    stop -= 1
                    continue
                if char.isnumeric():
                    for inc, pos_num in enumerate(line[x + 1 :]):
                        if not pos_num.isnumeric():
                            numbers.append(
                                Position(x, x + inc, y, y, int(line[x : x + inc + 1]))
                            )
                            stop = inc
                            break
                        if inc + x + 2 == len(line):
                            numbers.append(
                                Position(
                                    x, x + inc + 2, y, y, int(line[x : x + inc + 2])
                                )
                            )
                            stop = inc
                            break
                elif char != ".":
                    symbols.append(Position(x, x, y, y, char))
    return numbers, symbols


def get_parts(symbols: List[Position], numbers: List[Position]) -> int:
    parts: List[Position] = []
    for symbol in symbols:
        for number in numbers:
            if number.y1 in range(symbol.y1 - 1, symbol.y1 + 2) and range(
                max(number.x1, symbol.x1 - 1), min(number.x2, symbol.x1 + 1) + 1
            ):
                parts.append(number)
    distinct_parts = set(parts)
    return sum([part.value for part in distinct_parts if isinstance(part.value, int)])


def get_gear_ratios(symbols: List[Position], numbers: List[Position]) -> int:
    gear_ratios: List[int] = []
    for symbol in symbols:
        if not symbol.value == "*":
            continue
        storage = []

        for number in numbers:
            if number.y1 in range(symbol.y1 - 1, symbol.y1 + 2) and range(
                max(number.x1, symbol.x1 - 1), min(number.x2, symbol.x1 + 1) + 1
            ):
                storage.append(number)
        if len(storage) == 2:
            gear_ratios.append(
                reduce(
                    mul, [sto.value for sto in storage if isinstance(sto.value, int)]
                )
            )
    return sum(gear_ratios)


if __name__ == "__main__":
    numbers, symbols = parse_input("test_input.txt")

    # part 1
    sum_parts = get_parts(symbols, numbers)
    print(sum_parts)

    # part 2
    gear_ratio = get_gear_ratios(symbols, numbers)
    print(gear_ratio)
