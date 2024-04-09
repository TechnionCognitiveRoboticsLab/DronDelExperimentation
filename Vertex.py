import random


class Vertex:
    def __init__(self, x, y):
        self.xy = (x, y)  # String name
        self.neighbours = []  # list of Vertices
        self.distribution = {}  # reward: probability dictionary

    def hash(self):
        if self.xy == -1:
            raise Exception("-1 is an unusable hash number.")
        return self.xy

    def __str__(self):
        return "v" + str(self.xy)

    def expectation(self):
        return sum([r * self.distribution[r] for r in self.distribution])

    def p(self):
        return 1 - self.distribution[0]

    def q(self):
        return self.distribution[0]

    def bernoulli(self):
        return 0 if self.p() == 0 else sum([r * self.distribution[r] for r in self.distribution]) / self.p()


class EmpVertex(Vertex):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.is_empty = False
        self.reward = 0

    def generate_reward(self):
        p = random.random()
        sum_p = 0
        for r in self.distribution:
            sum_p += self.distribution[r]
            if sum_p > p:
                self.reward = r
                break
        self.is_empty = (self.reward == 0)

    def generate_semi_emp_reward(self):
        if random.random() > self.q():
            self.reward = self.bernoulli()
        self.is_empty = (self.reward == 0)

    def __str__(self):
        return "det_v" + str(self.xy) + " " + str(self.reward) + " " + str(self.is_empty)


class Stoch_Vertex(Vertex):
    def __init__(self, x, y):
        super().__init__(x, y)
