# adventOfCode 2021 day 15
# https://adventofcode.com/2021/day/15


# Use BFS iteration now.  (Prior attempts used DFS recursion and then DFS iteration).  Keep paths in a collection of paths, and each path will be a collection of points.

# Have each position have a value of the lowest path risk found to that position so far, in addition to the given risk level for that position.  If the new path has a lower path risk from any path(s),


import copy
import sys

# filename of input file
input_filename='input_sample0.txt'

# This is the multiplier introduced in part B
multiplier = 5

# Collection of paths under consideration will be a list of tuples, with each tuple having two integers
paths_current = []
# This is a list of paths that are one step ahead of those in paths_current
paths_stepped_forward = []
# This is a list of paths that are complete (they have reached the destination)
paths_complete = []

# dictionary with index=point, value = (individual risk level, lowest path risk known)
point_risks = {}

(i_max, j_max) = (None, None)


def point_permitted(next_point, this_path):
    # Don't allow point to fall off of the grid
    (i,j) = next_point
    if True in [i<0, j<0, i>i_max, j>j_max]:
        return False

    # Don't allow point to repeat any prior point on this path
    if next_point in this_path:
        return False

    return True

def replace_path(new_path):
    # replace the higher risk path with this lower risk path
    for path_collection in [paths_current, paths_stepped_forward, paths_complete]:
        for i, old_path in enumerate(path_collection):
            if new_path[-1] in old_path:
                # NEEDS_TO_BE_TESTED !!!!
                index_op = old_path.index(new_path[-1])
                path_collection[i] = new_path[:-1] + old_path[index_op:]


def take_step():
    while len(paths_current) > 0:

        # consider one path from the list
        this_path = paths_current.pop()
        dummy = 123
        (i,j) = this_path[-1]

        # evaluate if the end has been reached already
        if i == i_max and j == j_max:
            dummy = 123
            paths_complete.append(this_path)
            continue
        # print(this_path)

        # consider the adjacent points in all four directions from (i,j)
        for next_point in [(i-1,j), (i+1,j), (i,j-1), (i,j+1)]:
            # if next_point can be added to the path
            if point_permitted(next_point, this_path):
                dummy = 123

                # calculate total risk for path that includes next_point
                next_point_path_risk = point_risks[this_path[-1]] \
                    ['lowest_path_risk'] + point_risks[next_point]['individual_risk']

                # If adding next_point to this_path doesn't yield 
                # any improvement to prior paths, then skip it
                if next_point_path_risk >= point_risks[next_point]['lowest_path_risk']:
                    continue

                # Adding next_point to this_path yields improvement to 
                # prior paths, therefore replace the prior paths
                new_path = copy.deepcopy(this_path)
                new_path.append(next_point)
                replace_path(new_path)

                # Reset point_risks to reflect this lower risk path
                point_risks[next_point]['lowest_path_risk'] = next_point_path_risk

                # Put this path in list of those that have already been stepped forward
                paths_stepped_forward.append(new_path)

    # transfer paths_stepped_forward to paths_current
    paths_current.extend(paths_stepped_forward)
    paths_stepped_forward.clear()

# print()

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
                    point_risks[(i + i_extra * i_tile, j + j_extra * j_tile)] = {'individual_risk' : risk_calc, 'lowest_path_risk' : float('inf')}

# # Now use the information in the top row of tiles to fill in the rest of the tiles
# for i2 in range(i+1):
#     for j2 in range(j+1):
#         top_tile_ind_risk = point_risks[(i2,j2)]['individual_risk']
#         for counter in range(1, multiplier):
#             point_risks[(i2 + counter * (i+1), j2)] = {'individual_risk': top_tile_ind_risk + counter, 'lowest_path_risk' : float('inf')}
# for dict_index in point_risks:
#     for counter in range(1, multiplier):
#         dummy = 123

(i_max, j_max) = (multiplier*(i+1)-1,multiplier*(j+1)-1)

# Collection of paths under consideration will be a list of tuples, with each tuple having two integers
paths_current.append([(0,0)])
point_risks[(0,0)] = {'individual_risk' : float('inf'), 'lowest_path_risk' : 0}

while len(paths_current) > 0:
    take_step()

print('The answer to part b is: ', end='')
print(point_risks[(i_max, j_max)]['lowest_path_risk'])
print()
