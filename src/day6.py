# Advent of Code 2025, Day 6
# (c) blu3r4y

from functools import reduce
from operator import mul

from aocd.models import Puzzle
from funcy import print_calls, print_durations


@print_calls
@print_durations(unit="ms")
def part1(data):
    return solve(data)


@print_calls
@print_durations(unit="ms")
def part2(data):
    return solve(data)


def solve(data):
    columns, operators = data

    result = 0
    for col in columns:
        op = operators.pop(0)
        if op == "+":
            result += sum(col)
        elif op == "*":
            result += reduce(mul, col)

    return result


def load1(data):
    lines = data.splitlines()
    ncols = len(lines[0].split())

    columns = []  # [[123, 45, 6], [328, 64, 98], ...]
    operators = []  # ['*', '+', ...]

    for i in range(ncols):
        col = []
        for line in lines:
            entry = line.split()[i]
            if str.isnumeric(entry):
                col.append(int(entry))
            else:
                operators.append(entry)
        columns.append(col)

    return columns, operators


def load2(data):
    lines = data.splitlines()
    ncols = len(lines[0].split())
    nrows = len(lines)

    # column start positions
    starts = []
    for i, char in enumerate(lines[-1]):
        if char != " ":
            starts.append(i)

    # column end positions
    last_index = len(lines[-1]) - 1
    ends = [i - 2 for i in starts[1:]] + [last_index]

    # column widths
    widths = [end - start + 1 for start, end in zip(starts, ends)]

    # iterate columns, left-to-right
    columns = [[] for _ in range(ncols)]
    for i in range(ncols):
        # iterate digit indexes, right-to-left
        for j in range(widths[i] - 1, -1, -1):
            # iterate rows (building the digit), top-to-bottom
            digitstr = ""
            for r in range(nrows - 1):
                digitstr += lines[r][starts[i] + j]
            digit = int(digitstr.strip())
            columns[i].append(digit)

    # extract operators
    operators = [op.strip() for op in lines[-1].split()]

    return columns, operators


if __name__ == "__main__":
    puzzle = Puzzle(year=2025, day=6)

    ans1 = part1(load1(puzzle.input_data))
    assert ans1 == 5733696195703
    puzzle.answer_a = ans1

    ans2 = part2(load2(puzzle.input_data))
    assert ans2 == 10951882745757
    puzzle.answer_b = ans2
