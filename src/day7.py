# Advent of Code 2025, Day 7
# (c) blu3r4y

from collections import defaultdict

from aocd.models import Puzzle
from funcy import print_calls, print_durations

DOWN = 1j


@print_calls
@print_durations(unit="ms")
def part1(data):
    start, splitters, limits = data

    beams = set()
    beams.add(start + DOWN)  # initial beam

    num_splits = 0

    for r in range(2, limits[0] + 1):
        splits = {s for s in splitters if s.imag == r}

        previous_beams = beams.copy()
        beams = set()

        for pos in previous_beams:
            target = pos + DOWN
            if target in splits:
                beams.add(target + 1)
                beams.add(target - 1)
                num_splits += 1
            else:
                beams.add(target)

    return num_splits


@print_calls
@print_durations(unit="ms")
def part2(data):
    start, splitters, limits = data

    traces = defaultdict(int)
    traces[start + DOWN] = 1  # initial beam

    for r in range(2, limits[0] + 1):
        splits = {s for s in splitters if s.imag == r}

        new_traces = defaultdict(int)
        for pos, count in traces.items():
            target = pos + DOWN
            if target in splits:
                new_traces[target + 1] += count
                new_traces[target - 1] += count
            else:
                new_traces[target] += count
        traces = new_traces

    return sum(traces.values())


def load(data):
    start = None
    splitters = set()

    rows = data.splitlines()
    for r, row in enumerate(data.splitlines()):
        for c, cell in enumerate(row):
            pos = complex(c, r)
            if cell == "^":
                splitters.add(pos)
            elif cell == "S":
                start = pos

    limits = len(rows), len(rows[0])
    return start, splitters, limits


if __name__ == "__main__":
    puzzle = Puzzle(year=2025, day=7)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 1633
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data))
    assert ans2 == 34339203133559
    puzzle.answer_b = ans2
