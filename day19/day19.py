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
                self.edges[(p1_index, p2_index)] = {'length_squared':length_squared}
                self.lengths_squared.add(length_squared)

scannerList = []

# reading input from the input file
input_filename='input_sample2.txt'
with open(input_filename) as f:
    # pull in each line from the input file
    for in_string in f:
        in_string = in_string.rstrip()
        if len(in_string) < 2:
            scannerList[-1].determine_edges()
            continue
        if re.match('--- scanner', in_string):
            scannerList.append(Scanner())
        else:
            scannerList[-1].load_point(tuple([int(x) for x in in_string.split(',')]))
    # get last line
    scannerList[-1].determine_edges()

# testing input of points
for index, scanner in enumerate(scannerList):
    print('Scanner # ' + str(index))
    # for point in scanner.point_list:
    #     print(point)

    # # testing calculation of edge squared lengths
    # print(scanner.edges)

    # printing set of lengths_squared
    print(scanner.lengths_squared)
    print()

# Printing intersections of pairs of sets of lengths_squared from pairs of edges
# For 12 common beacons there should be 1+2+...+11 = 66 (This is due to recursive logic where adding a new point to a graph of n points creates n new edges. So start with n=1 point with no initial edges)
# I assume that no pairs of points will have the same exact distance between them.
for i in range(len(scannerList)-1):
    for j in range(i+1, len(scannerList)):
        int_len = len(scannerList[i].lengths_squared.intersection(scannerList[j].lengths_squared))
        if int_len >= 66:
            print(str(i) + ',' + str(j), end=': ')
            print(int_len)

