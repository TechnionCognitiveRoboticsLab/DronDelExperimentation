import numpy as np


class Agent:
    def __init__(self, number, loc, movement_budget, utility_budget):
        self.number = number
        self.loc = loc  # vertex location
        self.movement_budget = movement_budget  # int
        self.utility_budget = utility_budget  # int

    def hash(self):
        if self.number == -1:
            raise Exception("-1 is an unusable hash number.")
        return self.number

    def __str__(self):
        return "a" + self.number


class StochAgent(Agent):
    def __init__(self, number, loc, movement_budget, utility_budget):
        super().__init__(number, loc, movement_budget, utility_budget)


class DetAgent(Agent):
    def __init__(self, number, loc, movement_budget, utility_budget):
        super().__init__(number, loc, movement_budget, utility_budget)
        self.current_utility_budget = utility_budget

    def __str__(self):
        return "det_a" + str(self.number)
