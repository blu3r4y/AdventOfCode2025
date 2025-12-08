# Advent of Code 2025, Day 8
# (c) blu3r4y

import networkx as nx
import numpy as np
from aocd.models import Puzzle
from funcy import print_calls, print_durations


@print_calls
@print_durations(unit="ms")
def part1(points, max_connections=1000):
    G, _ = solve(points, max_connections=max_connections)

    # sizes of isolated subgraphs
    components = list(nx.connected_components(G))
    sizes = sorted([len(c) for c in components], reverse=True)

    # product of sizes of the three largest components
    return int(sizes[0] * sizes[1] * sizes[2])


@print_calls
@print_durations(unit="ms")
def part2(points):
    _, lastedge = solve(points)

    # multiply x-coordinates of last edge
    return int(lastedge[0][0] * lastedge[1][0])


@print_durations(unit="ms")
def solve(points, max_connections=None):
    num_points = len(points)

    pairs = []
    for i in range(num_points):
        for j in range(i + 1, num_points):
            dist = np.linalg.norm(points[i] - points[j])
            pairs.append((dist, i, j))

    # sort by distance
    pairs.sort(key=lambda x: x[0])

    # build graph
    G = nx.Graph()
    G.add_nodes_from(range(num_points))

    lastedge = None

    # keep connecting closest pairs
    for _, u, v in pairs[:max_connections]:
        if not nx.has_path(G, u, v):
            G.add_edge(u, v)

        # stop if all points are connected
        if nx.number_connected_components(G) == 1:
            lastedge = (points[u], points[v])
            break

    return G, lastedge


def load(data):
    points = []
    for line in data.splitlines():
        nums = list(map(int, line.split(",")))
        points.append(nums)
    return np.array(points)


if __name__ == "__main__":
    puzzle = Puzzle(year=2025, day=8)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 330786
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data))
    assert ans2 == 3276581616
    puzzle.answer_b = ans2
