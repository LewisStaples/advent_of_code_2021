# adventOfCode 2021 day 23
# https://adventofcode.com/2021/day/23

# Strategy
# Come up with all permutations of orders for which amphipod is sent out and then back (develop a notation).  This uses the simplifying assumption that blockage in the hallway is a non-issue.  It will, however, account for blockage in the side rooms.
# From this come up with all permutations of spaces where each amphipod could be deposited (maybe some permuatations from the earlier tree could be eliminated)
# Calculate total energy associated with each permutation above
# The minimum total energy is the answer to (a)

import sys
import re

# This dictionary has index = 'type of amphipod' and value is a list with energy and the hallway location that goes into its destination room.  These are immutable characteristics (it will be populated from the input file and it will not change afterward)
AMPHIPOD_CHARACTERISTICS = {'A':[1], 'B':[10], 'C':[100], 'D':[1000]}

init_amphipod_positions = {}
init_amphipod_positions_rev = {}

# This has information about the open spaces in the hallway.
# These are immutable characteristics (it will be populated from the input file and it will not change afterward)
HALLWAY_CHARACTERISTICS = dict()

input_filename='input.txt'
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
                # If there is an amphipod in that location, note that initial position in init_amphipod_positions
                if this_char in ['A','B','C','D']:
                    this_char += '1' # first instance of this one seen
                    if this_char in init_amphipod_positions:
                        this_char = this_char[0] + '2' # second instance of this one seen
                    init_amphipod_positions[this_char] = [col_num, row_num]
                    init_amphipod_positions_rev[(col_num, row_num)] = this_char
            
# delete local variables used when inputting data from the file
del in_string
del row_num
del col_num
del this_char
del f
del input_filename

# Determine locations of the four side rooms:
side_rooms = []
for value in init_amphipod_positions.values():
    s_r = value[0]
    if s_r not in side_rooms:
        side_rooms.append(s_r)
# Label side rooms' destinations in order ... left to right, as in the spec.
for i, amph in enumerate(['A','B','C','D']):
    AMPHIPOD_CHARACTERISTICS[amph].append(side_rooms[i])
# del side_rooms
del i
del value
del amph
del s_r

# Consider all permutations of amphipod sequence
all_amph_sequences = set()
all_amph_sequences.add('')
complete_amph_sequences = set()

try:
    while len(all_amph_sequences) > 0:
        seq = all_amph_sequences.pop()

        if len(all_amph_sequences) < 2:
            dummy = 123

        # if len(seq) == 20:
        #     complete_amph_sequences.add(seq)
        #     continue

        # List out all possible moves available for state seq.
        poss_moves = []
        # Consider all possible moves where an amphipod leaves a side room
        # If this happens, it will be added to new_seq with an upper case letter
        for sr in side_rooms:
            init_amph_1 = init_amphipod_positions_rev[(sr,2)]
            init_amph_2 = init_amphipod_positions_rev[(sr,3)]
            if init_amph_1 not in seq:
                # If both 1 and 2 are at final destination, then skip them.
                if sr == AMPHIPOD_CHARACTERISTICS[init_amph_1[0]][1]:
                    if sr == AMPHIPOD_CHARACTERISTICS[init_amph_2[0]][1]:
                        continue # Skip this one.
                # The top amphipod could leave this side room
                poss_moves.append(init_amph_1) 
            elif init_amph_2 not in seq:
                # If 2 is not at final destination, then it could leave this side room.
                if sr != AMPHIPOD_CHARACTERISTICS[init_amph_2[0]][1]:
                    poss_moves.append(init_amph_2) # The bottom amphipod could leave this side room

        del init_amph_1
        del init_amph_2
        del sr

        # Also consider possible moves where an amphipod leaves the hallway 
        # If this happens, it will be added to new_seq with a lower case letter
        i = 0
        # Loop through all pairs of characters in seq
        while i < len(seq):
            # Ignore lower case character (it's a record of having left the hallway already)
            if seq[i].islower():
                i += 2
                continue

            next_poss_move = seq[i:i+2].lower()
            # Look for records elsewhere in seq of this having left the hallway already
            if next_poss_move in seq:
                i += 2
                continue
            poss_moves.append(next_poss_move)
            i += 2

        for move in poss_moves:
            new_seq = seq
            new_seq += move
            all_amph_sequences.add(new_seq)

        if len(poss_moves) == 0:
            complete_amph_sequences.add(seq)

except KeyboardInterrupt:
    dummy = 123

print('Permutation counts: ')
print(len(complete_amph_sequences))
print(len(all_amph_sequences))


least_total_energy = float('inf')
