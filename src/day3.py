# Advent of Code 2025, Day 3
# (c) blu3r4y

from aocd.models import Puzzle
from funcy import print_calls, print_durations


@print_calls
@print_durations(unit="ms")
def part1(banks):
    return solve(banks, num_digits=2)


@print_calls
@print_durations(unit="ms")
def part2(banks):
    return solve(banks, num_digits=12)


def solve(banks, num_digits):
    total = 0
    for digits in banks:
        total += find_largest_combination(digits, num_digits)
    return total


def find_largest_combination(digits, num_digits):
    # 'running' maximum of length k found so far
    dp = [0] * num_digits

    for curr in digits:
        # update lengths from the last index down to 1
        for k in range(num_digits - 1, 0, -1):
            val = dp[k - 1] * 10 + curr
            if val > dp[k]:
                dp[k] = val

        # update length 1 (just the digit itself)
        if curr > dp[0]:
            dp[0] = curr

    return dp[-1]


def load(data):
    banks = []
    for line in data.splitlines():
        banks.append([int(x) for x in line.strip()])
    return banks


if __name__ == "__main__":
    puzzle = Puzzle(year=2025, day=3)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 17343
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data))
    assert ans2 == 172664333119298
    puzzle.answer_b = ans2
