import copy

import numpy as np



class Ber:
    def __init__(self, r, p):
        self.p = p
        self.r = r

    def q(self):
        return 1 - self.p

    def e(self):
        return self.p * self.r

    def hash(self):
        return self.p, self.r

    def __str__(self):
        return str(self.hash())


class Action:
    def __init__(self, loc=-1, dropoff=True):
        self.loc = loc
        self.dropoff = dropoff

    def __str__(self):
        return "( " + str(self.loc) + ", " + str(self.dropoff) + " )"

    def __repr__(self):
        return str(self)

    def hash(self):
        return self.loc, self.dropoff


class State:
    # Info held by every node. The info is gathered using agents actions only therefore is deterministic.
    def __init__(self):
        self.time_left = 0  # int

    def is_terminal(self):
        return self.time_left == 0

    def get_loc(self, a_hash):
        pass


class EmpState(State):
    def __init__(self, instance=None):
        super().__init__()
        self.path = {}  # a.hash(): [pos, pos, -1, ... , -1] -
        # Required to count the reward of the state. Not needed in stochastic state.
        if instance is not None:
            self.time_left = instance.horizon
            for a in instance.agents:
                self.path[a.hash()] = [None for _ in range(instance.horizon)]

    def get_loc(self, a_hash):
        if self.path[a_hash][0] is None:
            return None
        if self.path[a_hash][-1] is not None:
            return self.path[a_hash][-1].loc
        first_none = 0
        while self.path[a_hash][first_none] is not None:
            first_none += 1
        return self.path[a_hash][first_none - 1].loc

    def copy(self):
        copy_state = EmpState()
        copy_state.path = copy.deepcopy(self.path)
        copy_state.time_left = self.time_left
        return copy_state

    def __str__(self):
        return str((self.path, self.time_left))


class VectorState(State):
    def __init__(self, instance=None):
        super().__init__()
        self.reward = None
        if instance is not None:
            self.loc = {a.hash(): a.loc.hash() for a in instance.agents}
            self.bers = {v.hash(): Ber(v.bernoulli(), v.p()) for v in instance.map}
            self.utl = {a.hash(): [0 for _ in range(a.utility_budget + 1)] for a in instance.agents}
            for ah in self.utl:
                self.utl[ah][-1] = 1

    def copy(self):
        copy_state = VectorState()
        copy_state.loc = copy.deepcopy(self.loc)
        copy_state.utl = copy.deepcopy(self.utl)
        copy_state.bers = copy.deepcopy(self.bers)
        copy_state.time_left = self.time_left
        return copy_state

    def hash(self):
        hash = tuple((ah, str(self.loc[ah])) for ah in self.loc), \
               tuple((vh, self.bers[vh].hash()) for vh in self.bers), \
               tuple((ah, tuple(self.utl[ah])) for ah in self.utl)
        return hash

    def calculate_vertex_estimate(self, vertex):
        return self.bers[vertex.hash()].e()

    def bernoulli(self, vertex):
        return self.bers[vertex.hash()].r

    def get_loc(self, a_hash):
        return self.loc[a_hash]

    def prob_u_at_least(self, a_hash, x):
        return 1 - sum(self.utl[a_hash][u] for u in range(x))

    def __str__(self):
        return str(self.loc)


def dict_to_np_arr(dict):
    if round(sum(dict.values()), 5) != 1:
        raise Exception("Sum of probabilities in distribution must be 1")
    arr = np.zeros((max([k for k in dict if dict[k] != 0]) + 1))
    for k in dict:
        if round(k) != k:
            raise Exception("Number of targets must be an integer!")
        if dict[k] != 0:
            arr[k] = dict[k]
    return arr
