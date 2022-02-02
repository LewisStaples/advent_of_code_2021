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

    # def add(self, param):
    #     print('add', end=' ')
    #     for par in param.split(' '):
    #         print(par, end = ' ')
    #     print()

    def mul(self, param):
        var_str, mult_str = param.split(' ')        
        var = getattr(self, var_str)

        # If multiplying by zero, discard everything there
        if mult_str == '0':
            var = '0'
        else:
            var = '(' + var + ')*' + mult_str

        setattr(self, var_str, var)

        # Printing (for testing)
        print('mul', end=' ')
        for par in param.split(' '):
            print(par, end = ' ')
        print()



    # def div(self, param):
    #     print('div', end=' ')
    #     for par in param.split(' '):
    #         print(par, end = ' ')
    #     print()

    # def mod(self, param):
    #     print('mod', end=' ')
    #     for par in param.split(' '):
    #         print(par, end = ' ')
    #     print()

    def eql(self, param):
        var_str, comp_str = param.split(' ')        
        var = getattr(self, var_str)

        # # If multiplying by zero, discard everything there
        # if mult_str == '0':
        #     var = '0'
        # else:
        #     var = '(' + var + ')*' + mult_str

        var = '0 unless ' + var + ' equals ' + comp_str

        setattr(self, var_str, var)

        # Printing (for testing)
        print('eql', end=' ')
        for par in param.split(' '):
            print(par, end = ' ')
        print()

    def execute(self):
        dummy = 123
        for self.input_index in range(len(self.instructions)-1,-1,-1):
            self.w='w'
            self.x='x'
            self.y='y'
            self.z='z'
            for instruction in self.instructions[self.input_index]:
                instruction_line = instruction.split(' ',1)
                call_fxn = getattr(self, instruction_line[0])
                call_fxn(instruction_line[1])

                dummy = 123

# Main program
the_alu = ALU()
the_alu.execute()

