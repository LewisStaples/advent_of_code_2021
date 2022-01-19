# adventOfCode 2021 day 23
# https://adventofcode.com/2021/day/23

# Strategy
# Come up with all permutations of orders for which amphipod is sent out and then back (develop a notation).  This uses the simpliying assumption that blockage in the hallway is a non-issue.
# From this come up with all permutations of spaces where each amphipod could be deposited (maybe some permuatations from the earlier tree could be eliminated)
# Calculate total energy associated with each permutation above
# The minimum total energy is the answer to (a)

import sys
import re

# This dictionary has index = 'type of amphipod' and value is a list with energy and the hallway location that goes into its destination room.  These are immutable characteristics (it will be populated from the input file and it will not change afterward)
AMPHIPOD_CHARACTERISTICS = {'A':[1], 'B':[10], 'C':[100], 'D':[1000]}

amphipod_positions = {}
amphipod_positions_rev = {}

# This has information about the open spaces in the hallway.
# These are immutable characteristics (it will be populated from the input file and it will not change afterward)
HALLWAY_CHARACTERISTICS = dict()

input_filename='input_sample0.txt'
# Reading input from the input file
with open(input_filename) as f:
    # Pull in each line from the input file
    for row_num, in_string in enumerate(f):
        in_string = in_string.rstrip()

        # Search for row of periods (the hallway)
        if in_string.count('.') > 0:
            # Crash program if the periods aren't a continuous hallway
            if in_string.count('.') != in_string.rfind('.') - in_string.find('.') + 1:
                sys.exit('FAILURE!  The hallway is supposed to be in a continuous line of open spaces')
            if len(HALLWAY_CHARACTERISTICS)>0:
                sys.exit('FAILURE!  There should only be one row of open spaces in the hallway')
            if len(re.findall('[A-D]', in_string)) > 0:
                sys.exit('FAILURE!  No amphipods should be initially in the hallway')

            # Store characteristics involving the hallway
            HALLWAY_CHARACTERISTICS['init_index'] = in_string.find('.')
            HALLWAY_CHARACTERISTICS['final_index'] = in_string.rfind('.')
            HALLWAY_CHARACTERISTICS['row_num'] = row_num

            # For the time being, this program will require that the hallway be at row_num 1
            if row_num != 1:
                sys.exit('FAILURE!  The hallway must be in the second line of the input!')
        
        #  If there is at least one amphipod in this row of input....
        if len(re.findall('[A-D]', in_string)) > 0:

            # For the time being, this program will require that all amphipods initiial positions will be either 2 or 3:
            if row_num not in [2,3]:
                sys.exit('FAILURE!  All amphipods must start at rows 2 or 3!')

            # Iterate through each character in the row of input
            for col_num, this_char in enumerate(in_string):
                # If there is an amphipod in that location, note that initial position in amphipod_positions
                if this_char in ['A','B','C','D']:
                    this_char += '1' # first instance of this one seen
                    if this_char in amphipod_positions:
                        this_char = this_char[0] + '2' # second instance of this one seen
                    amphipod_positions[this_char] = [col_num, row_num]
                    amphipod_positions_rev[(col_num, row_num)] = this_char
            
# delete local variables used when inputting data from the file
del in_string
del row_num
del col_num
del this_char

# Determine locations of the four side rooms:
side_rooms = []
for value in amphipod_positions.values():
    s_r = value[0]
    if s_r not in side_rooms:
        side_rooms.append(s_r)
side_rooms.sort(reverse=True)
# Label side rooms' destinations in order ... left to right, as in the spec.
for amph in ['A','B','C','D']:
    AMPHIPOD_CHARACTERISTICS[amph].append(side_rooms.pop())
del side_rooms
del value
del amph

# Consider all permutations of amphipod sequence
all_amph_sequences_working = ['']
all_amph_sequences_complete = []
# 
# for seq in all_amph_sequences_working:
while len(all_amph_sequences_working) > 0:
    seq = all_amph_sequences_working.pop()
    for amph_key, amph_value in amphipod_positions.items():
        new_seq = seq
        # Skip it if its already in the sequence
        if amph_key in new_seq:
            continue
        # If amph is blocked:
        if amph_value[1] == 3:
            if amphipod_positions_rev[(amph_value[0],3)] not in new_seq:
                continue # Skip it (because it's blocked)
        new_seq += amph_key
        if len(new_seq) < 10:
            all_amph_sequences_working.append(new_seq)
        else:
            all_amph_sequences_complete.append(new_seq)

dummy = 123


    