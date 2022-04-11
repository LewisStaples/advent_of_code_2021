# adventOfCode 2021 day 23
# https://adventofcode.com/2021/day/23
#
# This version of the code for Day 23 will use classes and OOP
from enum import Enum
import sys
import copy

import astar
from numpy import not_equal

class Location(Enum):
    ORIGIN = 1
    DEST = 2
# End of class Location

class SideRoom:
    def __init__(self, amphipod_init):
        self.amphipod_structure = tuple(amphipod_init)

    def not_equal(self, other):
        if other is None:
            return True
        for i in range(len(self.amphipod_structure)):
            if self.amphipod_structure[i] != other.amphipod_structure[i]:
                return True
        return False

    def __ne__(self, other):
        return self.not_equal(other)

    def __eq__(self, other):
        if self.not_equal(other):
            return False
        else:
            return True

    def __hash__(self):
        hash_str = ''
        for i,ch in enumerate(self.amphipod_structure):
            if ch is None:
                hash_str += 'N'
            else:
                hash_str += ch

        for j in range(i+1, Burrow.AMPHIPOD_COUNT):
            hash_str += 'N'

        return hash(hash_str)

    def append(self, amphipod_next):
        self.amphipod_structure = self.amphipod_structure + (amphipod_next,)

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
            for i, amphipod in enumerate(self.amphipod_structure):
                if amphipod in Burrow.AMPHIPOD_LIST:
                    # Skip sideroom if all amphipods are at their intended destination
                    list_set = set(self.amphipod_structure[i:])
                    if len(list_set) == 1 and sideroom_dest_amph in list_set:
                        continue

                    return i
            return None

        elif location == Location.DEST:
            # Starting from the bottom ...
            # If any amphipods are found and if they wish to be sent to elsehwere, return None
            # If an empty slot is discovered, its index is returned
            # If the top is reached without encountering any empty slots, return None

            for i in range(len(self.amphipod_structure) - 1, -1, -1):
                if self.amphipod_structure[i] is None:
                    # Index of an empty slot.  An amphipod could be sent here.
                    return i
                # elif there is an amphipod and it wants to go elsewhere, then return None
                elif self.amphipod_structure[i] != sideroom_dest_amph:
                    return None
            dummy = 123
            return None
        
    def sideroom_pop(self):
        for amphipod in self.amphipod_structure:
            for i, amphipod in enumerate(self.amphipod_structure):
                if amphipod in Burrow.AMPHIPOD_LIST:
                    self.amphipod_structure = self.amphipod_structure[:i] + (None,) + self.amphipod_structure[i+1:]
                    return amphipod
        return None
# End of class SideRoom

class BurrowState:
    # Create a new BurrowState object, based on init_parameter.
    # Note that init_parameter could be a string or another BurrowState object
    def __init__(self, init_parameter):
        self.hallway = ()

        #  Create BurrowState object using a string representation what's in the hallway.
        #  This is intended to handle reading from the input file, and it is intended to only be run once.
        if isinstance(init_parameter, str):
            # Remove # and newline characters
            init_parameter = init_parameter.rstrip()[1:-1]
            for ch in init_parameter:
                if ch == '.':
                    self.hallway = self.hallway + (None,)

                elif ch in Burrow.AMPHIPOD_LIST:
                    self.hallway = self.hallway + (ch,)

                    # Counting amphipods at the start
                    Burrow.AMPHIPOD_COUNT += 1

                else:
                    sys.exit('Bad input character: ' + ch)

        # This code is run whenever duplicating a BurrowState.
        # It is intended to be used when a child BurrowState object is being created from a parent BurrowState object.
        elif isinstance(init_parameter, BurrowState):
            self.hallway = copy.deepcopy(init_parameter.hallway)
        
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
                new_val = SideRoom(None) if ch=='.' else SideRoom(ch)
                self.hallway = self.hallway[:i-1] + (new_val,) + self.hallway[i:]

                Burrow.SIDEROOM_INDICES.append(i-1)

                Burrow.DEST_AMPH__SIDEROOM_INDEX[i-1] = Burrow.AMPHIPOD_LIST[i_sideroom]
                Burrow.SIDEROOM_INDEX__DEST_AMPH[Burrow.AMPHIPOD_LIST[i_sideroom]] = i-1
                i_sideroom += 1
            
            if ch.isalpha():
                Burrow.AMPHIPOD_COUNT += 1

        if Burrow.PROBLEM_PART in ['B', 'b']:
            self.sideroom_append('  #D#C#B#A#')
            self.sideroom_append('  #D#B#A#C#')

    def sideroom_append(self, sideroom_str):
        has_no_amphipods = True
        for ch in Burrow.AMPHIPOD_LIST:
            if ch in sideroom_str:
                has_no_amphipods = False
        if has_no_amphipods:
            return
        for i in Burrow.SIDEROOM_INDICES:
            if sideroom_str[i+1] == '.':
                self.hallway[i] = self.hallway[i] + (None,)

            else:
                self.hallway[i].amphipod_structure = self.hallway[i].amphipod_structure + (sideroom_str[i+1],)
                Burrow.AMPHIPOD_COUNT += 1

    # Display contents of BurrowState (by printing)'
    # Note that this version should handle siderooms with varying numbers of indices
    def display(self):
        print()
        
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
                    if j < len(self.hallway[i].amphipod_structure):
                        if self.hallway[i].amphipod_structure[j] is None:
                            print('.', end='')
                        else:
                            print(self.hallway[i].amphipod_structure[j], end='')
                        amp_count += 1
                    else:
                        print('#', end='')
            print('#')
            j += 1
            # If amp_count is zero, then the length of all siderooms has been exceeded.
            if amp_count == 0:
                break
        print()
    
    def __eq__(self, other):
        return self.hallway == other.hallway

    def __hash__(self):
        hash_str = ''
        for ele in self.hallway:
            if ele is None:
                hash_str += 'N'
            elif isinstance(ele, str):
                hash_str += ele
            else:
                for i,ch in enumerate(ele.amphipod_structure):
                    if ch is None:
                        hash_str += 'N'
                    else:
                        hash_str += ch

                for j in range(i+1, Burrow.AMPHIPOD_COUNT):
                    hash_str += 'N'
        return hash(hash_str)

