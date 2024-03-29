# adventOfCode 2021 day 23
# https://adventofcode.com/2021/day/23
#
# This version of the code for Day 23 will use classes and OOP
from enum import Enum
import sys
import copy
import logging
import uuid

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
    # Create a new BurrowState object, based on init_parameter.
    # Note that init_parameter could be a string or another BurrowState object
    def __init__(self, init_parameter):
        self.hallway = []
        self.children = []
        self.parent = None  
        self.id = uuid.uuid4().int
        # Using lookup table for debugging only, because it's not needed for the actual program
        Burrow.burrowState_lookup[self.id] = self

        #  Create BurrowState object using a string representation what's in the hallway.
        #  This is intended to handle reading from the input file, and it is intended to only be run once.
        if isinstance(init_parameter, str):
            self.energy_total = 0
            # Remove # and newline characters
            init_parameter = init_parameter.rstrip()[1:-1]
            for ch in init_parameter:
                if ch == '.':
                    self.hallway.append(None)
                elif ch in Burrow.AMPHIPOD_LIST:
                    self.hallway.append(ch)
                else:
                    sys.exit('Bad input character: ' + ch)
            dummy = 123

        # This code is run whenever duplicating a BurrowState.
        # It is intended to be used when a child BurrowState object is being created from a parent BurrowState object.
        elif isinstance(init_parameter, BurrowState):
            self.energy_total = init_parameter.energy_total
            self.hallway = copy.deepcopy(init_parameter.hallway)
            self.parent = init_parameter.id
        
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
    def logging_BurrowState(self, wrap=False):
        # logging.debug(' ID: ' + str(hex(id(self))))

        logging.debug(' ' + str(self.parent) + ' ---> ' + str(self.id))
        logging.debug(' ID: ' + str(self.id))
        # logging.debug(' Total Energy: ' + str(self.energy_total))

        # Display top line of '#' characters
        str_to_log = ''
        if wrap:
            str_to_log += '\n'
        str_to_log += ' ' + '#'*(len(self.hallway)+2) + '|'
        if wrap:
            str_to_log += '\n'

        # Traverse the hallway, and display hallway one character at a time
        str_to_log += ' #'
        for hallway_space in self.hallway:
            if hallway_space is None:
                str_to_log += '.'
            if isinstance(hallway_space, SideRoom):
                str_to_log += '.'
            if isinstance(hallway_space, str):
                str_to_log += hallway_space
        str_to_log += '#|'
        if wrap:
            str_to_log += '\n'

        j = 0
        while True:
            # amp counts siderooms with amphipods visible
            amp_count = 0
            # print('#', end='')
            str_to_log += ' #'
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
            str_to_log += '#|'
            if wrap:
                str_to_log += '\n'
            # logging.debug(str_to_log)

            j += 1
            # If amp_count is zero, then the length of all siderooms has been exceeded.
            if amp_count == 0:
                break
        if wrap:
            str_to_log += '\n'
        logging.debug(str_to_log)
        logging.debug('')
        logging.debug('')

    # Display contents of BurrowState (by printing)'
    # Note that this version should handle siderooms with varying numbers of indices
    def display(self):
        print()
        # print('ID: ', end='')
        # print(hex(id(self)))
        print('parent', end='')
        print(self.parent)
        print('ID: ', end='')
        print(self.id)
        
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
            Burrow.complete_burrowStateID = self.id
            return True
        else:
            return False

    def __eq__(self, other):
        return self.hallway == other.hallway

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

    burrowState_lookup = dict()

    complete_burrowStateID = None

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
                original, next_state = self.make_move(burrowState, tran_origin, tran_dest)
                # if next_state is not None: # this is correct but less readable than below replacement
                if isinstance(next_state, BurrowState):
                    burrowState.children.append(next_state)
                    if original:
                        self.states_awaiting_next_move_analysis.append(next_state)

                    # If logging, log id's of burrowState, next_state
                    # logging.debug(' ' + str(hex(id(burrowState))) + ' ---> ' + str(hex(id(next_state))))
                    
                    next_state.logging_BurrowState(wrap=True)

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
                return (False, None)
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
                return (False, None)
            new_burrowState.hallway[tran_dest[0]].amphipod_list[tran_dest[1]] = transfer_amphipod
            pass

        new_burrowState.energy_total += step_count * Burrow.AMPHIPOD_ENERGY[transfer_amphipod]

        # See documentation for function verify_state_is_new
        return self.verify_state_is_new(new_burrowState)
    


    # # detect difference between parent/child and recalculate child's energy
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
                for j in range(len(parent_state.hallway[i].amphipod_list)):
                    if parent_state.hallway[i].amphipod_list[j] != child_state.hallway[i].amphipod_list[j]:
                        discrepancy_list.append((i,j+1))
                        if type(parent_state.hallway[i].amphipod_list[j]) == str:
                            amph = parent_state.hallway[i].amphipod_list[j]
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

        # debugging only
        # logging.debug('PARENT')
        # parent_state.logging_BurrowState(wrap = True)
        # logging.debug('CHILD')
        # child_state.logging_BurrowState(wrap = True)

        dummy = 123

        return steps_traversed * Burrow.AMPHIPOD_ENERGY[amph]


    # Call function that accepts new_burrowState.
    # The function will traverse the tree of all burrowStates to look for a matching hallway
    #   stack1 helps to traverse the tree of all burrowStates by listing all child states
    #   whose parent has been seen and the child hasn't.
    #
    # If no match is found, return (True, new_burrowState)
    # If a match is found, the return 2-tuple's index 0 will be False
    # If the new_burrowState's energy is greater or equal than what was found in stack1, return (False, this_state) to keep using what was found on stack1.
    # If the new_burrowState's energy is greater or equal than what was found using stack1, reset the energy of what was found using stack1 to the newest (lower) energy, and then use stack2 to traverse the subtree of its descendants and recalculate their energies.  When stack2 traversal is complete return (False, this_state) to keep using the memory location found on stack1.
    def verify_state_is_new(self, new_burrowState):

        # if new_burrowState.detect_completion():
        #     print('Energy Total: ', end='')
        #     print(new_burrowState.energy_total, end=' , ID = ')
        #     print(new_burrowState.id)

        stack1 = [self.initial_burrowState]
        while len(stack1) > 0:
            this_state = stack1.pop()

            # if hallway_compare(this_state.hallway, new_burrowState.hallway):
            if burrowState_compare(this_state, new_burrowState):
                stack2 = []

                if this_state.energy_total <= new_burrowState.energy_total:
                    return (False, this_state) # match found has the lower energy than the new one, so don't replace it

                # Since new_burrowState's energy_total is lower, bring its values to this_state
                this_state.energy_total = new_burrowState.energy_total
                this_state.parent = new_burrowState.parent

                # if this_state.detect_completion():
                #     print('Energy Total: ', end='')
                #     print(this_state.energy_total)

                while True:
                    # put all children in  stack2, as a pair (with its parent)
                    for child in this_state.children:
                        stack2.append((this_state, child))
                    if len(stack2) == 0:
                        return (False, this_state) # The match found had higher energy than the new one, so its descendants' energies were recalculated
                    # pop out one parent / child pair at a time
                    this_state, child = stack2.pop()
                    
                    # if child.energy_total > this_state.energy_total + self.energy_diff(child, this_state):
                    #     child.energy_total = this_state.energy_total + self.energy_diff(child, this_state)
                    s_e_d = self.energy_diff(child, this_state)
                    if child.energy_total > this_state.energy_total + s_e_d:
                        child.energy_total = this_state.energy_total + s_e_d
                        child.parent = this_state
                    this_state = child

                    # if child.detect_completion():
                    #     print('Energy Total: ', end='')
                    #     print(child.energy_total)

            for child in this_state.children:
                stack1.append(child)

        # This is truly new
        new_burrowState.detect_completion()
        return (True, new_burrowState)
# End of class Burrow

def burrowState_compare(this_burrow, new_burrow):
    # logging.debug('this_burrow:')
    # this_burrow.logging_BurrowState(wrap=True)
    # logging.debug('new_burrow:')
    # new_burrow.logging_BurrowState(wrap=True)
    this_hallway = this_burrow.hallway
    new_hallway = new_burrow.hallway
    for i in range(len(this_hallway)):
        if this_hallway[i] != new_hallway[i]:
            return False
    return True

theBurrow = Burrow('input_sample0.txt')
theBurrow.initial_burrowState.display()
logging.debug(' Initial Burrow State:')
theBurrow.initial_burrowState.logging_BurrowState(wrap=True)

while len(theBurrow.states_awaiting_next_move_analysis) > 0:
    theBurrow.next_move()


# for iii in range(20):
#     theBurrow.next_move()

print('Lowest energy found is: ', end='')
print(theBurrow.burrowState_lookup[Burrow.complete_burrowStateID].energy_total)

dummy = 123
