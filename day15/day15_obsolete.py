# adventOfCode 2021 day 15
# https://adventofcode.com/2021/day/15

import copy
import sys

class CavePosition:
    def __init__(self, risk_level):
        self.risk_level = risk_level


class CavePaths:
    def __init__(self):
        self.grid = []
        self.lowest_path_risk = float('inf')
        self.path_stack = []
    
    # calculate risk from a path
    def calc_path_risk(self, path):
        ret_val = 0
        for posn in path[1:]:
            # print(posn)
            ret_val += self.grid[posn[0]][posn[1]].risk_level
            # dummy = 123
        # pass
        return ret_val

    def input_line(self, in_line):
        self.grid.append([CavePosition(int(x)) for x in in_line])
        dummy=123

    def point_permitted_on_path(self, point, path):
        # don't allow point to fall off of the grid
        (i,j) = point
        if True in [i<0, j<0, i>=len(self.grid), j>=len(self.grid[0])]:
            return False
        # don't allow point to repeat any prior point on the path
        if point in path:
            return False
        # since neither constraint is violated, it is permitted
        return True

    # path_is the path
    # being passed to this function
    # i, j are the potential point to add to the path
    def recur_call(self): # , i, j):
        # ret_val = float('inf')
        while len(self.path_stack) > 0:
            # find the last point (i,j) in the path passed to this call
            path = self.path_stack.pop()
            (i,j) = path[-1]

            # test if the end has been reached
            if i == len(self.grid)-1 and j == len(self.grid[0])-1:
                # update value of best possible path found
                risk = self.calc_path_risk(path)
                self.lowest_path_risk = min(risk, self.lowest_path_risk)
                # return risk
                continue

            # consider the adjacent points in all four directions from (i,j)
            for next_point in [(i-1,j), (i+1,j), (i,j-1), (i,j+1)]:
                # if next_point can be added to the path
                if self.point_permitted_on_path(next_point, path):
                    # then create newpath by adding next_point
                    newpath = copy.deepcopy(path)
                    newpath.append(next_point)

                    # protection from infinite loops
                    # if len(newpath) > 1000000:
                    #     sys.exit('newpath is too large')

                    # if newpath has higher risk than the best previously discovered that 
                    # goes to the end so far, skip it ... this speeds up the program
                    if self.calc_path_risk(newpath) >= self.lowest_path_risk:
                        continue
                    # do recursive call with the new path
                    # ret_val = min(ret_val, self.recur_call(newpath))
                    self.path_stack.append(newpath)

            # return ret_val
            

    def find_best_path(self):
        self.path_stack.append([(0,0)])
        self.recur_call()

        print('The smallest total risk for all paths is ', end='')
        print(self.lowest_path_risk)
        print()

        # self.recur_call(0) #, 0, 0)
        # print( self.recur_call([(0,0)]) )
        # for i in range(3): # later replace with infinite loop with breakout logic
        #     dummy = 123

cavepaths = CavePaths()
# reading input from the input file
input_filename='input.txt'
with open(input_filename) as f:
    # pull in each line from the input file
    for in_string in f:
        cavepaths.input_line(in_string.rstrip())

cavepaths.find_best_path()



# ideas ....
# start by considering all possible permutations of paths from the start position
# when all possiblities to a point are exhausted, associate the best path to that point with the point
# exhaustion happens 
# even better .... only keep a few groups of paths to the leading edge, and drop paths that are known to be inferior
#
# use recursion to consider all paths
#
# there will be a grid of objects of a class
# each object will have risk_level (from input)
# best currently known path to the object, total path risk
#
# flag True/False if the optimal path has been found
# 
# leading edge of all paths
#
# paths can never switchback, but that will obviously be wasteful