# End of class BurrowState

# Class Burrow will contain information that always applies to the burrow, whereas clas BurrowState has information that captures the momentary state of a burrow.
class Burrow(astar.AStar):
    # List of all amphipods (in alphabetical order, which is the desired order when the process will be completed)
    AMPHIPOD_LIST = ['A', 'B', 'C', 'D']
    # List of indices of siderooms
    SIDEROOM_INDICES = []

    # Create dictionary to lookup destination amphipod by sideroom's hallway index 
    DEST_AMPH__SIDEROOM_INDEX = dict()
    SIDEROOM_INDEX__DEST_AMPH = dict()

    # This dictionary has index = 'type of amphipod' and value is the energy.
    AMPHIPOD_ENERGY = {'A':1, 'B':10, 'C':100, 'D':1000}

    # This will count the total amphipods in the system
    # (the example code has eight amphipods in both input samples)
    AMPHIPOD_COUNT = 0

    PROBLEM_PART = None

    burrowState_lookup = dict()

    complete_burrowStateID = None

    # Note:  it is not necessary to look for obstacles in the SideRoom(s) because that protection is already implemented in class SideRoom.  Therefore this function looks for a character (type str) in any hallway slots between origin and destination.
    def no_hallway_obstacle(self, node2, origin, dest):
        step_dir = 1 if origin[0] < dest[0] else -1
        for i in range(origin[0] + step_dir, dest[0], step_dir):
            if isinstance(node2.hallway[i], str):
                return False
        return True

    def move_amph(self, node2, origin, dest):
        # Remove amphipod from origin
        if origin[1] is None:
            # Remove origin amphipod from hallway
            transfer_amphipod = node2.hallway[origin[0]]
            node2.hallway = node2.hallway[:origin[0]] + (None,) + node2.hallway[origin[0]+1:]

        else:
            # Remove origin amphipod from a sideroom
            transfer_amphipod = node2.hallway[origin[0]].sideroom_pop()

        # Add amphipod at destination
        if dest[1] is None:
            node2.hallway = node2.hallway[:dest[0]] + (transfer_amphipod,) + node2.hallway[dest[0]+1:]
        else:
            if transfer_amphipod != Burrow.DEST_AMPH__SIDEROOM_INDEX[dest[0]]:
                return (False, None)

            node2.hallway[dest[0]].amphipod_structure = node2.hallway[dest[0]].amphipod_structure[:dest[1]] + (transfer_amphipod,) + node2.hallway[dest[0]].amphipod_structure[dest[1]+1:] 

    # For a given node, returns (or yields) the list of its neighbors:
    def neighbors(self, node):
        ret_val = []

        sideroom_origins = self.list_siderooms(node, Location.ORIGIN)
        sideroom_destinations = self.list_siderooms(node, Location.DEST)
        hallway_origins = self.list_hallways(node, Location.ORIGIN)
        hallway_destinations = self.list_hallways(node, Location.DEST)

        # Send amphipod from one sideroom to another
        for origin in sideroom_origins:
            # change to if dest in si....
            for dest in sideroom_destinations:
                if origin[2] == dest[2]:
                    if self.no_hallway_obstacle(node, origin, dest):
                        # Copy node to node2
                        node2 = BurrowState(node)

                        # Move amphipod from origin to destination in node2
                        self.move_amph(node2, origin, dest)

                        # Add node2 to ret_val
                        ret_val.append(node2)

        # Send amphipod from hallway to sideroom
        for origin in hallway_origins:
            for dest in sideroom_destinations:
                if origin[2] == dest[2]:
                    if self.no_hallway_obstacle(node, origin, dest):
                        # Copy node to node2
                        node2 = BurrowState(node)

                        # Move amphipod from origin to destination in node2
                        self.move_amph(node2, origin, dest)

                        # Add node2 to ret_val
                        ret_val.append(node2)

        # Send amphipod from sideroom to hallway
        for origin in sideroom_origins:
            for dest in hallway_destinations:
                if self.no_hallway_obstacle(node, origin, dest):
                        # Copy node to node2
                        node2 = BurrowState(node)

                        # Move amphipod from origin to destination in node2
                        self.move_amph(node2, origin, dest)

                        # Add node2 to ret_val
                        ret_val.append(node2)

        return ret_val

    # Gives the real distance/cost between two adjacent nodes
    # (adjacent nodes titled parent_state and child_state to use code
    # that was created earlier)
    def distance_between(self, parent_state, child_state):
        discrepancy_list = []
        amph = None
        for i in range(len(parent_state.hallway)):
            # If parent hallway is SideRoom
            # 	Compare all SideRoom slots in the parent vs the child
            # 		If the one is None and the other is str
            # 			You have found one of the discrepancies
            # 			You have also identified the amphipod (do for parent only)
            if isinstance(parent_state.hallway[i], SideRoom):
                for j in range(len(parent_state.hallway[i].amphipod_structure)):
                    if parent_state.hallway[i].amphipod_structure[j] != child_state.hallway[i].amphipod_structure[j]:
                        discrepancy_list.append((i,j+1))
                        if type(parent_state.hallway[i].amphipod_structure[j]) == str:
                            amph = parent_state.hallway[i].amphipod_structure[j]
            # If parent hallway is a None or str
            # 	If child is different (or alternatively .... opposite type)
            # 		You have found one of the discrepancies
            # 		You have also identified the amphipod (do for parent only)
            else:  # parent_state.hallway[i] is either str or None
                if parent_state.hallway[i] != child_state.hallway[i]:
                    discrepancy_list.append((i,0))
                    if type(parent_state.hallway[i]) == str:
                        amph = parent_state.hallway[i]

        steps_traversed = abs(discrepancy_list[0][0] - discrepancy_list[1][0]) + discrepancy_list[0][1] + discrepancy_list[1][1]
        return steps_traversed * Burrow.AMPHIPOD_ENERGY[amph]

    # Computes the estimated (rough) distance/cost between a node and the goal. 
    # Per https://en.wikipedia.org/wiki/Admissible_heuristic , this must not be greater than the actual value
    def heuristic_cost_estimate(self, current, goal):
        # Below program will assume that goal will always be the final state
        if burrowState_compare(goal, self.final_burrowState):
            pass
        else:
            sys.exit('heuristic_cost_estimate has been called with an unexpected value of goal!')
        
        ret_val = 0
        # Compare current to expected final state 
        for i_hall, hallway_space in enumerate(current.hallway):
            if isinstance(hallway_space, str):
                ret_val += (1 + abs(i_hall - Burrow.SIDEROOM_INDEX__DEST_AMPH[hallway_space])) * Burrow.AMPHIPOD_ENERGY[hallway_space]
            elif isinstance(hallway_space, SideRoom):
                no_blocked_amphs_found_yet = True
                for i_sideroom in range(len(hallway_space.amphipod_structure) - 1, -1, -1):
                    ch = hallway_space.amphipod_structure[i_sideroom]
                    if ch == Burrow.DEST_AMPH__SIDEROOM_INDEX[i_hall]:
                        if no_blocked_amphs_found_yet:
                            continue
                    elif isinstance(ch, str):
                        no_blocked_amphs_found_yet = False
                    elif ch is None:
                        break
                    ret_val += (2 + abs(i_hall - Burrow.SIDEROOM_INDEX__DEST_AMPH[ch]) + i_sideroom) * Burrow.AMPHIPOD_ENERGY[ch]

        return ret_val

    def __init__(self, input_filename, problem_part):
        self.initial_burrowState = None
        Burrow.PROBLEM_PART = problem_part

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
                    self.initial_burrowState = BurrowState(in_string)
                    self.states_awaiting_next_move_analysis = [self.initial_burrowState]

                elif row_num == 2:
                    self.initial_burrowState.sideroom_init(in_string)

                else:
                    self.initial_burrowState.sideroom_append(in_string)

    # This gets a list of siderooms that can give up an amphipod (origin) or receive an amphipod (dest)
    def list_siderooms(self, burrowState, location):
        ret_val = []
        for hallway_index in Burrow.SIDEROOM_INDICES:
            sideroom_dest_amph = Burrow.DEST_AMPH__SIDEROOM_INDEX[hallway_index]  
            sideroom_index = burrowState.hallway[hallway_index].get_sideroom_index(location, sideroom_dest_amph)
            
            if location == Location.ORIGIN:
                if sideroom_index is not None: # sideroom space has an amphipod
                    ret_val.append((hallway_index, sideroom_index, burrowState.hallway[hallway_index].amphipod_structure[sideroom_index]))
                    dummy = 123
            else: # if destination
                if sideroom_index is not None:
                    ret_val.append((hallway_index, sideroom_index, self.DEST_AMPH__SIDEROOM_INDEX[hallway_index]))

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
                    ret_val.append((hallway_index, None, burrowState.hallway[hallway_index]))
        return ret_val
        
    # # detect difference between parent/child
    def energy_diff(self, parent_state, child_state):
        discrepancy_list = []
        amph = None
        for i in range(len(parent_state.hallway)):
            # If parent hallway is SideRoom
            # 	Compare all SideRoom slots in the parent vs the child
            # 		If the one is None and the other is str
            # 			You have found one of the discrepancies
            # 			You have also identified the amphipod (do for parent only)
            if isinstance(parent_state.hallway[i], SideRoom):
                for j in range(len(parent_state.hallway[i].amphipod_structure)):
                    if parent_state.hallway[i].amphipod_structure[j] != child_state.hallway[i].amphipod_structure[j]:
                        discrepancy_list.append((i,j+1))
                        if type(parent_state.hallway[i].amphipod_structure[j]) == str:
                            amph = parent_state.hallway[i].amphipod_structure[j]
            # If parent hallway is a None or str
            # 	If child is different (or alternatively .... opposite type)
            # 		You have found one of the discrepancies
            # 		You have also identified the amphipod (do for parent only)
            else:  # parent_state.hallway[i] is either str or None
                if parent_state.hallway[i] != child_state.hallway[i]:
                    discrepancy_list.append((i,0))
                    if type(parent_state.hallway[i]) == str:
                        amph = parent_state.hallway[i]

        steps_traversed = abs(discrepancy_list[0][0] - discrepancy_list[1][0]) + discrepancy_list[0][1] + discrepancy_list[1][1]

        return steps_traversed * Burrow.AMPHIPOD_ENERGY[amph]

