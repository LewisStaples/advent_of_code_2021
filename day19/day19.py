# adventOfCode 2021 day 19
# https://adventofcode.com/2021/day/19

import re
import math
import sys
import copy

class Scanner:
    def __init__(self):
        self.point_list = []
        self.edges = dict()
        self.lengths_squared = set()

    def load_point(self, point):
        self.point_list.append(point)

    def determine_edges(self):
        for p1_index in range(len(self.point_list) - 1):
            for p2_index in range(p1_index + 1, len(self.point_list)):
                length_squared = 0
                for comp_index in range(len(self.point_list[p1_index])):
                    length_squared += (self.point_list[p1_index][comp_index] - self.point_list[p2_index][comp_index])**2
                self.edges[length_squared] = (p1_index, p2_index)
                self.lengths_squared.add(length_squared)
        dummy = 123

scannerListUntransformed = []
scannerListTransformed = []

# For 12 common beacons there should be 1+2+...+11 = 66 This may be proven using recursive logic where adding a new point to a graph of n points creates n new edges. So start with n=1 point with no initial edges, then adding a second point adds a single edge (1 in total), then adding a third point yields two new edges (3 total), and so on.
REQUIRED_NUMBER_OF_EQUAL_LENGTH_EDGES = 66

def get_scanner_pair():
    for this_scanner_transformed in scannerListTransformed:
        for this_scanner_untransformed in scannerListUntransformed:
            if len(this_scanner_transformed.lengths_squared.intersection(this_scanner_untransformed.lengths_squared)) > 11:
                return (this_scanner_transformed, this_scanner_untransformed)

def transform(this_scanner_transformed, this_scanner_untransformed):
    # Look for two connected edges in both the transformed and untransformed scanners
    lengths_squared_in_common = this_scanner_transformed.lengths_squared.intersection(this_scanner_untransformed.lengths_squared)
    edge0_length = lengths_squared_in_common.pop()
    edge0_tr = this_scanner_transformed.edges[edge0_length]
    edge1_tr = edge0_untr = edge1_untr = None
    for edge1_length in lengths_squared_in_common:
        if edge0_tr[0] in this_scanner_transformed.edges[edge1_length]:
            edge1_tr = this_scanner_transformed.edges[edge1_length]
            edge0_untr = this_scanner_untransformed.edges[edge0_length]
            edge1_untr = this_scanner_untransformed.edges[edge1_length]
            break # found edge1 (no need to look for any other acceptable edge1 possibilities)

    # Identify three beacons (points) that are represented in both the transformed and untransformed scanners by creating a list of three 2-tuples (tr. vs. untr.) of 3-tuples (3 coordinates, defining location of the beacon).
    beacon_list = []
    tr_middle = set(edge0_tr).intersection(set(edge1_tr)).pop()
    untr_middle = set(edge0_untr).intersection(set(edge1_untr)).pop()

    # Indicating point where edge0 and edge1 meet
    beacon_list.append(
        [this_scanner_untransformed.point_list[untr_middle],
        this_scanner_transformed.point_list[tr_middle]]
    )

    tr_0 = list(edge0_tr)
    tr_0.remove(tr_middle)
    tr_0 = tr_0.pop()
    untr_0 = list(edge0_untr)
    untr_0.remove(untr_middle)
    untr_0 = untr_0.pop()
    beacon_list.append(
        [this_scanner_untransformed.point_list[untr_0],
        this_scanner_transformed.point_list[tr_0]]
    )

    tr_1 = list(edge1_tr)
    tr_1.remove(tr_middle)
    tr_1 = tr_1.pop()
    untr_1 = list(edge1_untr)
    untr_1.remove(untr_middle)
    untr_1 = untr_1.pop()
    beacon_list.append(
        [this_scanner_untransformed.point_list[untr_1],
        this_scanner_transformed.point_list[tr_1]]
    )

    # Use one of these points to define the (x,y) displacement between the scanners.  
    displacement = []
    for i in range(len(beacon_list[0][0])):
        displacement.append(beacon_list[0][0][i] - beacon_list[0][1][i])
    for i in range(len(beacon_list)):
        for j in range(len(beacon_list[0])):
            for k in range(len(beacon_list[0][0])):
                beacon_list[i][j][k] -= displacement[k]
                
    # Use the above (x,y) displacement, along with the 24 available rotations to identify the rotation that works for the other two untransformed points.

    # Apply the known (x,y) displacement and rotation to all untransformed points

    # Relabel the untransformed scanner list as now having been transformed
    scannerListTransformed.append(this_scanner_untransformed)
    scannerListUntransformed.remove(this_scanner_untransformed)

# reading input from the input file
input_filename='input.txt'
print('Using input file ', end='')
print(input_filename)
with open(input_filename) as f:
    # pull in each line from the input file
    for in_string in f:
        in_string = in_string.rstrip()
        if len(in_string) < 2:
            scannerListUntransformed[-1].determine_edges()
            continue
        if re.match('--- scanner', in_string):
            scannerListUntransformed.append(Scanner())
        else:
            scannerListUntransformed[-1].load_point(list([int(x) for x in in_string.split(',')]))
    # get last line
    scannerListUntransformed[-1].determine_edges()

# Remove one Scanner from cannerListUntransformed and add it as-is to cannerListTransformed
this_scanner_untransformed = scannerListUntransformed.pop()
scannerListTransformed.append(this_scanner_untransformed)
dummy = 123

while len(scannerListUntransformed) > 0:
    scanner_pair = get_scanner_pair()
    transform(*scanner_pair)

print('The answer is:')
print('(To be determined)')
