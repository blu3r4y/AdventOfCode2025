# Advent of Code 2025, Day 1
# (c) blu3r4y

from aocd.models import Puzzle
from funcy import print_calls, print_durations


@print_calls
@print_durations(unit="ms")
def part1(sequence):
    dial = 50
    hits_zero = 0

    for turn, steps in sequence:
        if turn == "L":
            dial -= steps
        elif turn == "R":
            dial += steps

        dial %= 100
        if dial == 0:
            hits_zero += 1

    return hits_zero


@print_calls
@print_durations(unit="ms")
def part2(sequence):
    dial = 50
    cross_zero = 0

    for turn, steps in sequence:
        if turn == "L":
            if dial == 0:  # adjust special case
                cross_zero -= 1
            dial -= steps
            cross_zero += -((dial - 1) // 100)
        elif turn == "R":
            dial += steps
            cross_zero += dial // 100

        dial %= 100

    return cross_zero


def load(data):
    sequence = []
    for line in data.splitlines():
        turn, step = line[0], int(line[1:])
        sequence.append((turn, step))
    return sequence


if __name__ == "__main__":
    puzzle = Puzzle(year=2025, day=1)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 1059
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data))
    assert ans2 == 6305
    puzzle.answer_b = ans2
