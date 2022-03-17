# adventOfCode 2021 day 23
# https://adventofcode.com/2021/day/23
#
# This version of the code for Day 23 will use classes and OOP
from enum import Enum
import sys
import copy

class Location(Enum):
    ORIGIN = 1
    DEST = 2

class SideRoom:
    def __init__(self, amphipod_init):
        self.amphipod_list = [amphipod_init]

    def append(self, amphipod_next):
        self.amphipod_list.append(amphipod_next)

    def show(self, location, amphipod_final_dest):
        if location == Location.ORIGIN:
            for i, amphipod in enumerate(self.amphipod_list):
                if amphipod in Burrow.AMPHIPOD_LIST:
                    # Index of a slot with an amphipod, which can be sent elsewhere
                    return i
        elif location == Location.DEST:
            for i in range(self.amphipod_list, -1, -1):
                if self.amphipod_list[i] is None:
                    # Index of an empty slot.  An amphipod could be sent here.
                    return i
        return None
        
    def pop(self):
        for amphipod in self.amphipod_list:
            for i, amphipod in enumerate(Burrow.AMPHIPOD_LIST):
                if amphipod in Burrow.AMPHIPOD_LIST:
                    self.amphipod_list[i] = None
                    return amphipod
        return None

class BurrowState:
    def __init__(self, hallway_init):
        self.hallway = []

        #  This reads from input.  It is only run once.
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
            print('Still need to copy/test self.hallway and all siderooms !!!')
            self.hallway = copy.deepcopy(hallway_init.hallway)
        
    def sideroom_init(self, sideroom_str):
        # Process line of input with start of the siderooms.
        # Label each sideroom by which amphipods seek that as their destination.
        #
        # Note that my input samples include a '.' in siderooms,
        # because I wanted to test an alternate scenario where
        # amphipods were already in the hallway.

        i_sideroom = 0
        for i,ch in enumerate(sideroom_str):
            if ch.isalpha() or ch == '.':
                # This hallway position is a side room.  Add first amphipod
                self.hallway[i-1] = SideRoom(ch)
                Burrow.SIDEROOM_INDICES.append(i-1)

                Burrow.DEST_AMPH__SIDEROOM_INDEX[i-1] = Burrow.AMPHIPOD_LIST[i_sideroom]
                i_sideroom += 1
        dummy = 123

    def sideroom_append(self, sideroom_str):
        has_no_amphipods = True
        for ch in Burrow.AMPHIPOD_LIST:
            if ch in sideroom_str:
                has_no_amphipods = False
        if has_no_amphipods:
            return
        for i in Burrow.SIDEROOM_INDICES:
            self.hallway[i].append(sideroom_str[i+1])

# Class Burrow will contain information that always applies to the burrow, whereas clas BurrowState has information that captures the momentary state of a burrow.

class Burrow:
    # List of all amphipods (in alphabetical order, which is the desired order when the process will be completed)
    AMPHIPOD_LIST = ['A', 'B', 'C', 'D']
    # List of indices of siderooms
    SIDEROOM_INDICES = []

    # Create dictionary to lookup destination amphipod by sideroom's hallway index 
    DEST_AMPH__SIDEROOM_INDEX = dict()

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

    def next_move(self):
        burrowState = self.all_burrowStates[0]
        # Send an amphipod from origin sideroom directly to destination sideroom

        # Send an amphipod from the hallway directly to destination sideroom

        # Send an amphipod from a sideroom to a hallway location

        for tran_origin in self.list_siderooms(burrowState, Location.ORIGIN):
            for tran_dest in self.get_hallways(burrowState, Location.DEST):
                next_state = self.make_move(burrowState, tran_origin, tran_dest)
                if next_state:
                    self.all_burrowStates.append(next_state)

    def list_siderooms(self, burrowState, location):
        ret_val = []
        for sideroom_index in Burrow.SIDEROOM_INDICES:
            new_sr = burrowState.hallway[sideroom_index].show(location, Burrow.DEST_AMPH__SIDEROOM_INDEX[sideroom_index])
            if new_sr is not None: # sideroom space has an amphipod
                ret_val.append((sideroom_index, new_sr))
        dummy = 123
        return ret_val

    def get_hallways(self, burrowState, location):
        ret_val = []
        for hallway_index, hallway_space in enumerate(burrowState.hallway):
            if location == Location.DEST:
                if hallway_space is None:
                    ret_val.append(hallway_index)
        return ret_val

    def make_move(self, burrowState, tran_origin, tran_dest):
        energy_total = burrowState.energy_total

        # If origin is a sideroom, calculate energy use and look out for ostacles

        dummy = 123

theBurrow = Burrow('input_scenario1.txt')

# while len(theBurrow.all_burrowStates) > 0:
theBurrow.next_move()
