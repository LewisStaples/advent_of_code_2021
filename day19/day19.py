# adventOfCode 2021 day 19
# https://adventofcode.com/2021/day/19

import re
import math

class Scanner:
    def __init__(self):
        self.point_list = []
        self.edges = dict()
        self.lengths_squared = set()

    def load_point(self, point_tuple):
        self.point_list.append(point_tuple)

    def determine_edges(self):
        for p1_index in range(len(self.point_list) - 1):
            for p2_index in range(p1_index + 1, len(self.point_list)):
                length_squared = 0
                for comp_index in range(len(self.point_list[p1_index])):
                    length_squared += (self.point_list[p1_index][comp_index] - self.point_list[p2_index][comp_index])**2
                self.edges[(p1_index, p2_index)] = length_squared
                self.lengths_squared.add(length_squared)
        dummy = 123

scannerListUntransformed = []
scannerListTransformed = []

# For 12 common beacons there should be 1+2+...+11 = 66 This may be proven using recursive logic where adding a new point to a graph of n points creates n new edges. So start with n=1 point with no initial edges, then adding a second point adds a single edge (1 in total), then adding a third point yields two new edges (3 total), and so on.
REQUIRED_NUMBER_OF_EQUAL_LENGTH_EDGES = 66

def transform_scanner():
    for i_tr, this_scanner_transformed in enumerate(scannerListTransformed):
        for i_untr,this_scanner_untransformed in enumerate(scannerListUntransformed):
            if len(this_scanner_transformed.lengths_squared.intersection(this_scanner_untransformed.lengths_squared)) > 11:
                print('match!')
                scannerListTransformed.append(this_scanner_untransformed)
                scannerListUntransformed.remove(this_scanner_untransformed)
                return

# reading input from the input file
input_filename='input.txt'
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
            scannerListUntransformed[-1].load_point(tuple([int(x) for x in in_string.split(',')]))
    # get last line
    scannerListUntransformed[-1].determine_edges()

while len(scannerListUntransformed) > 0:
    # Remove one Scanner from cannerListUntransformed and add it as-is to cannerListTransformed
    this_scanner_untransformed = scannerListUntransformed.pop()
    scannerListTransformed.append(this_scanner_untransformed)
    transform_scanner()

dummy = 123

