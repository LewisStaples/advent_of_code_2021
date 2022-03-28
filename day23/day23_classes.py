# adventOfCode 2021 day 23
# https://adventofcode.com/2021/day/23
#
# This version of the code for Day 23 will use classes and OOP
from enum import Enum
import sys
import copy
import logging

from numpy import isin

class Location(Enum):
    ORIGIN = 1
    DEST = 2
# End of class Location

class SideRoom:
    def __init__(self, amphipod_init):
        self.amphipod_list = [amphipod_init]

    def __ne__(self, other):
        for i in range(len(self.amphipod_list)):
            if self.amphipod_list[i] != other.amphipod_list[i]:
                return True
        return False

    def append(self, amphipod_next):
        self.amphipod_list.append(amphipod_next)

    # This tests if the amphipods in this given SideRoom can be used as origin 
    # (to send elsewhere), or if the sideroom can be used as a destination 
    # (to send amphipods to here)
    #
    # If the sideroom can be used, the index (an integer) of what can be used is returned.
    # If the sideroom cannot be used, None is returned
    def get_sideroom_index(self, location, sideroom_dest_amph):
        if location == Location.ORIGIN:
            # If the sideroom has no amphipods in it, then it returns None
            # If any amphipods are in the sideroom, and if all amphipods here intend to stay here, it returns None
            # Otherwise the index of the first encountered amphipod (starting from index 0) is returned
            for i, amphipod in enumerate(self.amphipod_list):
                if amphipod in Burrow.AMPHIPOD_LIST:
                    # Skip sideroom if all amphipods are at their intended destination
                    list_set = set(self.amphipod_list[i:])
                    if len(list_set) == 1 and sideroom_dest_amph in list_set:
                        continue

                    return i
            return None

        elif location == Location.DEST:
            # Starting from the bottom ...
            # If any amphipods are found and if they wish to be sent to elsehwere, return None
            # If an empty slot is discovered, its index is returned
            # If the top is reached without encountering any empty slots, return None

            for i in range(len(self.amphipod_list) - 1, -1, -1):
                if self.amphipod_list[i] is None:
                    # Index of an empty slot.  An amphipod could be sent here.
                    return i
                # elif there is an amphipod and it wants to go elsewhere, then return None
                elif self.amphipod_list[i] != sideroom_dest_amph:
                    return None
            dummy = 123
            return None
        
    def sideroom_pop(self):
        for amphipod in self.amphipod_list:
            for i, amphipod in enumerate(self.amphipod_list):
                if amphipod in Burrow.AMPHIPOD_LIST:
                    self.amphipod_list[i] = None
                    return amphipod
        return None
# End of class SideRoom

class BurrowState:
    def __init__(self, hallway_init):
        self.hallway = []
        self.children = []

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

        # This code is run whenever duplicating a BurrowState.
        elif isinstance(hallway_init, BurrowState):
            self.energy_total = hallway_init.energy_total
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
                # self.hallway[i-1] = SideRoom(ch)
                self.hallway[i-1] = SideRoom(None) if ch=='.' else SideRoom(ch)
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
            if sideroom_str[i+1] == '.':
                self.hallway[i].append(None)
            else:
                self.hallway[i].append(sideroom_str[i+1])
            dummy = 123

    # Log contents of BurrowState (write to log file)'
    # Note that this version should handle siderooms with varying numbers of indices
    def logging_BurrowState(self):
        logging.debug(' ID: ' + str(hex(id(self))))
        logging.debug(' Total Energy: ' + str(self.energy_total))

        # Display top line of '#' characters
        logging.debug(' ' + '#'*(len(self.hallway)+2))

        # Traverse the hallway, and display hallway one character at a time
        str_to_log = ' #'
        for hallway_space in self.hallway:
            if hallway_space is None:
                str_to_log += '.'
            if isinstance(hallway_space, SideRoom):
                str_to_log += '.'
            if isinstance(hallway_space, str):
                str_to_log += hallway_space
        str_to_log += '#'
        logging.debug(str_to_log)

        j = 0
        while True:
            # amp counts siderooms with amphipods visible
            amp_count = 0
            # print('#', end='')
            str_to_log = ' #'
            for i in range(len(self.hallway)):
                if i not in Burrow.SIDEROOM_INDICES:
                    # print('#', end='')
                    str_to_log += '#'
                else:
                    if j < len(self.hallway[i].amphipod_list):
                        if self.hallway[i].amphipod_list[j] is None:
                            # print('.', end='')
                            str_to_log += '.'
                        else:
                            # print(self.hallway[i].amphipod_list[j], end='')
                            str_to_log += self.hallway[i].amphipod_list[j]
                        amp_count += 1
                    else:
                        # print('#', end='')
                        str_to_log += '#'
            # print('#')
            str_to_log += '#'
            logging.debug(str_to_log)

            j += 1
            # If amp_count is zero, then the length of all siderooms has been exceeded.
            if amp_count == 0:
                break

        logging.debug('')

    # Display contents of BurrowState (by printing)'
    # Note that this version should handle siderooms with varying numbers of indices
    def display(self):
        print()
        print('ID: ', end='')
        print(hex(id(self)))
        print('Total Energy: ', end='')
        print(self.energy_total)
        
        # Display top line of '#' characters
        for i in range(len(self.hallway) + 2):
            print('#', end='')
        print()

        # Traverse the hallway, and display hallway one character at a time
        # 
        print('#', end='')
        for hallway_space in self.hallway:
            if hallway_space is None:
                print('.', end='')
            if isinstance(hallway_space, SideRoom):
                print('.', end='')
            if isinstance(hallway_space, str):
                print(hallway_space, end='')
        print('#')

        j = 0
        while True:
            # amp counts siderooms with amphipods visible
            amp_count = 0
            print('#', end='')
            for i in range(len(self.hallway)):
                if i not in Burrow.SIDEROOM_INDICES:
                    print('#', end='')
                else:
                    if j < len(self.hallway[i].amphipod_list):
                        if self.hallway[i].amphipod_list[j] is None:
                            print('.', end='')
                        else:
                            print(self.hallway[i].amphipod_list[j], end='')
                        amp_count += 1
                    else:
                        print('#', end='')
            print('#')
            j += 1
            # If amp_count is zero, then the length of all siderooms has been exceeded.
            if amp_count == 0:
                break
        print()
    
    def detect_completion(self):
        # Shortcut to detect completion, detect if hallway is empty.
        if len(self.hallway) == self.hallway.count(None) + len(Burrow.AMPHIPOD_LIST):
            return True
        else:
            return False

