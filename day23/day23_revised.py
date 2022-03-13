# adventOfCode 2021 day 23
# https://adventofcode.com/2021/day/23

# import enum
# from hashlib import new
import sys
import copy

# from numpy import isin

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


input_filename='input_scenario1.txt'
# Reading input from the input file
print()
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
            line_length = len(in_string.rstrip())
            if in_string.rstrip() != '#'*line_length:
                sys.exit('Bad input!')
        elif row_num == 1:            
            # Require first and last character to be #
            # if in_string.rstrip() != '#'+'.'*(line_length-2)+'#':
            if in_string[0] != '#' or in_string.rstrip()[-1] != '#':
                sys.exit('Bad input!')
            
            # Initialize list with all hallway positions unoccupied
            burrow_state_list[0][0].extend([None]*(line_length-2))


            for i,ch in enumerate(in_string):
                if ch in AMPHIPOD_LIST:
                    burrow_state_list[0][0][i-1] = ch
            pass

        elif row_num == 2:
            # find the letters and their side room position
            # replace None with the named 2-tuple (described above)
            for i,ch in enumerate(in_string):
                if ch.isalpha() or ch == '.':
                    # This hallway position is a side room.  Add first amphipod
                    dest_char = AMPHIPOD_LIST[len(side_room_position)]
                    side_room_position[i] = dest_char
                    burrow_state_list[0][0][i-1] = (dest_char,[ch]) if ch!='.' else (dest_char, [None])
                    sideroom_indices.append(i-1)
                    
            dummy = 123
        else:
            for i,ch in enumerate(in_string):
                if ch.isalpha():
                    burrow_state_list[0][0][i-1][1].append(ch)
            dummy = 123
        dummy = 123

dummy = 123

def add_burrow_to_list(burrow_state_list, new_hallway, energy_total):
    # burrow_state_list.append((new_hallway, energy_total))
    # consider using https://zepworks.com/deepdiff/current/

    # Traverse list to look for any duplicates
    for i_list,old_list in enumerate(burrow_state_list):
        match = True
        for i_element, element in enumerate(old_list[0]):
            if not isinstance(element, tuple):
                if element != new_hallway[i_element]:
                    match = False
            else:
                # compare element to new_hallway[i_element], which are lists of values
                if element[1] != new_hallway[i_element][1]:
                    match = False
        # If there is a match ...
        if match:
            # If the newer of the match has less energy ...
            if energy_total < old_list[1]:
                # remove the original and replace it with the lower energy one
                burrow_state_list[i_list] = (new_hallway, energy_total)
            # Assumption is that there can only be one match
            return
    # If this point reached, no matches found.  Therefore, add it as a new one
    burrow_state_list.append((new_hallway, energy_total))


# i_origin and i_dest will both be 2-tuples of int.  If either is a hallway then element 1 will be None.  Otherwise, if they are a sideroom then element 1 will be the sideroom index.  Element 0 will always be the hallway index.
def transfer_amphipod(burrow_state_list, i_origin, i_dest):
    # If there are no obstacles on the journey, create a new state in state_list but with the amphipod transferred and increase the energy and add this to the end of the list.
    energy_total = burrow_state_list[0][1]

    # Identify the amphipod being transferred
    amph_to_transfer = burrow_state_list[0][0][i_origin[0]] if i_origin[1] == None else burrow_state_list[0][0][i_origin[0]][1][i_origin[1]]

    # Logic if origin is a sideroom
    if i_origin[1] is not None:
        sideroom_position = i_origin[1]
        # While still in the origin sideroom, take one step toward the hallway (up)
        while sideroom_position > -1:
            # Increment two variables directly impacted by taking a step
            sideroom_position -= 1
            energy_total += 1
            # If still in the sideroom, check if there is an amphipod blocking the route
            if sideroom_position > -1 and \
            isinstance(burrow_state_list[0][0][i_origin[0]][1][sideroom_position], str):
                # Blocking amphipod detected, therefore cancel the transfer
                return False

    # Logic used in all transfers
    # Determine transfer direction in hallway (left or right)
    tran_dir = 1 if i_origin[0] < i_dest[0] else -1 
    hallway_posn = i_origin[0] + tran_dir
    energy_total += 1
    while hallway_posn != i_dest[0] and hallway_posn > -1:
        if isinstance(burrow_state_list[0][0][hallway_posn], str):
            return False
        hallway_posn += tran_dir
        energy_total += 1
        dummy = 123


    # Logic if destination is a sideroom
    if i_dest[1] is not None:
        # Verify that this destination sideroom is where the amphipod should be going
        if amph_to_transfer != burrow_state_list[0][0][i_dest[0]][0]:
            return False

        # Repeating commands used for origin
        sideroom_position = i_dest[1]

        # Take one (imaginary) step toward the hallway (up)
        # (The step is imaginary, because the direction is actually reversed)
        while sideroom_position > -1:
            # Increment two variables directly impacted by taking a step
            sideroom_position -= 1
            energy_total += 1
            # If still in the sideroom, check if there is an amphipod blocking the route
            if sideroom_position > -1 and \
            isinstance(burrow_state_list[0][0][i_dest[0]][1][sideroom_position], str):
                # Blocking amphipod detected, therefore cancel the transfer
                return False

        # # Increment energy for step from sideroom to the hallway
        # energy_total += 1
        # dummy = 123


    # The transfer will happen (because otherwise False would have been returned earlier)
    new_hallway = copy.deepcopy(burrow_state_list[0][0])
    
    # Remove amphipod from origin
    if i_origin[1] == None:
        new_hallway[i_origin[0]] = None  
    else:
        new_hallway[i_origin[0]][1][i_origin[1]] = None
    
    # Add amphipod at destination
    if i_dest[1] == None:
        new_hallway[i_dest[0]] = amph_to_transfer
    else:
        new_hallway[i_dest[0]][1][i_dest[1]] = amph_to_transfer

    # burrow_state_list.append((new_hallway, energy_total))
    add_burrow_to_list(burrow_state_list, new_hallway, energy_total)
    return True

