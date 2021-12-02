# adventOfCode 2021 day 2, parts 1 and 2
# https://adventofcode.com/2021/day/2

# Task 1:  Input Data
input_filename='input_sample0.txt'
input_list = []

with open(input_filename) as f:
    for in_string in f:
        [direction, number] = in_string.split()
        if direction not in ['forward', 'up', 'down']:
            print('Error! Bad direction: ' + direction)
        if not number.isdigit():
            print('Error! Bad number: ' + number)
        input_list.append((direction,int(number)))

print(input_list)




