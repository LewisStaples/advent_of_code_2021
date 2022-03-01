# adventOfCode 2021 day 23
# https://adventofcode.com/2021/day/23

import sys

# List of all amphipods (in alphabetical order, which is the desired order when the process will be completed)
AMPHIPOD_LIST = ['A', 'B', 'C', 'D']

# This dictionary has index = 'type of amphipod' and value is a list with energy and the hallway location that goes into its destination room.  These are immutable characteristics (it will be populated from the input file and it will not change afterward)
AMPHIPOD_CHARACTERISTICS = {'A':[1], 'B':[10], 'C':[100], 'D':[1000]}

# This is a list where each element represents a location in the hallway.  The value elements can be:  
# 1. None (unoccupied)
# 2. A character (any element of AMPHIPOD_CHARACTERISTICS), indicating that an amphipod is in that location.
# 3. A named 2-tuple, indicating that that hallway location leads to a side room.  The first element is a character indicating which amphipod intends to end in that side room.  The second element is a list of characters, which lists all amphipods are in that side room.
amphipod_positions = []

input_filename='input.txt'
# Reading input from the input file
with open(input_filename) as f:
    line_length = None
    side_room_position = dict()
    # Pull in each line from the input file
    for row_num, in_string in enumerate(f):
        if row_num == 0:
            # Require line to be all pound characters
            line_length = len(in_string) - 1
            if in_string.rstrip() != '#'*line_length:
                sys.exit('Bad input!')
        elif row_num == 1:
            # Require line to have one pound at start and finish.  All interior characters must be periods
            if in_string.rstrip() != '#'+'.'*(line_length-2)+'#':
                sys.exit('Bad input!')
            
            # All hallway positions are initially unoccupied
            amphipod_positions = [None]*(line_length-2)
        elif row_num == 2:
            # find the letters and their side room position
            # replace None with the named 2-tuple (described above)
            for i,ch in enumerate(in_string):
                if ch.isalpha():
                    # This hallway position is a side room.  Add first amphipod
                    dest_char = AMPHIPOD_LIST[len(side_room_position)]
                    side_room_position[i] = dest_char
                    amphipod_positions[i-1] = (dest_char,[ch])
            dummy = 123
        else:
            for i,ch in enumerate(in_string):
                if ch.isalpha():
                    # amphipod_positions[i-1] = (side_room_position[i],[ch])
                    amphipod_positions[i-1][1].append(ch)
            dummy = 123
        dummy = 123

dummy = 123

