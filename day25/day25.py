# adventOfCode 2021 day 25
# https://adventofcode.com/2021/day/25

import re

class SeaCucumber:
    def __init__(self):
        # Python dictionaries about east-bound and south-bound herds
        # Each will have the row as the index and the value will be a list of all column numbers within that row with that character
        self.east_herd = dict()
        self.south_herd = dict()
        self.ROW_TOTAL = None
        self.COLUMN_TOTAL = None

        # Reading input from the input file
        input_filename='input_sampleN.txt'
        with open(input_filename) as f:
            # Pull in each line from the input file
            for row_number, in_string in enumerate(f):
                in_string = in_string.rstrip()

                self.east_herd[row_number] = [m.start() for m in re.finditer('>', in_string)]
                self.south_herd[row_number] = [m.start() for m in re.finditer('v', in_string)]

                # Capture before the variable goes out of scope.
                # (Unfortunately, it will be unnecessarily noted each time through)
                self.COLUMN_TOTAL = len(in_string)

    # This is for testing only.  (To compare to the given example)
    def display(self):
        for row_number in self.east_herd.keys():
            for col_number in range(self.COLUMN_TOTAL):
                if col_number in self.east_herd[row_number]:
                    print('>', end='')
                elif col_number in self.south_herd[row_number]:
                    print('v', end='')
                else:
                    print('.', end='')
            print()

seaCucumber = SeaCucumber()
seaCucumber.display()
