# adventOfCode 2021 day 5, parts a and b
# https://adventofcode.com/2021/day/5

input_filename='input.txt'

points__one_or_more = set()
points__two_or_more = set()


with open(input_filename) as f:
    for in_string in f:
        # print(in_string)
        in_list = list([int(x) for x in in_string.rstrip().replace(' -> ',',').split(',')])
        # print(in_list)

        # for part a, only consider vertical or horizontal segments
        if (in_list[0]!=in_list[2] and in_list[1]!=in_list[3]):
            continue

        if (in_list[0]==in_list[2] and in_list[1]==in_list[3]):
            print('input is a point')
            print(in_string)
            print()

        i_step = 1 if in_list[2] > in_list[0] else -1 # 1 or -1
        j_step = 1 if in_list[3] > in_list[1] else -1 # 1 or -1

        for i in range(in_list[0], in_list[2]+i_step,i_step):
            for j in range(in_list[1], in_list[3]+j_step, j_step):
                # print(str(i) + ', ' + str(j))
                new_point = (i,j)
                if new_point in points__one_or_more:
                    points__two_or_more.add(new_point)
                points__one_or_more.add(new_point)

print()
print('set with two or more: ', end='')
print(points__two_or_more)
# print('set with one or more: ', end='')
# print(points__one_or_more)
print()

print('The answer to a is ', end='')
print(len(points__two_or_more))



# plan:
# For each line of input
# Create multiple 2-tuples with all points in that segment
# Have two sets containing those tuples
# The first set will be for points with at least one line there
# The second set will be for points with at least two lines there
# The answer will be the length of the second set
