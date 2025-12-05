# Advent of Code 2025, Day 5
# (c) blu3r4y

from aocd.models import Puzzle
from funcy import print_calls, print_durations
from parse import parse


class Interval:
    """
    Represents a range of values [start, end).
    Supports cutting out sub-ranges, resulting in a tree of sub-intervals.
    Returns a minimal set of non-overlapping intervals when iterated over.

    Copyright (c) 2025 Mario Kahlhofer, AGPL-3.0 License
    Original Source: https://github.com/blu3r4y/jku-room-search/blob/main/src/scraper/splitTree.ts
    """

    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.left = None
        self.right = None

    @property
    def is_empty(self):
        return self.start >= self.end

    def cut(self, cut_start, cut_end):
        if self.left or self.right:
            if self.left and cut_start < self.left.end:
                self.left.cut(cut_start, cut_end)
            if self.right and cut_end > self.right.start:
                self.right.cut(cut_start, cut_end)
            return

        if self.is_empty or cut_start >= self.end or cut_end <= self.start:
            return

        if cut_start <= self.start and cut_end >= self.end:
            self.start = self.end
            return

        if cut_start > self.start:
            self.left = Interval(self.start, cut_start)
        if cut_end < self.end:
            self.right = Interval(cut_end, self.end)

    def __iter__(self):
        if self.left or self.right:
            if self.left:
                yield from self.left
            if self.right:
                yield from self.right
        elif not self.is_empty:
            yield (self.start, self.end)


@print_calls
@print_durations(unit="ms")
def part1(data):
    ranges, ingredients = data

    fresh = set()
    for start, end in ranges:
        fresh.update(ing for ing in ingredients if start <= ing <= end)

    return len(fresh)


@print_calls
@print_durations(unit="ms")
def part2(data):
    ranges, _ = data

    # start with a single large interval
    rmin, rmax = min(r[0] for r in ranges), max(r[1] for r in ranges)
    root = Interval(rmin, rmax + 1)

    # cut out all fresh ranges
    for start, end in ranges:
        root.cut(start, end + 1)

    # length of cut intervals
    cut_length = sum(end - start for start, end in root)

    # the number of fresh ingredients is equal to the total length
    # of the original interval minus the length of the cut intervals
    total_length = (rmax + 1) - rmin
    return total_length - cut_length


def load(data):
    blocks = data.split("\n\n")

    ranges = []
    for line in blocks[0].splitlines():
        start, end = parse("{:d}-{:d}", line)
        ranges.append((start, end))

    ingredients = []
    for line in blocks[1].splitlines():
        ingredients.append(int(line))

    return ranges, ingredients


if __name__ == "__main__":
    puzzle = Puzzle(year=2025, day=5)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 664
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data))
    assert ans2 == 350780324308385
    puzzle.answer_b = ans2
