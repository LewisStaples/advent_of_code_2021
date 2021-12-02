# adventOfCode 2021 day 2, parts 1 and 2
# https://adventofcode.com/2021/day/2

import sys

# Task 1:  Input Data
input_filename='input_sample0.txt'
input_list = []

with open(input_filename) as f:
    for in_string in f:
        [direction, number] = in_string.split()
        if direction not in ['forward', 'up', 'down']:
            sys.exit('Error! Bad direction: ' + direction)
        if not number.isdigit():
            sys.exit('Error! Bad number: ' + number)
        input_list.append((direction,int(number)))

# print(input_list)


# Task 2:  Solve part a
position = [0,0] # horizontal position, depth
for (direction, number) in input_list:
    # print(direction + ', ' + str(number))
    if direction == 'forward':
        position[0] += number
    if direction == 'down':
        position[1] += number
    if direction == 'up':
        position[1] -= number

# print('Final position is: ', end='')
# print(position)

print()
print('The answer to part a is: ', end='')
print(position[0] * position[1])
print()


# Task 3:  Solve part b
status = [0,0,0] # horizontal position, depth, aim
for (operation, unit_number) in input_list:
    if operation == 'down':
        status[2] += unit_number
    if operation == 'up':
        status[2] -= unit_number
    if operation == 'forward':
        status[0] += unit_number
        status[1] += status[2]*unit_number

    # print('input: ', end='')
    # print((operation, unit_number))

    # print('status: ', end='')
    # print(status)
    # print()

print('The answer to part b is: ', end='')
print(status[0] * status[1])
print()