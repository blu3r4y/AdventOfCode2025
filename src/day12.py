# Advent of Code 2025, Day 12
# (c) blu3r4y

from aocd.models import Puzzle
from funcy import print_calls, print_durations
from parse import parse
from tqdm import tqdm

# shapes are always 3x3
GRID_SIZE = 3


@print_calls
@print_durations(unit="ms")
def part1(data):
    shapes, regions = data

    # pre-compute all symmetries of each shape
    symmetries = [shape_symmetries(s) for s in shapes]
    areas = [shape_area(s) for s in shapes]

    num_fits = 0
    for region in tqdm(regions, desc="Testing regions"):
        if can_fit(region, symmetries, areas):
            num_fits += 1

    return num_fits


def can_fit(region, symmetries, areas):
    (width, height), quantities = region

    # currently occupied grid positions
    grid = set()

    # list of shape indices to place
    fringe = []
    for i, quantity in enumerate(quantities):
        fringe.extend([i] * quantity)

    # test if the grid is large enough to hold all shapes
    total_area = sum(q * areas[i] for i, q in enumerate(quantities))
    if total_area > width * height:
        return False

    def backtrack():
        if not fringe:
            return True  # all shapes placed

        i = fringe.pop()

        # try all symmetries and positions
        for symmetry in symmetries[i]:
            for y in range(height - GRID_SIZE + 1):
                for x in range(width - GRID_SIZE + 1):
                    shape = {complex(x, y) + s for s in symmetry}

                    # continue if already occupied
                    if shape & grid:
                        continue

                    # place shape and recurse
                    grid.update(shape)
                    if backtrack():
                        return True

                    # remove shape (backtrack)
                    grid.difference_update(shape)

        # put shape back on failure
        fringe.append(i)
        return False

    return backtrack()


def shape_symmetries(shape):
    """Generate all rotations and flips of a shape."""
    shapes = set()

    flipx = flip_shape(shape, "x")
    flipy = flip_shape(shape, "y")
    for n in range(4):
        shapes.add(frozenset(rotate_shape(shape, n)))
        shapes.add(frozenset(rotate_shape(flipx, n)))
        shapes.add(frozenset(rotate_shape(flipy, n)))

    return shapes


def shape_area(shape):
    """Return number of occupied cells in shape."""
    return len(shape)


def rotate_shape(shape, n=1):
    """Rotate 3x3 shape 90 degrees clockwise n times."""
    for _ in range(n):
        shape = {complex(GRID_SIZE - 1 - p.imag, p.real) for p in shape}
    return shape


def flip_shape(shape, axis="x"):
    """Flip 3x3 shape along the specified axis ('x' or 'y')."""
    if axis == "x":
        return {complex(GRID_SIZE - 1 - x.real, x.imag) for x in shape}
    if axis == "y":
        return {complex(x.real, GRID_SIZE - 1 - x.imag) for x in shape}


def load(data):
    segments = data.strip().split("\n\n")

    shapes = []
    for segment in segments[:-1]:
        lines = segment.splitlines()[1:]
        shape = set()
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char == "#":
                    shape.add(complex(x, y))
        shapes.append(shape)

    assert len(shapes) == 6

    regions = []
    for region in segments[-1].splitlines():
        width, height, quantities = parse("{:d}x{:d}: {}", region)
        quantities = tuple(int(v) for v in quantities.split())
        assert len(quantities) == 6
        regions.append(((width, height), quantities))

    return shapes, regions


if __name__ == "__main__":
    puzzle = Puzzle(year=2025, day=12)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 497
    puzzle.answer_a = ans1
