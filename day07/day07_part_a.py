# adventOfCode 2021 day 7, part a
# https://adventofcode.com/2021/day/7

import statistics

# calculate fuel required to move all submarines to the specified final position
def calc_fuel(horizontal_positions, alignment_position):
    ret_val = 0
    for sub in horizontal_positions:
        ret_val += abs(sub - alignment_position)
    return ret_val

input_filename='input.txt'
horizontal_positions = None

# read text file and write into horizontal_positions, which is a list of integers
with open(input_filename) as f:
    horizontal_positions = [int(x) for x in f.readline().rstrip().split(',')]

median = statistics.median(horizontal_positions)

# using the median solves part a (see part b for searching for the solution)
print('The answer to part a (fuel consumed) is ', end='')
print(calc_fuel(horizontal_positions, median))

