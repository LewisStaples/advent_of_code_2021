# adventOfCode 2021 day 25
# https://adventofcode.com/2021/day/25

import re
import copy

class SeaCucumber:
    def __init__(self):
        # # Python dictionaries about east-bound and south-bound herds
        # # Each will have the row as the index and the value will be a list of all column numbers within that row with that character
        # self.east_herd = dict()
        # self.south_herd = dict()

        self.sea_cucumbers = dict()
        self.herds = {'>': {'herd':'east_herd', 'motion_direction':(1,0)},
            'v' : {'herd':'south_herd', 'motion_direction':(0,1)}}

        self.ROW_TOTAL = None
        self.COLUMN_TOTAL = None

        # Reading input from the input file
        input_filename='input_sampleN.txt'
        with open(input_filename) as f:
            # Pull in each line from the input file
            for row_number, in_string in enumerate(f):
                in_string = in_string.rstrip()
                # print(in_string)

                # self.east_herd[row_number] = [m.start() for m in re.finditer('>', in_string)]
                # self.south_herd[row_number] = [m.start() for m in re.finditer('v', in_string)]
                self.sea_cucumbers[row_number] = {}
                for herd_symbol in self.herds:
                    self.sea_cucumbers[row_number][self.herds[herd_symbol]['herd']] = [m.start() for m in re.finditer(herd_symbol, in_string)]

                # Capture before the variable goes out of scope.
                # (Unfortunately, it will be unnecessarily calculated each time through)
                self.COLUMN_TOTAL = len(in_string)
                self.ROW_TOTAL = row_number + 1

    def blocked(self, location):
        for row_number in self.sea_cucumbers:
            if location[1] != row_number:
                continue
            for herd in self.sea_cucumbers[row_number]:
                for index_num in self.sea_cucumbers[row_number][herd]:
                    if index_num == location[0]:
                        return True
        return False

    def advance_single_herd(self, herd_symbol):
        # herd_old = None
        # all_herds = [self.east_herd, self.south_herd]
        # if herd_symbol == '>':
        #     herd_old = self.east_herd
        # elif herd_symbol == 'v':
        #     herd_old = self.south_herd
        
        # for row_num,indices_old in herd_old.items():
        #     pass

        # return 42

        change_count = 0 # value to return
        # sea_cucumbers_old = self.sea_cucumbers
        # sea_cucumbers_new = copy.deepcopy(sea_cucumbers_old)
        for row_num in self.sea_cucumbers:
            sea_cucumbers_old = self.sea_cucumbers
            sea_cucumbers_new = copy.deepcopy(sea_cucumbers_old)
            for herd in sea_cucumbers_old[row_num]:
                if self.herds[herd_symbol]['herd'] != herd:
                    continue
                for index in sea_cucumbers_old[row_num][herd]:
                    pass
                    # calc new value
                    new_location = (
                        (index + self.herds[herd_symbol]['motion_direction'][0]) % self.COLUMN_TOTAL ,
                        (row_num + self.herds[herd_symbol]['motion_direction'][1] ) % self.ROW_TOTAL
                    )
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
        # for row_number in self.east_herd.keys():
        #     for col_number in range(self.COLUMN_TOTAL):
        #         if col_number in self.east_herd[row_number]:
        #             print('>', end='')
        #         elif col_number in self.south_herd[row_number]:
        #             print('v', end='')
        #         else:
        #             print('.', end='')
            # print()
        
        herds_reverse = {}
        for symbol, name_dict in self.herds.items():
            herds_reverse[name_dict['herd']] = symbol
        
        for row_number in self.sea_cucumbers:
            line_to_print = ['.'] * self.COLUMN_TOTAL
            for herd in self.sea_cucumbers[row_number]:
                pass
                symbol = herds_reverse[herd]
                # Note that below is a list to allow for character substitution
                
                for index_num in self.sea_cucumbers[row_number][herd]:
                    line_to_print[index_num] = symbol
            print ("".join(line_to_print))
        print()
        print()

move_count = float('inf')
seaCucumber = SeaCucumber()
# while move_count > 0:
for i in range(10):
    print('After step # ', end='')
    print(i, end=':\n')
    seaCucumber.display()
    move_count = seaCucumber.advance_one_step()
seaCucumber.display()
