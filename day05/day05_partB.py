# adventOfCode 2021 day 5, part b
# https://adventofcode.com/2021/day/5

input_filename='input.txt'

points__one_or_more = set()
points__two_or_more = set()

# this function determines and returns
# flag values depending on which of two numeric
# values is larger, or if they are equal
def calc_increment(val1, val2):
    if val1==val2:
        return 0
    if val1 < val2:
        return 1
    if val1 > val2:
        return -1

with open(input_filename) as f:
    # pull in each line from the input file
    for in_string in f:
        # convert each line to a list of integers (with four elements)
        in_list = list([int(x) for x in in_string.rstrip().replace(' -> ',',').split(',')])

        # calculate the number of points in the line:
        points_in_line = max([abs(in_list[2] - in_list[0]), abs(in_list[3] - in_list[1])])

        # determine whether the value increases or decreases along axis (x and then y)
        i_step = calc_increment(in_list[0], in_list[2])
        j_step = calc_increment(in_list[1], in_list[3])

        # create line segments to fill in each point between endpoints
        for k in range(points_in_line+1):
            i = in_list[0] + k*i_step
            j = in_list[1] + k*j_step
            new_point = (i,j)
            if new_point in points__one_or_more:
                points__two_or_more.add(new_point)
            points__one_or_more.add(new_point)

# output the answer
print()
print('The answer to b is ', end='')
print(len(points__two_or_more))
print()



