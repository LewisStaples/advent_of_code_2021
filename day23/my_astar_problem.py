# Trying out my own program using implementation of a* from https://pypi.org/project/astar
# https://github.com/jrialland/python-astar

import astar

class MyAStarProblem(astar.AStar):
    def __init__(self):
        self.edges = {
            'AB': 10,
            'BC': 20,
            'CD': 10,
            'AD': 100
        }

    # For a given node, returns (or yields) the list of its neighbor:
    def neighbors(self, node):
        ret_val = []
        for key in self.edges.keys():
            if node in key:
                ret_val += key.replace(node, '')
        return ret_val

    # Gives the real distance/cost between two adjacent nodes n1 and n2
    def distance_between(self, n1, n2):
        for key in self.edges.keys():
            if n1 in key:
                if n2 in key:
                    return self.edges[key]

    # Computes the estimated (rough) distance/cost between a node and the goal. 
    # Per https://en.wikipedia.org/wiki/Admissible_heuristic , this must not be greater than the actual value
    def heuristic_cost_estimate(self, current, goal):
        return 0

masp = MyAStarProblem()

# Confirming that function neighbors is working
print(masp.neighbors('A'))
print(masp.neighbors('B'))
print(masp.neighbors('C'))
print(masp.neighbors('D'))
print()

# Confirming that function distance_between is working
print(masp.distance_between('A','B'))
print(masp.distance_between('B','A'))
print(masp.distance_between('B','C'))
print(masp.distance_between('C','D'))
print(masp.distance_between('A','D'))
print()

# Confirming that function heuristic_cost_estimate is working
print(masp.heuristic_cost_estimate('A','D'))
print()

# Solve problem, and show path
print(list(masp.astar('A', 'D')))

# Change problem, solve problem, and show path
masp.edges['BC'] = 2000
print(list(masp.astar('A', 'D')))