# End of class Burrow

def burrowState_compare(this_burrow, new_burrow):
    this_hallway = this_burrow.hallway
    new_hallway = new_burrow.hallway
    for i in range(len(this_hallway)):
        if this_hallway[i] != new_hallway[i]:
            return False
    return True

def create_final_burrowState():
    ret_val = BurrowState('#...........#')
    for i in range(len(Burrow.AMPHIPOD_LIST)):

        # Get length of Sideroom in initial state (To support varying Sideroom lengths)
        sideroom_length = len(theBurrow.initial_burrowState.hallway[Burrow.SIDEROOM_INDICES[i]].amphipod_structure)
        ret_val.hallway = ret_val.hallway[:Burrow.SIDEROOM_INDICES[i]] + (SideRoom([Burrow.AMPHIPOD_LIST[i]]*sideroom_length),) + ret_val.hallway[Burrow.SIDEROOM_INDICES[i]+1:]
    return ret_val

theBurrow = Burrow('input_sample0.txt', 'B')
theBurrow.final_burrowState = create_final_burrowState()
theBurrow.initial_burrowState.display()

# Testing code
# neighbors = theBurrow.neighbors(theBurrow.initial_burrowState)
# for neighbor in neighbors:
#     distance = theBurrow.distance_between(theBurrow.initial_burrowState, neighbor)
#     dummy = 123

# Running code
path = list(theBurrow.astar(theBurrow.initial_burrowState, theBurrow.final_burrowState))

energy_total = 0
for i in range(len(path)-1):
    energy_total += theBurrow.energy_diff(path[i], path[i+1])
    # print( theBurrow.energy_diff(path[i], path[i+1]) )    # Use to see energy values, as they appear

print('Total energy = ', end='')
print(energy_total)
