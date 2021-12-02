# adventOfCode 2021 day 2, parts 1 and 2
# https://adventofcode.com/2021/day/2

# Task 1:  Input Data
input_filename='input.txt'
input_list = []

with open(input_filename) as f:
    for in_string in f:
        [direction, number] = in_string.split()
        if direction not in ['forward', 'up', 'down']:
            print('Error! Bad direction: ' + direction)
        if not number.isdigit():
            print('Error! Bad number: ' + number)
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

print('The answer to part a is: ', end='')
print(position[0] * position[1])


