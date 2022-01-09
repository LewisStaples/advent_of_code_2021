# adventOfCode 2021 day 19
# https://adventofcode.com/2021/day/19

import re
import math

class Scanner:
    def __init__(self):
        self.point_list = []
        self.edges = dict()

    def load_point(self, point_tuple):
        self.point_list.append(point_tuple)

    def determine_edges(self):
        for p1_index in range(len(self.point_list) - 1):
            for p2_index in range(p1_index + 1, len(self.point_list)):
                length = 0
                for comp_index in range(len(self.point_list[p1_index])):
                    length += (self.point_list[p1_index][comp_index] - self.point_list[p2_index][comp_index])**2
                length = math.sqrt(length)
                self.edges[(p1_index, p2_index)] = {'length':length}

ScannerList = []

# reading input from the input file
input_filename='input_scenario0.txt'
with open(input_filename) as f:
    # pull in each line from the input file
    for in_string in f:
        in_string = in_string.rstrip()
        if len(in_string) < 2:
            ScannerList[-1].determine_edges()
            
            continue
        if re.match('--- scanner', in_string):
            ScannerList.append(Scanner())
        else:
            ScannerList[-1].load_point(tuple([int(x) for x in in_string.split(',')]))
    # get last line
    ScannerList[-1].determine_edges()
# testing input of points
for index, scanner in enumerate(ScannerList):
    print('Scanner # ' + str(index))
    for point in scanner.point_list:
        print(point)

    # testing calculation of edge lengths
    print(scanner.edges)

    print()
