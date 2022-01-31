# adventOfCode 2021 day 25
# https://adventofcode.com/2021/day/25

import re
import copy

class SeaCucumber:
    def __init__(self):
        # This data structure will store information about all sea cucumbers.
        # The outer dictionary has row numbers as its indices and the values 
        # are inner dictionaries.  The inner dictionary has the names of the 
        # two herds as the indices and the values are lists.  These lists 
        # list the column numbers of all sea cucumbers in that herd in that 
        # row.
        self.sea_cucumbers = dict()

        # This data structure lists important unchangeable characteristics 
        # of each herd.
        self.HERDS = {'>': {'herd':'east_herd', 'motion_direction':(1,0)},
            'v' : {'herd':'south_herd', 'motion_direction':(0,1)}}

        # This dictionary is used in the display method, which allows for 
        # the herd name to be used to get the symbol.
        self.herds_reverse = {}
        for symbol, name_dict in self.HERDS.items():
            self.herds_reverse[name_dict['herd']] = symbol

        # Variables to store the size of the region where 
        # the sea cucumbers are.
        self.ROW_TOTAL = None
        self.COLUMN_TOTAL = None

        # Reading input from the input file
        input_filename='input.txt'
        with open(input_filename) as f:
            # Pull in each line from the input file
            for row_number, in_string in enumerate(f):
                in_string = in_string.rstrip()

                self.sea_cucumbers[row_number] = {}
                for herd_symbol in self.HERDS:
                    self.sea_cucumbers[row_number][self.HERDS[herd_symbol] \
                    ['herd']] = [m.start() for m in re.finditer(herd_symbol, \
                        in_string)]

                # Capture before the variables go out of scope.
                # (Unfortunately, both will be unnecessarily 
                # calculated each time through)
                self.COLUMN_TOTAL = len(in_string)
                self.ROW_TOTAL = row_number + 1

    # Generate a lookup table listing all blocked locations.
    def get_all_blocked_locations(self):
        ret_val = {}
        for row_num in self.sea_cucumbers:
            ret_val[row_num] = set()
            for herd in self.sea_cucumbers[row_num]:
                for col_num in self.sea_cucumbers[row_num][herd]:
                    ret_val[row_num].add(col_num)
        return ret_val

    # This function advances a single herd of sea cucumbers
    def advance_single_herd(self, herd_symbol):
        # value to return
        change_count = 0 
        sea_cucumbers_new = copy.deepcopy(self.sea_cucumbers)
        
        # Create a data structure for looking up all blocked locations
        blocked_sc = self.get_all_blocked_locations()

        # Loop through all rows of sea cucumbers.
        for row_num in self.sea_cucumbers:
            herd = self.HERDS[herd_symbol]['herd']

            # Loop through all sea cucumbers in this row.
            for index in self.sea_cucumbers[row_num][herd]:
                # calc new value
                new_location = ( (index + self.HERDS[herd_symbol] \
                    ['motion_direction'][0]) % self.COLUMN_TOTAL , \
                        (row_num + self.HERDS[herd_symbol] \
                            ['motion_direction'][1] ) % \
                                 self.ROW_TOTAL )

                # If the intended destination of the sea cucumber is blocked,
                # then disallow the move.
                if new_location[0] in blocked_sc[new_location[1]]:
                    # Since this move is disallowed, proceed to the next 
                    # sea cucumber in the loop.
                    continue

                # since new value isn't blocked, remove old value from 
                # and add new value to sea_cucumbers_new
                sea_cucumbers_new[row_num][herd].remove(index)
                sea_cucumbers_new[new_location[1]][herd].append(new_location[0])
                change_count += 1
        self.sea_cucumbers = sea_cucumbers_new
        return change_count
        
    # This advances the herd by one step
    # It returns the number of sea cucumbers that moved in that step.
    # Part a wants to know if the value is zero or non-zero.
    # Part b could perhaps want more detailed information.
    def advance_one_step(self):
        num_sea_cucu_advanced = 0
        # Advance east-bound herd
        num_sea_cucu_advanced += self.advance_single_herd('>')
        # Advance south-bound herd
        num_sea_cucu_advanced += self.advance_single_herd('v')
        return num_sea_cucu_advanced

    # This prints out the status of both herds.
    # This assumes that no location has both a south-bound and an 
    # east-bound sea cucumber in that location.
    # This is for testing only.  (To compare to the given example)
    def display(self):
        for row_number in self.sea_cucumbers:
            # line_to_print is a list to allow for character substitution
            line_to_print = ['.'] * self.COLUMN_TOTAL
            for herd in self.sea_cucumbers[row_number]:
                symbol = self.herds_reverse[herd]
                
                for index_num in self.sea_cucumbers[row_number][herd]:
                    line_to_print[index_num] = symbol
            print ("".join(line_to_print))
        print()
        print()

move_count = float('inf')
seaCucumber = SeaCucumber()

# print('Initial State:')
total_steps=0
while move_count > 0:
    total_steps += 1
    # seaCucumber.display()
    move_count = seaCucumber.advance_one_step()
    # print('After step # ', end='')
    # print(total_steps, end=':\n')

# print('The above is also the Final State')
print('The answer is ', end='')
print(total_steps, end='')
print(' steps')
