# adventOfCode 2021 day ??
# https://adventofcode.com/2021/day/??

class ALU:
    # This reads the ALU program from an input file
    def __init__(self):
        input_filename='input_sample1.txt'
        self.instructions = []
        this_instruction_list = None
        # Reading input from the input file
        with open(input_filename) as f:
            # Pull in each line from the input file
            for in_string in f:
                in_string = in_string.rstrip()
                if in_string[:3] == 'inp':
                    if this_instruction_list is not None:
                        self.instructions.append(this_instruction_list)
                    this_instruction_list = []
                this_instruction_list.append(in_string)
        self.instructions.append(this_instruction_list)

    def inp(self, param):
        print('inp ' + param)

    def mul(self, param):
        print('mul', end=' ')
        for par in param.split(' '):
            print(par, end = ' ')
        print()

    def eql(self, param):
        print('eql', end=' ')
        for par in param.split(' '):
            print(par, end = ' ')
        print()

    def execute(self):
        for instruction_list in self.instructions:
            for instruction in instruction_list:
                instruction_line = instruction.split(' ',1)
                # dummy = 123
                call_fxn = getattr(self, instruction_line[0]) #(instruction_line[1])
                call_fxn(instruction_line[1])
            #     print(instruction)
            # print('------------')

# Main program
the_alu = ALU()
the_alu.execute()

