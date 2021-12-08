# adventOfCode 2021 day 5, part a
# https://adventofcode.com/2021/day/5

input_filename='input.txt'

points__one_or_more = set()
points__two_or_more = set()


with open(input_filename) as f:
    # pull in each line from the input file
    for in_string in f:
        # convert each line to a list of integers (with four elements)
        in_list = list([int(x) for x in in_string.rstrip().replace(' -> ',',').split(',')])

        # part a will only consider vertical or horizontal segments, so ignore any diagonals
        if (in_list[0]!=in_list[2] and in_list[1]!=in_list[3]):
            continue

        # this scenario didn't appear
        if (in_list[0]==in_list[2] and in_list[1]==in_list[3]):
            print('input is a point')
            print(in_string)
            print()

        # determine whether the value increases or decreases along axis (x and then y)
        i_step = 1 if in_list[2] > in_list[0] else -1 # 1 or -1
        j_step = 1 if in_list[3] > in_list[1] else -1 # 1 or -1

        # create line segments to fill in each point between endpoints
        for i in range(in_list[0], in_list[2]+i_step,i_step):
            for j in range(in_list[1], in_list[3]+j_step, j_step):
                new_point = (i,j)
                if new_point in points__one_or_more:
                    points__two_or_more.add(new_point)
                points__one_or_more.add(new_point)


# output the answer
print()
print('The answer to a is ', end='')
print(len(points__two_or_more))
