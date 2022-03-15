# adventOfCode 2021 day 23
# https://adventofcode.com/2021/day/23
#
# This version of the code for Day 23 will use classes and OOP

import sys

from day23_revised import AMPHIPOD_LIST

class SideRoom:
    pass

class HallwayRoom:
    pass

class BurrowState:
    # This code is only run once ... while reading from input.
    def __init__(self, hallway_init):
        self.hallway = []
        if isinstance(hallway_init, str):
            self.energy_total = 0
            # Remove # and newline characters
            hallway_init = hallway_init.rstrip()[1:-1]
            for ch in hallway_init:
                if ch == '.':
                    self.hallway.append(None)
                elif ch in Burrow.AMPHIPOD_LIST:
                    self.hallway.append(ch)
                else:
                    sys.exit('Bad input character: ' + ch)
            dummy = 123

        # This code is run multiple times ... whenever duplicating a BurrowState.
        elif isinstance(hallway_init, BurrowState):
            self.energy_total = hallway_init.energy_total
        
    def sideroom_init(self, sideroom_str):
        # Discover where the side rooms are
        #
        # Note that my input samples include a '.' in siderooms,
        # because I wanted to test an alternate scenario where
        # amphipods were already in the hallway.

        al_index = 0 # temp. variable:  index in Burrow.AMPHIPOD_LIST
        for i,ch in enumerate(sideroom_str):
            if ch.isalpha() or ch == '.':
                # This hallway position is a side room.  Add first amphipod
                al_index += 1
                self.hallway[i-1] = ([ch])
                Burrow.SIDEROOM_INDICES.append(i-1)

    def sideroom_append(self, sideroom_str):
                    # for i,ch in enumerate(in_string):
                    #     if ch.isalpha():
                    #         # burrow_state_list[0][0][i-1][1].append(ch)
                    #         pass
        pass

# Burrow will
class Burrow:
    # List of all amphipods (in alphabetical order, which is the desired order when the process will be completed)
    AMPHIPOD_LIST = ['A', 'B', 'C', 'D']
    # List of indices of siderooms
    SIDEROOM_INDICES = []

    # Create pair of dictionaries to lookup destination amphipod by sideroom index and vice versa.
    DEST_AMPH__SIDEROOM_INDEX = dict()
    SIDEROOM_INDEX__DEST_AMPH = dict()

    # This dictionary has index = 'type of amphipod' and value is the energy.
    AMPHIPOD_ENERGY = {'A':[1], 'B':[10], 'C':[100], 'D':[1000]}

    def __init__(self, input_filename):
        self.all_burrowStates = []

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
                    if in_string[0] != '#' or in_string.rstrip()[-1] != '#':
                        sys.exit('Bad input!')
                    
                    # Create the first BurrowState
                    self.all_burrowStates.append(BurrowState(in_string))

                elif row_num == 2:
                    self.all_burrowStates[0].sideroom_init(in_string)

                else:
                    self.all_burrowStates[0].sideroom_append(in_string)

        for i in range(len(Burrow.AMPHIPOD_LIST)):
            Burrow.DEST_AMPH__SIDEROOM_INDEX[AMPHIPOD_LIST[i]] = Burrow.SIDEROOM_INDICES[i]
            Burrow.SIDEROOM_INDEX__DEST_AMPH[Burrow.SIDEROOM_INDICES[i]] = AMPHIPOD_LIST[i]

class HallwayRoom:
    pass

theBurrow = Burrow('input_scenario2.txt')

