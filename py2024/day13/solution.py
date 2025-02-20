#!/usr/bin/env python3
# www.jrodal.com

from aoc_utils.helpers import ints
from aoc_utils.base_solver import BaseSolver, Solution
from z3 import Int, Optimize, sat


class Solver(BaseSolver):
    def _solve(self, part1: bool) -> Solution:
        # We weren't given a part2 test case, so just run part1 again
        conversion_factor = 0 if part1 else 10000000000000
        ans = 0
        for section in self.sections():
            ax, ay, bx, by, x, y = ints(section)
            ans += self._z3solver(
                ax, ay, bx, by, x + conversion_factor, y + conversion_factor
            )
        return ans

    @classmethod
    def _z3solver(cls, ax: int, ay: int, bx: int, by: int, x: int, y: int) -> int:
        a_val = Int("a_val")
        b_val = Int("b_val")

        opt = Optimize()

        opt.add(ax * a_val + bx * b_val == x)
        opt.add(ay * a_val + by * b_val == y)
        opt.add(a_val >= 0, b_val >= 0)

        total_cost = 3 * a_val + b_val
        opt.minimize(total_cost)

        if opt.check() == sat:
            model = opt.model()
            return model.evaluate(total_cost).as_long()  # pyright: ignore
        else:
            return 0
