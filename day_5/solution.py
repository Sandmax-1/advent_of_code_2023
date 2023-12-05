import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple


@dataclass()
class MapRange:
    destination_start: int
    diff: int
    source_range: range

    def __repr__(self) -> str:
        return f"source_range={self.source_range}, diff={self.diff}, dest_start={self.destination_start}"  # noqa: E501


MAP_NAMES = {
    "seed-to-soil": "soil-to-fertilizer",
    "soil-to-fertilizer": "fertilizer-to-water",
    "fertilizer-to-water": "water-to-light",
    "water-to-light": "light-to-temperature",
    "light-to-temperature": "temperature-to-humidity",
    "temperature-to-humidity": "humidity-to-location",
    "humidity-to-location": "",
}


def parse_input(file_name: str) -> Tuple[Dict[str, List[MapRange]], List[int]]:
    maps: Dict[str, List[MapRange]] = {}
    with open(Path(os.getcwd()) / "day_5" / file_name) as f:
        for line in f.readlines():
            if line[0:5] == "seeds":
                seeds = map(int, line.split(":")[1].strip().split(" "))
            elif "map:" in line:
                map_name = line.split("map")[0].strip()
            elif line == "\n":
                continue
            else:
                values = line.strip().split()
                maps[map_name] = maps.get(map_name, []) + [
                    MapRange(
                        destination_start=int(values[0]),
                        diff=int(values[1]) - int(values[0]),
                        source_range=range(
                            int(values[1]),
                            int(values[1]) + int(values[2]),
                        ),
                    )
                ]
    return maps, list(seeds)


def get_range_intersection(r1: range, r2: range) -> range:
    r = range(max(r1.start, r2.start), min(r1.stop, r2.stop))
    return r


def get_non_intersecting_ranges(r1: range, r2: range) -> List[range]:
    if r1.start < r2.start <= r2.stop < r1.stop:  # contained
        poss_ranges = [range(r1.start, r2.start), range(r2.stop, r1.stop)]
    elif r1.start <= r2.start <= r1.stop < r2.stop:  # overalps left side
        poss_ranges = [range(r1.start, r2.start)]
    elif r2.start <= r1.start <= r2.stop < r1.stop:  # overlaps right side
        poss_ranges = [range(r2.stop, r1.stop)]
    elif (
        r1.start < r1.stop < r2.start < r2.stop
        or r1.stop >= r1.start > r2.stop >= r2.start  # noqa: W503
    ):  # disjoint
        poss_ranges = [r1]
    else:  # completely contained
        poss_ranges = []
    return poss_ranges


def get_locations_from_seed_ranges(
    maps: Dict[str, List[MapRange]], seed_ranges: List[range]
) -> List[range]:
    map_name = "seed-to-soil"
    intersections: List[range] = []
    disjoint_ranges = seed_ranges
    while map_name:
        current_map = maps[map_name]
        if intersections:
            disjoint_ranges = intersections + disjoint_ranges
        intersections = []
        for map_range in current_map:
            intersections += [
                range(a.start - map_range.diff, a.stop - map_range.diff)
                for inter in disjoint_ranges
                if (a := get_range_intersection(inter, map_range.source_range))
            ]
            disjoint_range_lists = [
                get_non_intersecting_ranges(inter, map_range.source_range)
                for inter in disjoint_ranges
            ]
            disjoint_ranges = [
                item for sublist in disjoint_range_lists for item in sublist
            ]

        map_name = MAP_NAMES[map_name]
    return intersections + disjoint_ranges


if __name__ == "__main__":
    maps, seeds = parse_input("input.txt")

    # part 1
    seed_ranges = [range(seed, seed + 1) for seed in seeds]
    part_1 = ranges = get_locations_from_seed_ranges(maps, seed_ranges)
    print(min(val.start for val in ranges))

    # part 2
    seed_ranges = []
    for ii in range(0, len(seeds), 2):
        seed_ranges += [range(seeds[ii], seeds[ii] + seeds[ii + 1])]

    part_2 = get_locations_from_seed_ranges(maps, seed_ranges)
    print(min(val.start for val in part_2))
