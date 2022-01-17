# adventOfCode 2021 day 23
# https://adventofcode.com/2021/day/23

# Strategy
# Come up with all permutations of orders for which amphipod is sent out and then back (develop a notation).  This uses the simpliying assumption that there can't be any blockage in the hallway.
# From this come up with all permutations of spaces where each amphipod could be deposited (maybe some permuatations from the earlier tree could be eliminated)
# Calculate total energy associated with each permutation above
# The minimum total energy is the answer to (a)

import sys
import re

# This dictionary has index = 'type of amphipod' and value is a list with energy and the hallway location that goes into its destination room.  These are immutable characteristics
amphipod_characteristics = {'A':[1], 'B':[10], 'C':[100], 'D':[1000]}

amphipod_positions = {}

# This has information about the open spaces in the hallway
hallway_characteristics = dict()

input_filename='input_sample0.txt'
# Reading input from the input file
with open(input_filename) as f:
    # Pull in each line from the input file
    for row_num, in_string in enumerate(f):
        in_string = in_string.rstrip()
        # print(in_string)

        # Search for row of periods (the hallway)
        if in_string.count('.') > 0:
            # Crash program if the periods aren't a continuous hallway
            if in_string.count('.') != in_string.rfind('.') - in_string.find('.') + 1:
                sys.exit('FAILURE!  The hallway is supposed to be in a continuous line of open spaces')
            if len(hallway_characteristics)>0:
                sys.exit('FAILURE!  There should only be one row of open spaces in the hallway')
            if len(re.findall('[A-D]', in_string)) > 0:
                sys.exit('FAILURE!  No amphipods should be initially in the hallway')

            # Store characteristics involving the hallway
            hallway_characteristics['init_index'] = in_string.find('.')
            hallway_characteristics['final_index'] = in_string.rfind('.')
            hallway_characteristics['row_num'] = row_num
        
        #  If there is at least one amphipod in this row of input....
        if len(re.findall('[A-D]', in_string)) > 0:
            # Iterate through each character in the row of input
            for col_num, this_char in enumerate(in_string):
                # If there is an amphipod in that location, note that initial position in amphipod_positions
                if this_char in ['A','B','C','D']:
                    this_char += '1' # first instance of this one seen
                    if this_char in amphipod_positions:
                        this_char = this_char[0] + '2' # second instance of this one seen
                    amphipod_positions[this_char] = [col_num, row_num]
            
# delete local variables used when inputting data from the file
del in_string
del row_num
del col_num
del this_char


