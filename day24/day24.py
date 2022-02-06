# adventOfCode 2021 day ??
# https://adventofcode.com/2021/day/??

class ALU:
    # This reads the ALU program from an input file
    def __init__(self):
        input_filename='input.txt'
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

    # The specifications indicate that b could either be a value (such as 0) or a variable (such as w).
    def get_b_value(self, b_value):
        # Assume that w,x,y,z are the only variables that it could be
        if b_value in ['w', 'x', 'y', 'z']:
            # return the value of the variable
            return getattr(self, b_value)

        # return the value itself, since it is not a variable.
        return b_value

    def inp(self, param):
        var_str = param
        setattr(self, var_str, 'input_' + str(self.input_index))
        # # Printing (for testing)
        # print('inp ' + param)

    def add(self, param):
        var_str, add_str = param.split(' ')        
        var = getattr(self, var_str)
        add_value = self.get_b_value(add_str)
        # Make changes only if adding something other than zero
        # (otherwise, keep var as it is)
        if add_value != '0':
            if var != '0':
                # Add var and add_value together, as long as they're both non-zero
                var = '(' + var + ' + ' + add_value + ')'
            else:
                # If var is zero, replace it with add_value
                var = add_value
            setattr(self, var_str, var)

        # # Printing (for testing)
        # print('add', end=' ')
        # for par in param.split(' '):
        #     print(par, end = ' ')
        # print()

    def mul(self, param):
        var_str, mult_str = param.split(' ')        
        var = getattr(self, var_str)
        mult_value = self.get_b_value(mult_str)

        # If multiplying by zero, discard everything there
        if mult_value == '0':
            var = '0'
        else:
            var = '(' + var + ')*' + mult_value

        setattr(self, var_str, var)

        # # Printing (for testing)
        # print('mul', end=' ')
        # for par in param.split(' '):
        #     print(par, end = ' ')
        # print()



    def div(self, param):
        var_str, div_str = param.split(' ')        
        var = getattr(self, var_str)
        div_value = self.get_b_value(div_str)

        # Make changes only if dividing by something other than one
        if div_value != '1':
            var = '(' + var + ')/' + div_value

        setattr(self, var_str, var)

        #  # Printing (for testing)
        # print('div', end=' ')
        # for par in param.split(' '):
        #     print(par, end = ' ')
        # print()

    def mod(self, param):
        var_str, mod_str = param.split(' ')        
        var = getattr(self, var_str)
        mod_value = self.get_b_value(mod_str)

        # Make changes only if taking modulus by something other than one
        if mod_value != '1':
            var = '(' + var + ')%' + mod_value

        setattr(self, var_str, var)

        #  # Printing (for testing)
        # print('mod', end=' ')
        # for par in param.split(' '):
        #     print(par, end = ' ')
        # print()

    def eql(self, param):
        var_str, comp_str = param.split(' ')        
        var = getattr(self, var_str)
        comp_value = self.get_b_value(comp_str)
        var = '(0 unless (' + var + ') equals (' + comp_value + '))'

        setattr(self, var_str, var)

        # # Printing (for testing)
        # print('eql', end=' ')
        # for par in param.split(' '):
        #     print(par, end = ' ')
        # print()

    def elim_unneeded_parens(self):
        # Remove parentheses pairs that don't contain anything inside requiring a parenthesis
        while True:
            count_parens_removed = 0
            i_open = -1
            while True:
                i_open += 1
                # 1. find next open parenthesis
                i_open = self.z.find('(', i_open)
                if i_open == -1:
                    break # There are no more open parentheses.

                # 2. look to see if next operator is close parenthesis or any member of '(+%ue'
                # (The u and e are there, because it is they start "unless" and "equals")
                i_next = float('inf')
                for ch in '(+s':
                    possible_next = self.z.find(ch, i_open + 1)
                    if possible_next != -1:
                        i_next = min(i_next, possible_next)
                i_close = self.z.find(')', i_open + 1)
                if i_close >= i_next:
                    continue
                count_parens_removed += 1
                
                # 3. If the next is a close parenthesis, then remove both parentheses, since they are superflous
                dummy = 123
                self.z = self.z[:i_open] + self.z[i_open+1:i_close] + self.z[i_close+1:]
                dummy = 1235
            if count_parens_removed == 0:
                break

        # Detect superfluous pairs of parentheses
        while True:
            count_parens_removed = 0
            i_open2 = -1
            while True:
                i_open2 += 1
                # 1. Find a pair of open parenthesis
                i_open2 = self.z.find('((', i_open2)
                if i_open2 == -1:
                    break # There are no more pairs of open parentheses.

                # 2. Find the close parenthesis that matches the second in the pair
                # i_close = self.z.find(')', i_open2)
                i_close = i_open2 + 1
                paren_level = 2
                while True:
                    i_close += 1
                    if self.z[i_close] == '(':
                        paren_level += 1
                    if self.z[i_close] == ')':
                        paren_level -= 1
                    if paren_level == 1:
                        break

                # 3. If the character after that close parenthesis is another close parenthesis
                if self.z[i_close + 1] == ')':
                    # Remove a pair of parentheses, since they are superflous
                    dummy = 123
                    count_parens_removed += 1
                    self.z = self.z[:i_open2+1] + self.z[i_open2+2:i_close] + self.z[i_close+1:]
                    dummy = 1235
                break
            if count_parens_removed == 0:
                break

    def execute(self):
        dummy = 123
        for self.input_index in range(len(self.instructions)-1,-1,-1):
            self.w='w_init'
            self.x='x_init'
            self.y='y_init'
            self.z='z_init'
            for instruction in self.instructions[self.input_index]:
                instruction_line = instruction.split(' ',1)
                call_fxn = getattr(self, instruction_line[0])
                call_fxn(instruction_line[1])

                dummy = 123
            
            print('At end of part ', end='')
            print(self.input_index, end=' ')
            print(' of the code: ')
            print()

            # Only z is printed, because w,x,y are not needed.
            # w remains the input value.  x and y never impact z

            print('z = ', end='')
            print(self.z)
            print()
            self.elim_unneeded_parens()
            print('z = ', end='')
            print(self.z)
            print()
            print()
            dummy = 123


# Main program
the_alu = ALU()
the_alu.execute()

