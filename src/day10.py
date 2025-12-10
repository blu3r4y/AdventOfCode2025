# Advent of Code 2025, Day 10
# (c) blu3r4y

from collections import deque

import numpy as np
from aocd.models import Puzzle
from funcy import print_calls, print_durations
from scipy.optimize import LinearConstraint, milp


@print_calls
@print_durations(unit="ms")
def part1(machines):
    return sum(bfs_minimum_light_steps(m) for m in machines)


@print_calls
@print_durations(unit="ms")
def part2(machines):
    return sum(lp_minimum_joltage_steps(m) for m in machines)


def bfs_minimum_light_steps(machine):
    lights, buttons, _ = machine

    goal = tuple(lights)
    start = (False,) * len(lights)
    queue = deque([(start, 0)])
    visited = {start}

    while queue:
        current_state, steps = queue.popleft()
        if current_state == goal:
            return steps

        for button in buttons:
            next_state = toggle_lights(current_state, button)
            if next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, steps + 1))


def toggle_lights(lights, button):
    lights = list(lights)
    for i in button:
        lights[i] = not lights[i]
    return tuple(lights)


def lp_minimum_joltage_steps(machine):
    _, buttons, joltage = machine
    num_variables = len(buttons)
    num_equations = len(joltage)

    # objective: coefficients to be minimized (sum of button presses)
    # c[i] = n, if button i is pressed n times
    c = np.ones(num_variables)

    # constraint: A @ x = joltage (where x is the vector of button presses)
    # A[i,j] = 1, if button j affects indicator light i
    A = np.zeros((num_equations, num_variables))
    for j, btn in enumerate(buttons):
        for i in btn:
            A[i, j] = 1

    # bounds: the target joltage (right-hand side of the equation)
    b = np.array(joltage)

    # solve linear programming problem with exact constraints
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.milp.html
    res = milp(
        c=c,
        constraints=LinearConstraint(A, b, b),  # lower bound = upper bound
        integrality=np.ones(num_variables),  # solve for integers
    )

    assert res.success
    return int(round(res.fun))


def load(data):
    machines = []
    for line in data.splitlines():
        parts = line.split(" ")
        lights, buttons, joltage = parts[0], parts[1:-1], parts[-1]

        # indicator lights
        lights = lights.strip("[]").replace("#", "1").replace(".", "0")
        lights = [bool(int(x)) for x in lights]
        # buttons
        buttons = [tuple(int(x) for x in b.strip("()").split(",")) for b in buttons]
        # joltage
        joltage = tuple(int(x) for x in joltage.strip("{}").split(","))

        machines.append((lights, buttons, joltage))

    return machines


if __name__ == "__main__":
    puzzle = Puzzle(year=2025, day=10)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 520
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data))
    assert ans2 == 20626
    puzzle.answer_b = ans2
