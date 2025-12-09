# Advent of Code 2025, Day 9
# (c) blu3r4y

from aocd.models import Puzzle
from funcy import print_calls, print_durations


@print_calls
@print_durations(unit="ms")
def part1(points):
    largest_area = 0

    for a in points:
        for b in points:
            area = rectangle_area(a, b)
            if area > largest_area:
                largest_area = area

    return largest_area


@print_calls
@print_durations(unit="ms")
def part2(points):
    h_edges, v_edges = polygon_edges(points)
    largest_area = 0

    for a in points:
        for b in points:
            area = rectangle_area(a, b)
            if area <= largest_area:
                continue

            # check if the rectangle is contained within the polygon
            if is_valid_rectangle(a, b, h_edges, v_edges):
                largest_area = area

    return largest_area


def rectangle_area(a, b):
    (ax, ay), (bx, by) = a, b
    width = abs(bx - ax) + 1
    height = abs(by - ay) + 1
    return width * height


def polygon_edges(points):
    h_edges, v_edges = [], []

    for i in range(len(points)):
        a = points[i]
        b = points[(i + 1) % len(points)]  # wrap around

        (ax, ay), (bx, by) = a, b

        # make vertical line
        if ax == bx:
            ystart = min(ay, by)
            ystop = max(ay, by)
            v_edges.append((ax, ystart, ystop))

        # make horizontal line
        else:
            xstart = min(ax, bx)
            xstop = max(ax, bx)
            h_edges.append((ay, xstart, xstop))

    return h_edges, v_edges


def is_valid_rectangle(a, b, h_segs, v_segs):
    (ax, ay), (bx, by) = a, b
    x1, x2 = min(ax, bx), max(ax, bx)
    y1, y2 = min(ay, by), max(ay, by)

    # check vertical edges
    for vx, vy1, vy2 in v_segs:
        if x1 < vx < x2:
            if vy1 < y2 and vy2 > y1:  # check y overlap
                return False

    # check horizontal edges
    for hy, hx1, hx2 in h_segs:
        if y1 < hy < y2:
            if hx1 < x2 and hx2 > x1:  # check x overlap
                return False

    return True


def load(data):
    points = []
    for line in data.splitlines():
        x, y = line.split(",")
        points.append((int(x), int(y)))
    return points


if __name__ == "__main__":
    puzzle = Puzzle(year=2025, day=9)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 4750092396
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data))
    assert ans2 == 1468516555
    puzzle.answer_b = ans2
