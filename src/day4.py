# Advent of Code 2025, Day 4
# (c) blu3r4y

from aocd.models import Puzzle
from funcy import print_calls, print_durations

ADJACENT = (
    complex(-1, -1),
    complex(0, -1),
    complex(1, -1),
    complex(-1, 0),
    complex(1, 0),
    complex(-1, 1),
    complex(0, 1),
    complex(1, 1),
)


@print_calls
@print_durations(unit="ms")
def part1(data):
    return len(accessible_positions(*data))


@print_calls
@print_durations(unit="ms")
def part2(data):
    paper, limits = data
    num_removed = 0

    while True:
        accessible = accessible_positions(paper, limits)
        if not accessible:
            break

        # remove accessible positions and repeat
        paper -= accessible
        num_removed += len(accessible)

    return num_removed


def accessible_positions(paper, limits):
    height, width = limits
    accessible = set()

    for y in range(height):
        for x in range(width):
            pos = complex(x, y)
            if pos not in paper:
                continue

            # forklifts can access positions with less than 4 neighbors
            count = sum(1 for n in neighbors(pos) if n in paper)
            if count < 4:
                accessible.add(pos)

    return accessible


def neighbors(pos):
    for d in ADJACENT:
        yield pos + d


def load(data):
    paper = set()

    rows = data.splitlines()
    for r, row in enumerate(data.splitlines()):
        for c, cell in enumerate(row):
            pos = complex(c, r)
            if cell == "@":
                paper.add(pos)

    limits = len(rows), len(rows[0])
    return paper, limits


if __name__ == "__main__":
    puzzle = Puzzle(year=2025, day=4)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 1527
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data))
    assert ans2 == 8690
    puzzle.answer_b = ans2
