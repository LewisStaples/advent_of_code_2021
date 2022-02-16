# adventOfCode 2021 day 24 helper 2
# https://adventofcode.com/2021/day/24


import enum


length_group = 18
input_filename='input.txt'
input_lines = []
for i in range(length_group):
    input_lines.append(dict())
# Reading input from the input file
with open(input_filename) as f:
    # Pull in each line from the input file
    for i, in_string in enumerate(f):
        in_string = in_string.rstrip()
        # print(in_string)
        # input_lines[i%length_group].add(in_string)
        if in_string not in input_lines[i%length_group]:
            input_lines[i%length_group][in_string] = []
        input_lines[i%length_group][in_string].append(i//length_group)
        # input_lines[i%length_group][in_string] = i//length_group


for i, ithgroup in enumerate(input_lines):
    print(i+1, end='')
    print('th line:')
    # if len(ithgroup) == 1:
        # print('ALL: ', end='')
        # print(ithgroup)
    print(ithgroup)
    # for the_str in ithgroup:
    #     print(the_str)
    print('---------------')

