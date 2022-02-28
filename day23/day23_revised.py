# adventOfCode 2021 day 23
# https://adventofcode.com/2021/day/23

from re import L
import sys



input_filename='input.txt'
# Reading input from the input file
with open(input_filename) as f:
    line_length = None
    # Pull in each line from the input file
    for row_num, in_string in enumerate(f):
        # print(in_string)

        # Require assumptions about input
        if row_num == 0:
            # Require line to be all pound characters
            line_length = len(in_string) - 1
            if in_string.rstrip() != '#'*line_length:
                sys.exit('Bad input!')
            dummy = 123  
        elif row_num == 1:
            # Require line to have one pound at start and finish and all periods inside
            if in_string.rstrip() != '#'+'.'*(line_length-2)+'#':
                sys.exit('Bad input!')
            dummy = 123
        dummy = 123

