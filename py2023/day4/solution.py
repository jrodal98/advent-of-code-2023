#!/usr/bin/env python3
# www.jrodal.com

import re
from aoc_utils.base_solver import BaseSolver, Solution


class Solver(BaseSolver):
    PART1_EXAMPLE_SOLUTION: Solution | None = 13
    PART2_EXAMPLE_SOLUTION: Solution | None = 30

    def part1(self) -> Solution:
        res = 0
        for card in self.data.splitlines():
            _, numbers = card.split(": ")
            winners, mine = numbers.split(" | ")
            winners = set(re.findall(r"\d+", winners))
            mine = set(re.findall(r"\d+", mine))
            num_matches = len(winners & mine)
            if num_matches > 0:
                res += int(2 ** (num_matches - 1))
        return res

    def part2(self) -> Solution:
        cards_original = self.data.splitlines()
        num_cards = [1 for _ in range(len(cards_original))]
        for i, card in enumerate(cards_original):
            card_num_stuff, numbers = card.split(": ")
            card_num = int(re.findall(r"\d+", card_num_stuff)[0])
            winners, mine = numbers.split(" | ")
            winners = set(re.findall(r"\d+", winners))
            mine = set(re.findall(r"\d+", mine))
            num_matches = len(winners & mine)
            for j in range(num_matches):
                num_cards[card_num + j] += num_cards[i]
        return sum(num_cards)
