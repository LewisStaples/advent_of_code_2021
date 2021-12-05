# adventOfCode 2021 day 4, parts 1 and 2
# https://adventofcode.com/2021/day/5

input_filename='input_scenario0.txt'

with open(input_filename) as f:
    for in_string in f:
        print(in_string.rstrip().split(' -> '))


# plan:
# For each line of input
# Create multiple 2-tuples with all points in that segment
# Have two sets containing those tuples
# The first set will be for points with at least one line there
# The second set will be for points with at least two lines there
# The answer will be the length of the second set
