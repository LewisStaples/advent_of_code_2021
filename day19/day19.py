# adventOfCode 2021 day 19
# https://adventofcode.com/2021/day/19

import re

class Scanner:
    def __init__(self):
        self.point_list = []
        self.edges = dict()

    def load_point(self, point_tuple):
        self.point_list.append(point_tuple)

ScannerList = []

# reading input from the input file
input_filename='input.txt'
with open(input_filename) as f:
    # pull in each line from the input file
    for in_string in f:
        in_string = in_string.rstrip()
        if len(in_string) == 0:
            continue
        if re.match('--- scanner', in_string):
            ScannerList.append(Scanner())
        else:
            ScannerList[-1].load_point(tuple(in_string.split(',')))

# testing input of points
for index, scanner in enumerate(ScannerList):
    print('Scanner # ' + str(index))
    for point in scanner.point_list:
        print(point)

    