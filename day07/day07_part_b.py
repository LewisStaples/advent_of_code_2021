# adventOfCode 2021 day 7, part b
# https://adventofcode.com/2021/day/6

import statistics
import enum
import sys

# calculate fuel required to move all submarines to the specified final position
def calc_fuel(horizontal_positions, alignment_position):
    ret_val = 0
    # loop through all submarines
    for sub in horizontal_positions:
        # loop through each unit of distance traveled
        for dist_remaining in range(abs(sub-alignment_position), 0, -1):
            # add fuel consumed for that unit of distance
            #
            # note that instead of calculating sum as 1+2+3+...
            # this loop calculates the sum as ...+3+2+1 (this gives the identical sum)
            ret_val += dist_remaining
    return ret_val

# this indicates whether fuel consumed is decreasing, at the minimum, or increasing
class FuelTrend(enum.Enum):
    DECREASING = -1
    MINIMUM    =  0
    INCREASING =  1
    ERROR      = 99

# this function indicates whether fuel consumed is decreasing, at the minimum, or increasing
# at position posn
def getFuelTrend(horizontal_positions, posn):
    left = calc_fuel(horizontal_positions, posn-1)
    mid = calc_fuel(horizontal_positions, posn)
    right  = calc_fuel(horizontal_positions, posn+1)

    if left < mid < right:
        return FuelTrend.INCREASING
    if right < mid < left:
        return FuelTrend.DECREASING
    if mid < right and mid < left:
        return FuelTrend.MINIMUM
    return FuelTrend.ERROR

print()

# read text file and write into horizontal_positions, which is a list of integers
input_filename='input.txt'
horizontal_positions = None

with open(input_filename) as f:
    horizontal_positions = [int(x) for x in f.readline().rstrip().split(',')]

median = statistics.median(horizontal_positions)
stdev = statistics.stdev(horizontal_positions)

bounds = [int(median-2*stdev-1), int(median+2*stdev+1)]

# assume that the minimum will between median-2*stdev and median+2*stdev
# therefore assert that lower bound must be decreasing, and upper bound increasing
# assert that bounds has getFuelTrend of decreasing for 0 and increasing for 1
if getFuelTrend(horizontal_positions, bounds[0]) != FuelTrend.DECREASING:
    sys.exit('FAILURE in bounds lower bound!')
if getFuelTrend(horizontal_positions, bounds[1]) != FuelTrend.INCREASING:
    sys.exit('FAILURE in bounds upper bound!')


while bounds[1]-bounds[0] > 1:
    midpoint = int(sum(bounds)/2)
    if getFuelTrend(horizontal_positions, midpoint) == FuelTrend.DECREASING:
        bounds[0] = midpoint
    elif getFuelTrend(horizontal_positions, midpoint) == FuelTrend.INCREASING:
        bounds[1] = midpoint
    elif getFuelTrend(horizontal_positions, midpoint) == FuelTrend.MINIMUM:
        # success!
        print('The answer to part b (fuel consumed) is ', end='')
        print(calc_fuel(horizontal_positions, midpoint), end='')
        sys.exit('')

sys.exit('WARNING: The program has ended unsuccessfully')
