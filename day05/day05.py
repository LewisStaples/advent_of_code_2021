# adventOfCode 2021 day 4, parts 1 and 2
# https://adventofcode.com/2021/day/5

input_filename='input_scenario0.txt'

with open(input_filename) as f:
    for in_string in f:
        print(in_string.rstrip().split(' -> '))


    # number_draws = [int(i) for i in f.readline().rstrip().split(',')]
    # bingo_board_being_created = None
    # for line_num, in_string in enumerate(f):
        # print(line_num, end=': ')
        # print(in_string.rstrip())
