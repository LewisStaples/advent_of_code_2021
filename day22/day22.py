# adventOfCode 2021 day 22
# https://adventofcode.com/2021/day/22

input_cube_reset_instructions = []

class CubeResetInstruction:
    # Load a line of input instructions into memory
    def __init__(self, str_input):
        self.operation, str_input = str_input.split(' ')
        self.ranges = {}
        for str_input in str_input.split(','):
            axis, str_input = str_input.split('=')
            self.ranges[axis] = str_input.split('..')


# reading input from the input file
input_filename='input_sample0.txt'
with open(input_filename) as f:
    # pull in each line from the input file
    for in_string in f:
        in_string = in_string.rstrip()
        input_cube_reset_instructions.append(CubeResetInstruction(in_string))

pass

