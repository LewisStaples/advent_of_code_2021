# adventOfCode 2021 day 23
# https://adventofcode.com/2021/day/23
#
# This version of the code for Day 23 will use classes and OOP

import sys

# Burrow will
class Burrow:
    def __init__(self, input_filename):

        # List of all amphipods (in alphabetical order, which is the desired order when the process will be completed)
        self.AMPHIPOD_LIST = ['A', 'B', 'C', 'D']
        # This dictionary has index = 'type of amphipod' and value is a list with energy and the hallway location that goes into its destination room.  These are immutable characteristics (it will be populated from the input file and it will not change afterward)
        self.AMPHIPOD_CHARACTERISTICS = {'A':[1], 'B':[10], 'C':[100], 'D':[1000]}

        # Open the input file
        print('Using input file: ', end='')
        print(input_filename)
        with open(input_filename) as f:
            line_length = None
            side_room_position = dict()
            # Pull in each line from the input file
            for row_num, in_string in enumerate(f):
                if row_num == 0:
                    # Require line to be all pound characters
                    line_length = len(in_string.rstrip())
                    if in_string.rstrip() != '#'*line_length:
                        sys.exit('Bad input!')
                    self.HALLWAY_LENGTH = line_length -2
                elif row_num == 1:            
                    # Require first and last character to be #
                    # if in_string.rstrip() != '#'+'.'*(line_length-2)+'#':
                    if in_string[0] != '#' or in_string.rstrip()[-1] != '#':
                        sys.exit('Bad input!')
                    
                    # # Initialize list with all hallway positions unoccupied
                    # burrow_state_list[0][0].extend([None]*(line_length-2))


                    for i,ch in enumerate(in_string):
                        if ch in self.AMPHIPOD_LIST:
                            # burrow_state_list[0][0][i-1] = ch
                            pass


                elif row_num == 2:
                    # find the letters and their side room position
                    # replace None with the named 2-tuple (described above)
                    for i,ch in enumerate(in_string):
                        if ch.isalpha() or ch == '.':
                            # This hallway position is a side room.  Add first amphipod
                            dest_char = self.AMPHIPOD_LIST[len(side_room_position)]
                            side_room_position[i] = dest_char
                            # burrow_state_list[0][0][i-1] = (dest_char,[ch]) if ch!='.' else (dest_char, [None])
                            # sideroom_indices.append(i-1)
                            
                else:
                    for i,ch in enumerate(in_string):
                        if ch.isalpha():
                            # burrow_state_list[0][0][i-1][1].append(ch)
                            pass

class HallwayRoom:
    pass

theBurrow = Burrow('input.txt')

