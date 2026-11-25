"""HW3 · report.py: add up the steps and save a report as JSON. Practises Session 7 (writing
and reading JSON) and Session 9 (a context manager)."""

import json
from collections.abc import Iterable, Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import TextIO

from walks import Walk, good_walks, read_rows


def steps_per_day(walks: Iterable[Walk]) -> dict[str, int]:
    totals={}
    for walk in walks:
        totals[walk.date]=totals.get(walk.date, 0) + walk.steps
    ordered={}
    for date in sorted(totals):
        ordered[date] = totals[date]
    return ordered
    raise NotImplementedError("core: add up the steps for each date, earliest date first")


def best_day(totals: dict[str, int]) -> str:
    if len(totals)==0:
        raise ValueError("there are no days")
    best=None
    for date in sorted(totals):
        if best is None or totals[date]>totals[best]:
            best=date
    return best
    raise NotImplementedError("core: the date with the most steps, the earliest on a tie")


@contextmanager
def saved_safely(path: Path) -> Iterator[TextIO]:
    temp=path.with_name(path.name + ".tmp")
    try:
        with open(temp, "w", encoding="utf-8") as file:
            yield file
    except Exception:
        temp.unlink(missing_ok=True)
        raise
    temp.replace(path)
    raise NotImplementedError("core: write to a .tmp file, then replace path only if nothing failed")


def write_report(path: Path, walks: Iterable[Walk]) -> dict:
    days=steps_per_day(walks)
    report={
        "total_steps": sum(days.values()),
        "best_day": best_day(days),
        "days": days,
    }
    with saved_safely(path) as file:
        json.dump(report, file, indent=2)
    return report
    raise NotImplementedError("core: build the report dict, save it with saved_safely, return it")


def load_report(path: Path) -> dict | None:
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return None
    raise NotImplementedError("core: load the saved report, or None if it is missing or broken")


if __name__ == "__main__":
    # Provided: runs only with `python report.py`, not on import.
    here = Path(__file__).parent
    last_time = load_report(here / "report.json")
    report = write_report(here / "report.json", good_walks(read_rows(here / "walks.csv")))
    print(f"{report['total_steps']} steps this week. Best day: {report['best_day']}.")
    if last_time is not None:
        print(f"Last time you saved {last_time['total_steps']} steps.")
