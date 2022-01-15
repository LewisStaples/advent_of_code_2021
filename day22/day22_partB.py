# adventOfCode 2021 day 22
# https://adventofcode.com/2021/day/22

input_cube_reset_instructions = []
blocks_on = set()

def get_volume_from_block(block):
    ret_val = 1
    for i in range(len(block[0])):
        ret_val *= (block[1][i] - block[0][i] + 1)
    return ret_val

# Detects any clash between the two input blocks
# Returns None if there is no clash.
# Returns a block of the region with a clash if there is any clash
def get_clash(block1, block2):
    min_pt = []
    max_pt = []
    for i in range(len(block1[0])):
        # Look for two scenarios without any overlaps in this axis
        if block1[1][i] <= block2[0][i]:
            return None
        if block2[1][i] <= block1[0][i]:
            return None
        
        # Store information about the overlap in this axis
        min_pt.append(max(block1[0][i], block2[0][i]))
        max_pt.append(min(block1[1][i], block2[1][i]))

    # Only if all three axes have a clash.
    return (tuple(min_pt), tuple(max_pt))

# This breaks up block into pieces that completely cover the non-clash region of block
# Only those pieces (covering non-clash region) are returned
def break_up(block_whole, block_clash):
    block_remaining_after_breakup = [list(x) for x in block_whole]
    ret_val = []
    for i in range(len(block_whole[0])):
        if block_remaining_after_breakup[0][i] != block_clash[0][i]:
            block_to_add = [list(x) for x in block_remaining_after_breakup]
            block_to_add[1][i] = block_clash[0][i] - 1
            block_to_add = (tuple(x) for x in block_to_add)
            ret_val.append(tuple(block_to_add))

        if block_remaining_after_breakup[1][i] != block_clash[1][i]:
            block_to_add = [list(x) for x in block_remaining_after_breakup]
            block_to_add[0][i] = block_clash[1][i]
            block_to_add = [tuple(x) for x in block_to_add]
            ret_val.append(tuple(block_to_add))

        block_remaining_after_breakup[0][i] = block_clash[0][i]
        block_remaining_after_breakup[1][i] = block_clash[1][i]

    return ret_val

class CubeResetInstruction:
    # Load a line of input instructions into memory
    def __init__(self, str_input):
        self.operation, str_input = str_input.split(' ')
        self.ranges = {}
        for str_input in str_input.split(','):
            axis, str_input = str_input.split('=')
            self.ranges[axis] = str_input.split('..')
            self.ranges[axis] = list(map(int, self.ranges[axis]))
        pass
    # End of __init__ declaration

    # Execute this one instruction
    def execute_instruction(self):
        min_pt = []
        max_pt = []
        axes = ['x', 'y', 'z']
        for axis in axes:
            min_pt.append(self.ranges[axis][0])
            max_pt.append(self.ranges[axis][1])
        newest_block = (tuple(min_pt), tuple(max_pt))

        # Additional loop needed here .... while True:
        while True:
            # Iterate through blocks_on to seek out clashes
            for on_block___from_set in blocks_on:
                clash_block = get_clash(on_block___from_set, newest_block)
                # if there's a clash, remove current from set blocks_on and break it up so clash is resolved
                if clash_block:
                    blocks_on.remove(on_block___from_set)
                    broken_up_blocks = break_up(on_block___from_set, clash_block)
                    # return all broken pieces that comprise non-clash to the set
                    for broken_block in broken_up_blocks:
                        blocks_on.add(broken_block)
                    break # Break out of for loop (for on_block___from_set in blocks_on), since the set is now modified
                          # Note that this will repeat the while True loop

            break # Break out of while True loop (only runs if for loop runs to completion)

        # At end, if on add newest_block to set of blocks .... alternatively if off, discard newest_block
        if self.operation == 'on':
            blocks_on.add(newest_block)

            
            
        # start over with iteration to see if any other elements of the set clash
        
    

# Reading input from the input file
input_filename='input_sample2.txt'
with open(input_filename) as f:
    del input_filename
    # pull in each line from the input file
    for in_string in f:
        in_string = in_string.rstrip()
        cri = CubeResetInstruction(in_string)
        if cri.operation:
            input_cube_reset_instructions.append(cri)

# Delete variables that are no longer needed
del cri
del in_string
del f

for icri in input_cube_reset_instructions:
    icri.execute_instruction()

number_of_cubes = 0

for block in blocks_on:
    number_of_cubes += get_volume_from_block(block)

print('The answer to part B is: ', end='')
print(number_of_cubes) # eventual answer to the problem
