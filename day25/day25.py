# adventOfCode 2021 day 25
# https://adventofcode.com/2021/day/25

import re
import copy

class SeaCucumber:
    def __init__(self):
        # # Python dictionaries about east-bound and south-bound herds
        # # Each will have the row as the index and the value will be a list of all column numbers within that row with that character
        self.sea_cucumbers = dict()
        self.herds = {'>': {'herd':'east_herd', 'motion_direction':(1,0)},
            'v' : {'herd':'south_herd', 'motion_direction':(0,1)}}

        self.herds_reverse = {}
        for symbol, name_dict in self.herds.items():
            self.herds_reverse[name_dict['herd']] = symbol

        # Variables to store the size of the region where the sea cucumbers are.
        self.ROW_TOTAL = None
        self.COLUMN_TOTAL = None

        # Reading input from the input file
        input_filename='input.txt'
        with open(input_filename) as f:
            # Pull in each line from the input file
            for row_number, in_string in enumerate(f):
                in_string = in_string.rstrip()

                self.sea_cucumbers[row_number] = {}
                for herd_symbol in self.herds:
                    self.sea_cucumbers[row_number][self.herds[herd_symbol]['herd']] = [m.start() for m in re.finditer(herd_symbol, in_string)]

                # Capture before the variables go out of scope.
                # (Unfortunately, both will be unnecessarily calculated each time through)
                self.COLUMN_TOTAL = len(in_string)
                self.ROW_TOTAL = row_number + 1

    # This function (likely to be removed shortly) determines if a given location is blocked by a sea cucumber that is arleady there.
    def blocked(self, location):
        for herd in self.sea_cucumbers[location[1]]:
            for index_num in self.sea_cucumbers[location[1]][herd]:
                if index_num == location[0]:
                    return True
        return False

    # This function advances a single herd of sea cucumbers
    def advance_single_herd(self, herd_symbol):
        change_count = 0 # value to return
        sea_cucumbers_new = copy.deepcopy(self.sea_cucumbers)
        
        # Loop through all rows of sea cucumbers.
        for row_num in self.sea_cucumbers:
            herd = self.herds[herd_symbol]['herd']
            # Loop through all sea cucumbers in this row.
            for index in self.sea_cucumbers[row_num][herd]:
                # calc new value
                new_location = (
                    (index + self.herds[herd_symbol]['motion_direction'][0]) % self.COLUMN_TOTAL ,
                    (row_num + self.herds[herd_symbol]['motion_direction'][1] ) % self.ROW_TOTAL
                )

                # NEXT CHANGE .... don't loop through the entire row's seacucumbers for every move into this row
                # Instead determine them for all rows at the outset.

                # if new_location is blocked, then continue (retain the old location)
                if self.blocked(new_location):
                    continue
                # since new value isn't blocked, remove old value from and add new value to sea_cucumbers_new
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
    # This assumes that no location has both a south-bound and an east-bound sea cucumber in that location
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
