"""HW3 · walks.py: read the step counter's CSV file and keep only the good rows. Practises
Session 7 (reading a CSV file, cleaning data) and Session 9 (a generator and a decorator)."""

import csv
from collections.abc import Callable, Iterable, Iterator
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Walk:
    """Provided: one walk from the log, cleaned. `steps` is a whole number, 0 or more."""

    date: str
    steps: int
    place: str


def parse_walk(row: dict[str, str]) -> Walk:
    date=(row["date"] or "").strip()
    if date=="":
        raise ValueError("date is empty")
    steps=int(row["steps"] or "")
    if steps<0:
        raise ValueError(f"steps is below 0: {steps}")
    place=(row["place"] or "").strip()
    return Walk(date, steps, place)
    raise NotImplementedError("core: clean one row into a Walk, or raise ValueError for a bad row")


def none_on_error(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return None
    return wrapper
    raise NotImplementedError("core: wrap func so that a ValueError becomes None")


def read_rows(path: Path) -> Iterator[dict[str, str]]:
    with open(path, encoding="utf-8", newline="") as file:
        for row in csv.DictReader(file):
            yield row
    raise NotImplementedError("core: open the CSV file and yield its rows one at a time")


def good_walks(rows: Iterable[dict[str, str]]) -> Iterator[Walk]:
    parse=none_on_error(parse_walk)
    for row in rows:
        walk=parse(row)
        if walk is not None:
            yield walk
    raise NotImplementedError("core: yield a Walk for each good row and skip the bad ones")
