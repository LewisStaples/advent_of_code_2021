# adventOfCode 2021 day 23
# https://adventofcode.com/2021/day/23

import enum
import sys
import copy

from numpy import isin

# List of all amphipods (in alphabetical order, which is the desired order when the process will be completed)
AMPHIPOD_LIST = ['A', 'B', 'C', 'D']

# This dictionary has index = 'type of amphipod' and value is a list with energy and the hallway location that goes into its destination room.  These are immutable characteristics (it will be populated from the input file and it will not change afterward)
AMPHIPOD_CHARACTERISTICS = {'A':[1], 'B':[10], 'C':[100], 'D':[1000]}

# This is a list of states, where each state is a list where each element is a 2-tuple with elements  list (amphipod positions, described below) and an integer, representing the energy consumed.
# 
# The list of amphipod positions represents a location in the hallway.  Each value elements is one of the below:  
# 1. None.  This indicates that the hallway location is currently unoccupied.
# 2. A character (any index of AMPHIPOD_CHARACTERISTICS), indicating that an amphipod is in that location.
# 3. A 2-tuple, indicating that that hallway location leads to a side room.  The first element is a character indicating which amphipod intends to end in that side room.  The second element is a list of characters, which lists all amphipods that are in that side room.
burrow_state_list = [([], 0)]

# This stores the smallest yet encountered total energy.
# When the program finishes, this will be the answer.
least_total_energy = float('inf')

# This is a list of ints that are indices to where the siderooms are
sideroom_indices = []


input_filename='input.txt'
# Reading input from the input file
print('Reading input from ', end='')
print(input_filename)
print()

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
            burrow_state_list[0][0].extend([None]*(line_length-2))
            dummy = 123

        elif row_num == 2:
            # find the letters and their side room position
            # replace None with the named 2-tuple (described above)
            for i,ch in enumerate(in_string):
                if ch.isalpha():
                    # This hallway position is a side room.  Add first amphipod
                    dest_char = AMPHIPOD_LIST[len(side_room_position)]
                    side_room_position[i] = dest_char
                    burrow_state_list[0][0][i-1] = (dest_char,[ch])
                    sideroom_indices.append(i-1)
                    
            dummy = 123
        else:
            for i,ch in enumerate(in_string):
                if ch.isalpha():
                    burrow_state_list[0][0][i-1][1].append(ch)
            dummy = 123
        dummy = 123

dummy = 123


# i_origin and i_dest will both be 2-tuples of int.  If either is a hallway then element 1 will be None.  Otherwise, if they are a sideroom then element 1 will be the sideroom index.  Element 0 will always be the hallway index.
# def transfer_amphipod(amp_position_list, i_origin, i_dest):
def transfer_amphipod(burrow_state_list, i_origin, i_dest):
    # If there are no obstacles on the journey, create a new state in state_list but with the amphipod transferred and increase the energy and add this to the end of the list.
    energy_diff = 0
    # Logic if origin is a sideroom
    if i_origin[1] is not None:
        sideroom_position = i_origin[1]
        while sideroom_position > 1:
            sideroom_position -= 1
            # NEED TO ADD ... CHECK IF PRIOR IS OCCUPIED, INCREMENT ENERGY_DIFF
            # if amp_position_list[hallway_position][1]

        # Increment energy for step from sideroom to the hallway
        energy_diff += 1
    

    
    tran_dir = 1 if i_origin[0] < i_dest[0] else -1
    hallway_posn = i_origin[0] + tran_dir
    energy_diff += 1
    while hallway_posn != i_dest[0]:
        if isinstance(burrow_state_list[0][0][hallway_posn], str):
            return False
        hallway_posn += tran_dir
        energy_diff += 1


    # Logic if destination is a sideroom
    # (To be added later)


    # The transfer will happen (because otherwise False would have been returned earlier)
    new_hallway = copy.deepcopy(burrow_state_list[0][0])
    # NEED TO ADD ... replace origin amph. with None, add dest amph. (replace the None there) in the copy.  Then put energy in with a tuple
    amph_to_transfer = new_hallway[i_origin[0]] if i_origin[1] == None else new_hallway[i_origin[0]][1][i_origin[1]]
    if i_origin[1] == None:
        new_hallway[i_origin[0]] = None  
    else:
        new_hallway[i_origin[0]][1][i_origin[1]] = None
    if i_dest[1] == None:
        new_hallway[i_dest[0]] = amph_to_transfer
    else:
        new_hallway[i_dest[0]][1][i_dest[1]] = amph_to_transfer
    return True


# Loop through function to try each possible move
# For one move, deepcopy burrow_state_list
# Then update both for that move
# Then consider another possible move
# Using depth first search, instead of breadth-first search should prevent storing too many possibilities in memory at once.
def next_move(burrow_state_list):
    # Possible moves
    # 1. Move directly from sideroom to destination sideroom (if conditions allow it)
    # 2. Move from hallway to destination sideroom (if conditions allow it)
    # 3. Move from sideroom to hallway (if conditions allow it, and if 1 isn't possible)
    #   (3) is skipped if (1) is possible, because (1) must be faster

    # Check all siderooms if eligible to receive an amphipod.
    for sideroom_dest in sideroom_indices:
        eligible = True
        for i_dest, amp_dest in enumerate(burrow_state_list[0][0][sideroom_dest][1]):
            # if any that aren't the destination amphipod, then it's ineligible
            # otherwise it's eligible (if empty or with 1+ destination amphipods)
            if amp_dest != burrow_state_list[0][0][sideroom_dest][0]:
                eligible = False
        if eligible:
            for sideroom_origin in sideroom_indices:
                if sideroom_dest==sideroom_origin:
                    continue
                for i_origin,amp_origin in enumerate(burrow_state_list[0][0][sideroom_origin][1]):
                    if amp_origin is None:
                        continue
                    if amp_origin == amp_dest:
                        # if transfer_amphipod(burrow_state_list[0][0][sideroom_origin][1], i_origin, burrow_state_list[0][0], i_dest):
                        if True:
                            break
                    break

    # Check all hallway locations for amphipods that could be sent to destination sideroom.
    pass

    # Send an amphipod to a hallway location
    for sideroom_origin in sideroom_indices:
        for i_origin, amp_origin in enumerate(burrow_state_list[0][0][sideroom_origin][1]):
            # Skip over any open slots in sideroom_origin
            if amp_origin is None:
                continue


            # If the first amphipod is the destination, then
            if amp_origin == burrow_state_list[0][0][sideroom_origin][0]:
                # Breaking from inner loop should continue the outer loop
                break
            # if amp_origin != burrow_state_list[0][0][sideroom_origin][0]:
            # Since the first amphipod isn't the destination ...
            # send to a hallway location
            for i_dest, hallway_dest in enumerate(burrow_state_list[0][0]):
                if hallway_dest is None:
                    if transfer_amphipod(burrow_state_list, (sideroom_origin, i_origin), (i_dest, None)):
                        break

            # Do not try any amphipods in sideroom_origin after the first one
            break
    
    # When this point gets reached, remove the 0th element from the list, because all next moves have been exhausted
    burrow_state_list.pop(0)

    # continue_condition = True
    # while continue_condition:
    #     continue_condition = False

while len(burrow_state_list)>0:
    next_move(burrow_state_list)

# continue_condition = True
# while continue_condition:
#     continue_condition = next_move(burrow_state_list)
