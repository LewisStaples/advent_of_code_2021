# adventOfCode 2021 day 24
# https://adventofcode.com/2021/day/24

import re

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

    # This is for the input instruction.
    def inp(self, param):
        var_str = param
        setattr(self, var_str, 'input_' + str(self.input_index))
        # # Printing (for testing)
        # print('inp ' + param)

    # This is for the add instruction.
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

    # This is for the multiply instruction.
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


    # This is for the divide instruction.
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

    # This is for the modulus instruction.
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

    # This is for the equal instruction.
    # (Note that the output doesn't capture that the value is 1 if unequal)
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

    # This resolves any unless statements.
    # The unless statements to parse are always   (something0 unless something1 equals something2)
    def process_unless_statements(self):
        # Keeping looping through
        # while True:

        # look for an unless/equals statement 
        i_unless = self.z.find('unless')

        # if none found, end this function
        # if i_unless == -1:
        #   return

        i_equals = None
        # loop until an inner unless/equals is found
        # (caveat:  This does not solve the general problem where a sub-unless command could be anywhere in the unless statement. It only solves for sub-unless between the parent's 'unless' and 'equals' keywords)
        while True:
            # Look to see what comes next: i_equals or i_unless
            i_equals = self.z.find('equals', i_unless)
            i_unless_next = self.z.find('unless', i_unless+1)
            if i_unless_next == -1: # if there are no additional unless-es
                break
            if i_equals < i_unless_next: # if the next equals comes before the unless
                break
            i_unless = i_unless_next

            # if found, look for any sub-unless/equals statements
            # keep moving one element to the left

        # move to the left
        # identify the end of the unless/equals statement
        l_paren_info = {'level': 0, 'index': i_unless}
        r_paren_info = {'level': 0, 'index': i_equals}
        while l_paren_info['level'] < 1:
            l_paren_info['index'] -= 1
            if self.z[l_paren_info['index']] == '(':
                l_paren_info['level'] += 1
            elif self.z[l_paren_info['index']] == ')':
                l_paren_info['level'] -= 1
            
        # move to the right, with logic similar to above, 
        # identify the end of the unless/equals statement
        while r_paren_info['level'] > -1:
            r_paren_info['index'] += 1
            if self.z[r_paren_info['index']] == '(':
                r_paren_info['level'] += 1
            elif self.z[r_paren_info['index']] == ')':
                r_paren_info['level'] -= 1


            
        # resolve the lowest level unless/equals statement (then continue looping)
        # --- automate the logic in notes.txt
        dummy = 123
        print(self.z)
        i_equals = self.z.find('equals',i_unless)
        statement_a = self.z[l_paren_info['index']+1:i_unless-1]
        statement_b = self.z[i_unless+8:i_equals-2]
        statement_c = self.z[i_equals+7:r_paren_info['index']]

        # if statement_c is an input
        if re.match('input_\d+$', statement_c):
            # if statement b has [any_numerator % any_denominator + anything_greater than nine]
            # Try detecting any of the below, perhaps using regular expressions
            # 'z_', digits,'%26 + ', followed by two digits # This cannot be a single digit number
            if re.match('z([\d]|[_init])+%26 \+ \d\d', statement_b):
                # then statement_b can never equal statement_c, therefore the answer is 0
                self.z = self.z[:l_paren_info['index']] + '0' + self.z[r_paren_info['index']+1:]
                dummy = 123
            # Either one below could be a single digit number
            # 'z_', digits,'%26 + ', followed by one digit
            # 'z_', digits,'%26 + -', followed by one or two digits
            elif re.match('z\d+%26 \+ -?\d{1,2}', statement_b):
                # assumption that that statement_b equals statement_c (to help get the ending value of z back down to zero)
                self.z = self.z[:l_paren_info['index']] + '1' + self.z[r_paren_info['index']+1:]
                dummy = 123

        print(self.z)
        dummy = 123


        # break

        # Output to remind me to finish this
        print('---------------------------------------')
        print('process_unless_statements')
        print('NOT  YET  WORKING !!!!!!!!!!!!')
        print('---------------------------------------')


    # This eliminates unneeded parentheses.
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

                # 2. look to see if next operator is close parenthesis or any member of '(+s'
                # (The s is there, because this letter is in both "unless" and "equals" and its not in "input")
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

        # Remove duplicate pairs of parentheses.
        # Example:  ((x+1/2)) would become (x+1/2).
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
        # for self.input_index in range(len(self.instructions)-1,-1,-1): # going through in reverse order

        self.w='w_init'
        self.x='x_init'
        self.y='y_init'
        self.z='z_init'

        for self.input_index in range(len(self.instructions)):
            # self.w='w_init'
            # self.x='x_init'
            # self.y='y_init'
            # self.z='z_init'
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
            self.elim_unneeded_parens()
            self.process_unless_statements()
            self.elim_unneeded_parens()

            # print('z', end='')
            # print(str(self.input_index), end='')
            # print(' = ', end='')
            print(self.z)
            print()
            print()

            # Reset four variables for the next round
            self.w='w' + str(self.input_index)
            self.x='x' + str(self.input_index)
            self.y='y' + str(self.input_index)
            self.z='z' + str(self.input_index)

# Main program
the_alu = ALU()
the_alu.execute()

