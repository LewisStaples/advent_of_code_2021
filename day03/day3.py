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

    # this is the number of lines in the original input
    def length(self):
        return len(self.puzzle_input)

    # this is the length of each line in the original input
    # (the length of line 0 is returned, but this is assumed to be constant)
    def line_length(self):
        return len(self.puzzle_input[0])

    # this returns a string with either most or least common bit
    def superlative_common_bit(self, number_index_list, bit_number, which_superlative):
        sum=0
        for index in number_index_list:
            sum += self.puzzle_input[index][bit_number]
        # most_common_bit = sum/(len(number_index_list))
        if sum/(len(number_index_list)) > 0.5:
            most_common_bit = 1
        else:
            most_common_bit = 0
        if which_superlative == Superlative.most_common:
            return str(most_common_bit)
        else:
            return str((most_common_bit+1)%2)

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

print(puzzle_input)
print()


# Task 2:  Solve part a

part_a_gamma_str = ''
part_a_epsilon_str = ''

# create list of indices in puzzle_input to be considered
# (for part a it is all indices in puzzle_input, but this will change in part b)
number_index_list = [x for x in range(puzzle_input.length())]

# print('number_index_list')
# print(number_index_list)
# print()

for line_index in range(puzzle_input.line_length()):
    part_a_gamma_str += puzzle_input.superlative_common_bit(number_index_list, line_index, Superlative.most_common)
    part_a_epsilon_str += puzzle_input.superlative_common_bit(number_index_list, line_index, Superlative.least_common)

# print(part_a_gamma_str)
# print(int(part_a_gamma_str,2))
# print()

# print(part_a_epsilon_str)
# print(int(part_a_epsilon_str,2))
# print()

print('The solution to part a is ', end='')
print(int(part_a_gamma_str,2)*int(part_a_epsilon_str,2))
