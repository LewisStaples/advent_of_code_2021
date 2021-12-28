# adventOfCode 2021 day 15
# https://adventofcode.com/2021/day/15


# Latest approach ...
#
# Use iteration on a set of leading edge points.  Each iterative step 
# will expand from each leading each point to its neighbors.
#
# Dictionary point_risk's index is as a 2-tuple of coordinates for 
# every point.  Dict point_risk's value is another dict with two 
# indices: 'individual_risk' and 'lowest_path_risk.'  The values 
# of these are the individual risk from the given input and the 
# lowest total risk of any path to that point from the starting position.

import copy
import sys

# filename of input file
input_filename='input.txt'

# This is the multiplier introduced in part B
# For part A, this value should be 1.  
# For part B, this value is given as 5
# (program output will interpret any non-1 value as being a part B problem)
multiplier = 5

# This is a set of leading edge points.  
leading_edge_points = set()

# dictionary with index=point, 
# value = (individual risk level, lowest path risk known)
point_risks = {}

# highest values of point coordinates
(i_max, j_max) = (None, None)

# This function returns True if a point is permitted (if it is on the grid)
# This function returns False if a point is off the grid
def point_permitted(next_point):
    (i,j) = next_point
    if True in [i<0, j<0, i>i_max, j>j_max]:
        return False
    # The tests have passed
    return True

# This function solves the problem (searches for the smallest total risk
# for any path from the starting point to the ending point)
def solve_problem():
    while len(leading_edge_points) > 0:
        # consider one point from the list of leading edge points
        (i,j) = leading_edge_points.pop()

        # evaluate if the end has been reached already
        if i == i_max and j == j_max:
            continue

        # consider the adjacent points in all four directions from (i,j)
        for next_point in [(i-1,j), (i+1,j), (i,j-1), (i,j+1)]:
            # if next_point can be added to the path
            if point_permitted(next_point):
                # calculate total for new_point when approached from (i,j)
                next_point_path_risk = point_risks[(i,j)]['lowest_path_risk'] \
                    + point_risks[next_point]['individual_risk']

                # If approaching next_point from (i,j) doesn't yield 
                # any improvement to any prior paths that lead to there, skip it
                if next_point_path_risk >= point_risks[next_point]['lowest_path_risk']:
                    continue

                # Reset point_risks to reflect this lower risk path
                point_risks[next_point]['lowest_path_risk'] = next_point_path_risk

                # Add next_point to set, so program can review its neighbors
                leading_edge_points.add(next_point)

# End of function solve_problem()


# Read input file to determine the size of the file
with open(input_filename) as f:
    for i, in_string in enumerate(f):
        # for j, risk in enumerate(in_string.rstrip()):
        pass
    f.close()
# dimenions of a single "tile" (also file dimensions)
(i_tile, j_tile) = (i+1, len(in_string.rstrip()))
# maximum values of i, j
(i_max, j_max) = (i_tile*multiplier-1, j_tile*multiplier-1)

# Read input from the input file, which leads to filling in the "individual risk"
# associated with points all in the cave.

# First read each line from input. The resulting output yields information 
# for all points in the top row of "tiles" within the cave.
with open(input_filename) as f:
    # pull in each line from the input file
    for i, in_string in enumerate(f):
        for j, risk in enumerate(in_string.rstrip()):
            for i_extra in range(multiplier):
                for j_extra in range(multiplier):
                    risk_calc = int(risk) + i_extra + j_extra
                    while risk_calc > 9:
                        risk_calc -= 9
                    point_risks[(i + i_extra * i_tile, j + j_extra * j_tile)] \
                        = {'individual_risk' : risk_calc, \
                            'lowest_path_risk' : float('inf')}

(i_max, j_max) = (multiplier*(i+1)-1,multiplier*(j+1)-1)

# The initial leading edge will be a single point
leading_edge_points.add( (0,0) )

# Risks for starting point artificially changed to discourage any repeat
# visits to the starting point
point_risks[(0,0)] = {'individual_risk' : float('inf'), 'lowest_path_risk' : 0}

solve_problem()

# Output results
print('The answer to ', end='')
print('part A', end='') if multiplier == 1 else print ('part B with mulitiplier ' + str(multiplier), end='')
print(' is: ', end='')
print(point_risks[(i_max, j_max)]['lowest_path_risk'])
print()
