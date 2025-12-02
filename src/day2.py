# Advent of Code 2025, Day 2
# (c) blu3r4y

from aocd.models import Puzzle
from funcy import print_calls, print_durations


@print_calls
@print_durations(unit="ms")
def part1(ranges):
    invalid_ids = set()

    for start, end in ranges:
        for i in range(start, end + 1):
            if is_invalid_id(i, n_repeat=2):
                invalid_ids.add(i)

    return sum(invalid_ids)


@print_calls
@print_durations(unit="ms")
def part2(ranges):
    invalid_ids = set()

    for start, end in ranges:
        for i in range(start, end + 1):
            num_digits = len(str(i))
            for j in range(2, num_digits + 1):
                if is_invalid_id(i, n_repeat=j):
                    invalid_ids.add(i)

    return sum(invalid_ids)


def is_invalid_id(i, n_repeat=2):
    # split into digits and check if divisible
    digits = [int(d) for d in str(i)]
    if len(digits) % n_repeat != 0:
        return False

    # test all offsets (e.g., for 1212 check index 0,2 and 1,3)
    offset = len(digits) // n_repeat
    for j in range(offset):
        for k in range(1, n_repeat):
            if digits[j] != digits[j + k * offset]:
                return False

    return True


def load(data):
    ranges = []
    for chunk in data.strip().split(","):
        start, end = chunk.split("-")
        ranges.append((int(start), int(end)))
    return ranges


if __name__ == "__main__":
    puzzle = Puzzle(year=2025, day=2)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 37314786486
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data))
    assert ans2 == 47477053982
    puzzle.answer_b = ans2
