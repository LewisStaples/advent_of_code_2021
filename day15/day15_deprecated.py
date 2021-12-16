# adventOfCode 2021 day 15
# https://adventofcode.com/2021/day/15

from os import path


class CavePosition:
    def __init__(self, risk_level):
        self.risk_level = risk_level


class CavePaths:
    def __init__(self):
        self.grid = []
        self.paths = [[(0,0)]]  # [[]] #
        self.best_path_energy = float('inf')
    
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

    def point_permitted_on_path(self, point, path_index):
        # don't allow point to fall off of the grid
        (i,j) = point
        if True in [i<0, j<0, i>=len(self.grid), j>=len(self.grid[0])]:
            return False
        # don't allow point to repeat any prior point on the path
        if point in self.paths[path_index]:
            return False
        # since neither constraint is violated, it is permitted
        return True

    # path_index is the index in self.paths of the path
    # being passed to this function
    # i, j are the potential point to add to the path
    def recur_call(self, path_index): # , i, j):
        # find the last point (i,j) in the path passed to this call
        (i,j) = self.paths[path_index][-1]

        # test if the end has been reached succesfully
        if i == len(self.grid)-1 and j == len(self.grid[0])-1:
            risk = self.calc_path_risk(self.paths[path_index])
            return (path_index,risk)

        # if yes .... what is to be done ????
        # return the risk along the path

        # consider the adjacent points in all four directions from (i,j)
        for next_point in [(i-1,j), (i+1,j), (i,j-1), (i,j+1)]:
            if self.point_permitted_on_path(next_point, path_index):
                self.paths.append(self.paths[path_index].append(next_point))
                # compute index of the newest path and do recursive call with it
                self.recur_call(len(self.paths)-1)

            # remove the orig. path (either it's a deadend or it's been replaced)
            # CANT DO THIS .... it's reshuffling the indices
            # self.paths[path_index] = None

            # self.recur_call(next_point)
        #     self.recur_call(next_point) if self.point_permitted_on_path(next_point, path)

        # if self.point_permitted_on_path(i,j, path_index):
        #     self.paths[path_index].append((i,j)) 


    def find_best_path(self):
        # this_path = self.paths[0]
        self.recur_call(0) #, 0, 0)
        # posn = self.paths[0][0]
        # for i in range(3): # later replace with infinite loop with breakout logic
        #     dummy = 123

cavepaths = CavePaths()
# reading input from the input file
input_filename='input_scenario0.txt'
with open(input_filename) as f:
    # pull in each line from the input file
    for in_string in f:
        cavepaths.input_line(in_string.rstrip())

cavepaths.find_best_path()

cavepaths.calc_path_risk([(0,0), (1,0), (1,1),(0,1)])



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



