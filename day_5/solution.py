import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict


@dataclass()
class MapRange:
    name_source: str
    name_destination: str
    source_start: int
    destination_start: int
    range_length: int
    source_range: range


MAP_NAMES = {
    "seed-to-soil": "soil-to-fertilizer",
    "soil-to-fertilizer": "fertilizer-to-water",
    "fertilizer-to-water": "water-to-light",
    "water-to-light": "light-to-temperature",
    "light-to-temperature": "temperature-to-humidity",
    "temperature-to-humidity": "humidity-to-location",
    "humidity-to-location": "",
}


def parse_input(file_name: str) -> Any:
    maps: Dict[Any, Any] = {}
    with open(Path(os.getcwd()) / "day_5" / file_name) as f:
        for line in f.readlines():
            if line[0:5] == "seeds":
                seeds = map(int, line.split(":")[1].strip().split(" "))
            elif "map:" in line:
                map_name = line.split("map")[0].strip()
                name_source = map_name.split("-to-")[0]
                name_destination = map_name.split("-to-")[1]

            elif line == "\n":
                continue
            else:
                values = line.strip().split()
                maps[map_name] = maps.get(map_name, []) + [
                    MapRange(
                        name_source,
                        name_destination,
                        source_start=int(values[1]),
                        destination_start=int(values[0]),
                        range_length=int(values[2]),
                        source_range=range(
                            int(values[1]),
                            int(values[1]) + int(values[2]),
                        ),
                    )
                ]
    return maps, seeds


# def make_maps(maps):
#     for key, map in maps.items():


if __name__ == "__main__":
    maps, seeds = parse_input("input.txt")
    seeds = list(seeds)
    new_seeds = []

    for ii in range(0, len(seeds), 2):
        new_seeds += [range(seeds[ii], seeds[ii] + seeds[ii + 1])]
    out = []
    for seed_range in new_seeds:
        for seed in seed_range:
            mn = "seed-to-soil"
            while mn:
                current_map = maps[mn]
                for map_range in current_map:
                    if seed in map_range.source_range:
                        value = seed - map_range.source_start
                        seed = map_range.destination_start + value
                        break
                mn = MAP_NAMES[mn]

            out.append(seed)
    print(min(out))
