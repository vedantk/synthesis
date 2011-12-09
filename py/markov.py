#!/usr/bin/pypy
# markov.py - Vedant Kumar <vsk@berkeley.edu>

import random
from collections import defaultdict, deque

'''
A node is some atomic, fundamental unit.
A state is an ordered collection of nodes (a history).
A branch contains a list of nodes that can follow a given state (the future).
A Markov chain maps states to their branches.
'''

class Branch:
        def __init__(self):
                self.total = 0.0
                self.counts = defaultdict(int) # Node => Frequency

        def update(self, node):
                self.total += 1
                self.counts[node] += 1

        def sample(self):
                thresh = random.random()
                for node, freq in self.counts.items():
                        probability = freq / self.total
                        if probability >= thresh:
                                return node
                        thresh -= probability
                return random.choice(list(self.counts.keys()))

class MarkovChain:
        def __init__(self, n_limit):
                '''n_limit: Maximum history per node.'''
                self.n_limit = n_limit
                self.transitions = defaultdict(Branch) # State => [Node]

        def add_sequence(self, seq):
                '''seq: Iterable of hash-able information.'''
                for state, node in self._find_transitions(seq):
                        self.transitions[state].update(node)
                self._state_list = list(self.transitions.keys())

        def _find_transitions(self, seq):
                '''Generate all states and their futures.'''
                for i in xrange(len(seq)):
                        for j in xrange(1, self.n_limit + 1):
                                state = seq[i:i+j]
                                if len(state) == j and (i + j) < len(seq):
                                        yield tuple(state), seq[i + j]

        def random_state(self):
                return random.choice(self._state_list)

        def walk(self):
                '''Generate a walk through the chain.'''
                start = self.random_state()
                history = deque(start, maxlen=self.n_limit)
                while True:
                        node = self.walk_from(tuple(history))
                        history.append(node)
                        yield node

        def walk_from(self, state):
                '''Take one random step in the chain.'''
                while len(state):
                        nodes = self.transitions[state]
                        if nodes.total > 0:
                                return nodes.sample()
                        state = tuple(state[1:])
                return self.walk_from(self.random_state())