# End of class BurrowState

# Class Burrow will contain information that always applies to the burrow, whereas clas BurrowState has information that captures the momentary state of a burrow.
class Burrow:
    # List of all amphipods (in alphabetical order, which is the desired order when the process will be completed)
    AMPHIPOD_LIST = ['A', 'B', 'C', 'D']
    # List of indices of siderooms
    SIDEROOM_INDICES = []

    # Create dictionary to lookup destination amphipod by sideroom's hallway index 
    DEST_AMPH__SIDEROOM_INDEX = dict()

    # This dictionary has index = 'type of amphipod' and value is the energy.
    AMPHIPOD_ENERGY = {'A':1, 'B':10, 'C':100, 'D':1000}

    def __init__(self, input_filename):
        logging.basicConfig(filename='debug.log', filemode = "w", level=logging.DEBUG)
        self.initial_burrowState = None

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
                    # self.active_burrowStates.append(BurrowState(in_string))
                    self.initial_burrowState = BurrowState(in_string)
                    self.states_awaiting_next_move_analysis = [self.initial_burrowState]

                elif row_num == 2:
                    # self.active_burrowStates[0].sideroom_init(in_string)
                    self.initial_burrowState.sideroom_init(in_string)

                else:
                    # self.active_burrowStates[0].sideroom_append(in_string)
                    self.initial_burrowState.sideroom_append(in_string)

    def move_location(self, origin_fxn, dest_fxn, burrowState):
        for tran_origin in origin_fxn(burrowState, Location.ORIGIN):
            for tran_dest in dest_fxn(burrowState, Location.DEST):
                next_state = self.make_move(burrowState, tran_origin, tran_dest)
                if next_state is not None:
                    # self.active_burrowStates.append(next_state)
                    burrowState.children.append(next_state)
                    self.states_awaiting_next_move_analysis.append(next_state)

                    # If logging, log id's of burrowState, next_state
                    logging.debug(' ' + str(hex(id(burrowState))) + ' ---> ' + str(hex(id(next_state))))
                    next_state.logging_BurrowState()


    def next_move(self):
        if len(self.states_awaiting_next_move_analysis) > 0:
            burrowState = self.states_awaiting_next_move_analysis.pop()
        else:
            return

        # Send an amphipod from origin sideroom directly to destination sideroom
        self.move_location(self.list_siderooms, self.list_siderooms, burrowState)

        # Send an amphipod from the hallway directly to destination sideroom
        self.move_location(self.list_hallways, self.list_siderooms, burrowState)

        # # Send an amphipod from a sideroom to a hallway location
        self.move_location(self.list_siderooms, self.list_hallways, burrowState)

    # This gets a list of siderooms that can give up an amphipod (origin) or receive an amphipod (dest)
    def list_siderooms(self, burrowState, location):
        ret_val = []
        for hallway_index in Burrow.SIDEROOM_INDICES:
            sideroom_dest_amph = Burrow.DEST_AMPH__SIDEROOM_INDEX[hallway_index]  
            sideroom_index = burrowState.hallway[hallway_index].get_sideroom_index(location, sideroom_dest_amph)
            
            if location == Location.ORIGIN:
                if sideroom_index is not None: # sideroom space has an amphipod
                    ret_val.append((hallway_index, sideroom_index))
            else: # if destination
                if sideroom_index is not None:
                    ret_val.append((hallway_index, sideroom_index))

        dummy = 123
        return ret_val

    def list_hallways(self, burrowState, location):
        ret_val = []
        for hallway_index, hallway_space in enumerate(burrowState.hallway):
            if location == Location.DEST:
                if hallway_space is None:
                    ret_val.append((hallway_index, None))
            elif location == Location.ORIGIN:
                if isinstance(hallway_space, str):
                    ret_val.append((hallway_index, None))
        return ret_val

    def make_move(self, burrowState, tran_origin, tran_dest):
        step_count = 0

        # (1) If origin is a sideroom, calculate steps taken
        # Don't need to look out for obstacles while traversing sideroom, because 
        # only top level amphipods have been used
        if tran_origin[1] is not None:
            step_count += 1 + tran_origin[1]
        dummy = 123

        # (2) Take steps in hallway

        # Determine transfer direction in hallway (left or right)
        tran_dir = 1 if tran_origin[0] < tran_dest[0] else -1 
        hallway_posn = tran_origin[0] + tran_dir
        step_count += 1
        while hallway_posn != tran_dest[0] and hallway_posn > -1:
            if isinstance(burrowState.hallway[hallway_posn], str):
                # Amphipod obstacle in hallway detected
                return None
            hallway_posn += tran_dir
            step_count += 1

        # (3) If destination is a sideroom, calculate step counts
        if tran_dest[1] is not None:
            step_count += 1 + tran_dest[1]

        # Create a new burrowState object
        new_burrowState = BurrowState(burrowState)

        transfer_amphipod = None

        # Remove amphipod from origin
        if tran_origin[1] is None:
            # Remove origin amphipod from hallway
            pass # TO BE DEFINED LATER ... probably below code
            transfer_amphipod = new_burrowState.hallway[tran_origin[0]]
            new_burrowState.hallway[tran_origin[0]] = None
        else:
            # Remove origin amphipod from a sideroom
            transfer_amphipod = new_burrowState.hallway[tran_origin[0]].sideroom_pop()

        # Add amphipod at destination
        if tran_dest[1] is None:
            new_burrowState.hallway[tran_dest[0]] = transfer_amphipod
        else:
            if transfer_amphipod != Burrow.DEST_AMPH__SIDEROOM_INDEX[tran_dest[0]]:
                return None
            new_burrowState.hallway[tran_dest[0]].amphipod_list[tran_dest[1]] = transfer_amphipod
            pass

        new_burrowState.energy_total += step_count * Burrow.AMPHIPOD_ENERGY[transfer_amphipod]

        # See if the state is already in the list of states
        # If state is already there, then keep it but
        # if the new energy_total is lower than change it to the new lower value.
        return self.verify_state_is_new(new_burrowState)

    # detect difference between parent/child and recalculate child's energy
    # Traverse both hallways, one space/SideRoom at a time
    # until first discrepancy detected
    # continue traversal but count the energy difference along the way
    def energy_diff(self, parent_state, child_state):
        # dummy implementation ... fill in later
        return 42



    # Call function that accepts new_burrowState.
    # The function will traverse the list of all burrowStates to look for a matching hallway
    # If a match is found,
    #    ensure that that match has the lowest_energy total,
    #    and then return None
    # Otherwise, return newBurrowState
    def verify_state_is_new(self, new_burrowState):
        stack = [self.initial_burrowState]
        while len(stack) > 0:
            this_state = stack.pop()
            if hallway_compare(this_state.hallway, new_burrowState.hallway):
                this_state.energy_total = min(this_state.energy_total, new_burrowState.energy_total)
                stack.clear()

                    

                while True:
                    # put all children in the stack, as a pair (with its parent)
                    for child in this_state.children:
                        stack.append((this_state, child))
                    if len(stack) == 0:
                        return None
                    # pop out one parent / child pair at a time
                    this_state, child = stack.pop()
                    child.energy_total = min(child.energy_total, this_state.energy_total + self.energy_diff(child, this_state))
                    this_state = child

            for child in this_state.children:
                stack.append(child)

        # new_burrowState.detect_completion()
        return new_burrowState
# End of class Burrow

def hallway_compare(this_hallway, new_hallway):
    for i in range(len(this_hallway)):
        if this_hallway[i] != new_hallway[i]:
            return False
    return True

theBurrow = Burrow('input_sample0.txt')
# theBurrow.initial_burrowState.display()
logging.debug(' Initial Burrow State:')
theBurrow.initial_burrowState.logging_BurrowState()

while len(theBurrow.states_awaiting_next_move_analysis) > 0:
    theBurrow.next_move()

# theBurrow.next_move()
# theBurrow.next_move()
# theBurrow.next_move()
dummy = 123

