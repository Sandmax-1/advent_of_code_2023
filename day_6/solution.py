import os
import re
from pathlib import Path
from typing import List, Tuple


def parse_input(file_name: str) -> List[Tuple[str, str]]:
    with open(Path(os.getcwd()) / "day_6" / file_name) as f:
        for line in f.readlines():
            if "Time" in line:
                times = re.findall(r"\d+", line)
            if "Distance" in line:
                distances = re.findall(r"\d+", line)
    return list(zip(times, distances))


def evaluate_races(races: List[Tuple[str, str]]) -> int:
    out = 1
    for time, distance_to_beat in races:
        time_int = int(time)
        distance_to_beat_int = int(distance_to_beat)
        winning_dists = []
        for subtime in range(0, time_int):
            speed = subtime
            time_left = time_int - subtime
            distance = speed * time_left
            if distance > distance_to_beat_int:
                winning_dists.append(distance)
        out *= len(winning_dists)
    return out


if __name__ == "__main__":
    races = parse_input("input.txt")

    # part 1
    part_1 = evaluate_races(races)
    print(part_1)

    # part 2
    races = [
        (
            "".join([time for time, _ in races]),
            "".join([distance for _, distance in races]),
        )
    ]
    part_2 = evaluate_races(races)
    print(part_2)
