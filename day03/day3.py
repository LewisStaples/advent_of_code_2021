# adventOfCode 2021 day 3, parts 1 and 2
# https://adventofcode.com/2021/day/3

from enum import Enum
from types import MethodDescriptorType

class Superlative(Enum):
    most_common = 0
    least_common = 1

class PuzzleInput:
    def __init__(self):
        # puzzle_input is also known as "diagnostic report", list of lists of integers
        self.puzzle_input = []

    def __str__(self):
            return str(self.puzzle_input)

    def add_line_list(self, line_list ):
        self.puzzle_input.append(line_list)

    # this returns a line as an integer
    def get_line_integer(self, line_num):
        str_rep = ''
        for bit in self.puzzle_input[line_num]:
            str_rep += str(bit)
        return int(str_rep,2)

    # this is the number of lines in the original input
    def length(self):
        return len(self.puzzle_input)

    # this is the length of each line in the original input
    # (the length of line 0 is returned, but this is assumed to be constant)
    def line_length(self):
        return len(self.puzzle_input[0])

    # this returns an integer with either most or least common bit
    def superlative_common_bit(self, number_index_list, bit_number, which_superlative):
        sum=0
        for index in number_index_list:
            sum += self.puzzle_input[index][bit_number]
        # most_common_bit = sum/(len(number_index_list))
        if sum/(len(number_index_list)) >= 0.5:
            most_common_bit = 1
        else:
            most_common_bit = 0
        if which_superlative == Superlative.most_common:
            return most_common_bit
        else:
            return (most_common_bit+1)%2

    def reduce_number_index_list(self, number_index_list, bit_number, bit_to_match):
        new_number_index_list = []
        for number_index in number_index_list:
            if self.puzzle_input[number_index][bit_number] == bit_to_match:
                new_number_index_list.append(number_index)    
        return new_number_index_list

# Task 1:  Input data
input_filename='input.txt'
# puzzle_input is also known as "diagnostic report", list of lists of integers
# puzzle_input = [] 
puzzle_input = PuzzleInput()

with open(input_filename) as f:
    for in_string in f:
        # print(in_string.rstrip())
        line_list = []
        for ch in in_string.rstrip():
            # print(ch)
            line_list.append(int(ch))
        # puzzle_input.append(line_list)
        puzzle_input.add_line_list(line_list)
        # print()

# print(puzzle_input)
# print()


# Task 2:  Solve part a
gamma_str = ''
epsilon_str = ''

# create list of indices in puzzle_input to be considered
# (for part a it is all indices in puzzle_input, but this will change in part b)
number_index_list_gamma = [x for x in range(puzzle_input.length())]
number_index_list_epsilon = [x for x in range(puzzle_input.length())]

# print('number_index_list_gamma')
# print(number_index_list_gamma)
# print()

for line_index in range(puzzle_input.line_length()):
    gamma_str += str(puzzle_input.superlative_common_bit(number_index_list_gamma, line_index, Superlative.most_common))
    epsilon_str += str(puzzle_input.superlative_common_bit(number_index_list_epsilon, line_index, Superlative.least_common))

# print(gamma_str)
# print(int(gamma_str,2))
# print()

# print(epsilon_str)
# print(int(epsilon_str,2))
# print()

# print('number_index_list_gamma ', end='')
# print(number_index_list_gamma , end=', ')
# print('number_index_list_epsilon ', end='')
# print(number_index_list_epsilon , end=', ')

print('The solution to part a is ', end='')
print(int(gamma_str,2)*int(epsilon_str,2))
print()


# Task 3:  For part b, determine gamma:

for line_index in range(puzzle_input.line_length()):
    gamma_bit = puzzle_input.superlative_common_bit(number_index_list_gamma, line_index, Superlative.most_common)

    # reduce number_index_list-s
    number_index_list_gamma = puzzle_input.reduce_number_index_list(number_index_list_gamma, line_index, gamma_bit)


    # print('line_index: ', end='')
    # print(line_index, end=', ')
    # print('number_index_list_gamma ', end='')
    # print(number_index_list_gamma , end=', ')
    # print()

    if len(number_index_list_gamma) < 2:
        break

# print()

# Task 4:  For part b, determine epsilon:


for line_index in range(puzzle_input.line_length()):
    epsilon_bit = puzzle_input.superlative_common_bit(number_index_list_epsilon, line_index, Superlative.least_common)

    # reduce number_index_list-s
    number_index_list_epsilon = puzzle_input.reduce_number_index_list(number_index_list_epsilon, line_index, epsilon_bit)

    # print('line_index: ', end='')
    # print(line_index, end=', ')


    # print('number_index_list_epsilon ', end='')
    # print(number_index_list_epsilon , end=', ')
    # print()

    if len(number_index_list_epsilon) < 2:
        break

# print(puzzle_input.get_line_integer(number_index_list_gamma[0]))

# print(puzzle_input.get_line_integer(number_index_list_epsilon[0]))

print('The solution to part b is ', end='')
print(
puzzle_input.get_line_integer(number_index_list_gamma[0]) *
puzzle_input.get_line_integer(number_index_list_epsilon[0])
)

