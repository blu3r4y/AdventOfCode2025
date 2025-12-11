# Advent of Code 2025, Day 11
# (c) blu3r4y

from functools import cache

import networkx as nx
from aocd.models import Puzzle
from funcy import print_calls, print_durations


@print_calls
@print_durations(unit="ms")
def part1(G):
    count_paths.cache_clear()
    return count_paths(G, "you", "out")


@print_calls
@print_durations(unit="ms")
def part2(G):
    count_paths.cache_clear()

    svr_to_fft = count_paths(G, "svr", "fft")
    svr_to_dac = count_paths(G, "svr", "dac")

    fft_to_dac = count_paths(G, "fft", "dac")
    dac_to_fft = count_paths(G, "dac", "fft")

    fft_to_out = count_paths(G, "fft", "out")
    dac_to_out = count_paths(G, "dac", "out")

    svr_fft_dac_out = svr_to_fft * fft_to_dac * dac_to_out
    svr_dac_fft_out = svr_to_dac * dac_to_fft * fft_to_out
    return svr_fft_dac_out + svr_dac_fft_out


@cache
def count_paths(G, u, target):
    if u == target:
        return 1
    return sum(count_paths(G, v, target) for v in G.successors(u))


def load(data):
    G = nx.DiGraph()
    for line in data.splitlines():
        node, edges = line.split(": ")
        for edge in edges.split():
            G.add_edge(node, edge)
    return G


if __name__ == "__main__":
    puzzle = Puzzle(year=2025, day=11)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 506
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data))
    assert ans2 == 385912350172800
    puzzle.answer_b = ans2