def get_siderooms(burrow_state_list, in_str):
    ret_val = []

    for sideroom_index in sideroom_indices:
        # Variable pointing to this sideroom
        sideroom = burrow_state_list[0][0][sideroom_index]

        if in_str == 'origin':
            lowest_occupied = float('inf')
            for i_amphipod, amphipod in enumerate(sideroom[1]):
            # If sideroom slot unoccupied, look for an occupied slot
                if amphipod is None:
                    continue
            # Look for an amphipod that should end up elsewhere
            # (This should not have other amphipods put on top of it)
                if amphipod != sideroom[0]:
                    # This needs to use last variable as lowest index of an occupied slot
                    ret_val.append((sideroom_index, min(lowest_occupied, i_amphipod)))
                    break
                else:
                    lowest_occupied = min(lowest_occupied, i_amphipod)


        if in_str == 'dest':
            # Since all amphipods that are here belong here, any None can be used
            # Traverse all slots in the sideroom, from bottom to top
            for i_amphipod in range(len(sideroom[1])-1,-1,-1):
                if sideroom[1][i_amphipod] is None:
                    ret_val.append((sideroom_index, i_amphipod))
                    break
            # ret_val.append((sideroom_index, i_amphipod))

    return ret_val

def get_hallways(burrow_state_list, in_str):
    ret_val = []
    for i_elem,elem in enumerate(burrow_state_list[0][0]):
        if elem is None and in_str == 'dest':
            ret_val.append((i_elem, None))

        # # NOT YET TESTED, SO COMMENTING IT OUT FOR NOW
        # elif isinstance(elem, str) and in_str == 'origin':
        #     ret_val.append((i_elem, None))
    return ret_val

# Loop through function to try each possible move
# For one move, deepcopy burrow_state_list
# Then update both for that move
# Then consider another possible move
# Using depth first search, instead of breadth-first search should prevent storing too many possibilities in memory at once.
def next_move(burrow_state_list):
    pass
    # Possible moves
    # 1. Move directly from sideroom to destination sideroom (if conditions allow it)
    # 2. Move from hallway to destination sideroom (if conditions allow it)
    # 3. Move from sideroom to hallway (if conditions allow it, and if 1 isn't possible)
    #   (3) is skipped if (1) is possible, because (1) must be faster

    # Send an amphipod from origin sideroom directly to destination sideroom
    for tran_origin in get_siderooms(burrow_state_list, 'origin'):
        for tran_dest in get_siderooms(burrow_state_list, 'dest'):
            transfer_amphipod(burrow_state_list, tran_origin, tran_dest)
                # return

    # Send an amphipod from the hallway directly to destination sideroom
    # !!! NEEDED !!!

    # Send an amphipod from a sideroom to a hallway location
    for tran_origin in get_siderooms(burrow_state_list, 'origin'):
        for tran_dest in get_hallways(burrow_state_list, 'dest'):
            transfer_amphipod(burrow_state_list, tran_origin, tran_dest)

    # When this point gets reached, remove the 0th element from the list, because all next moves have been exhausted
    # burrow_state_list.pop(0)

# Code to use for real ....
# while len(burrow_state_list)>0:
#     next_move(burrow_state_list)

# Code for testing / development only
next_move(burrow_state_list)
# next_move(burrow_state_list)
# next_move(burrow_state_list)
# next_move(burrow_state_list)
# next_move(burrow_state_list)
# next_move(burrow_state_list)

for i in range(len(burrow_state_list)):
    # display = False
    # for ele in burrow_state_list[i][0]:
    #     if isinstance(ele,tuple):
    #         if ele[1][0] is None:
    #             display = True
    # if display:
    print([i for i in burrow_state_list[i][0]], end=', ')
    print(burrow_state_list[i][1])
print()


pass



