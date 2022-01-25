# adventOfCode 2021 day ??
# https://adventofcode.com/2021/day/??

class ALU:
    # This reads the ALU program from an input file
    def __init__(self):
        input_filename='input_sample0.txt'
        self.instructions = []
        # Reading input from the input file
        with open(input_filename) as f:
            # Pull in each line from the input file
            for in_string in f:
                in_string = in_string.rstrip()
                self.instructions.append(in_string)

    # This executes the ALU program against one value in a list of input numbers
    def execute(self, input_numbers, number_index):
        # Variables defined in the problem specification:
        w = x = y = z = 0
        #
        input_number = 0
        for i_ins in range(len(self.instructions)):
            print(self.instructions[i_ins])
        print('x = ', end='')
        print(x, end=', ')

# Main program
the_alu = ALU()
the_alu.execute(2)

