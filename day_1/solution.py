import os
from pathlib import Path

NUMBERS_LIST = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
NUMBERS_TO_REPLACE = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def get_first_last_number(line: str) -> int:
    lval = ""
    rval = ""
    for id, val in enumerate(line):
        rid = -id - 1
        if val in NUMBERS_LIST and not lval:
            lval = val
        if line[rid] in NUMBERS_LIST and not rval:
            rval = line[rid]
        if rval and lval:
            break
    return int(lval + rval)


with open(Path(os.getcwd()) / "day_1" / "input.txt", "r") as f:
    s = 0
    for line in f.readlines():
        line = line.lower().strip()
        rev_line = line[::-1]
        lidx = None
        ridx = None
        lval = None
        rval = None
        for strnum, num in NUMBERS_TO_REPLACE.items():
            lower_idx = line.find(strnum)
            upper_idx = rev_line.find(strnum[::-1])

            if lower_idx >= 0:
                if not lidx and lidx != 0:
                    lidx = lower_idx
                    lval = num
                elif lidx > lower_idx:
                    lidx = lower_idx
                    lval = num

            if upper_idx >= 0:
                if not ridx and ridx != 0:
                    ridx = -upper_idx
                    rval = num
                elif ridx < -upper_idx:
                    if -upper_idx == 0:
                        upper_idx = 1
                    ridx = -upper_idx
                    rval = num
        if lidx is not None:
            line = line[:lidx] + lval + line[lidx:]
        if ridx is not None:
            line = (
                line[: len(line) + ridx]
                + rval
                + line[len(line) + ridx :]  # noqa: E203, E501
            )
        s += get_first_last_number(line)
    print(s)
