# adventOfCode 2021 day 22
# https://adventofcode.com/2021/day/22

input_cube_reset_instructions = []
cubes_on = set()

def get_volume_from_block(block):
    ret_val = 1
    for i in range(len(block[0])):
        ret_val *= (block[1][i] - block[0][i])
    return ret_val

# Detects any clash between the two input cubes
# Returns None if there is no clash.
# Returns a cube of the region with a clash if there is any clash
def get_clash(cube1, cube2):
    min_pt = []
    max_pt = []
    for i in range(len(cube1[0])):
        # Look for two scenarios without any overlaps in this axis
        if cube1[1][i] <= cube2[0][i]:
            return None
        if cube2[1][i] <= cube1[0][i]:
            return None
        
        # Store information about the overlap in this axis
        min_pt.append(max(cube1[0][i], cube2[0][i]))
        max_pt.append(min(cube1[1][i], cube2[1][i]))

    # Only if all three axes have a clash.
    return (tuple(min_pt), tuple(max_pt))

# This breaks up cube into pieces that completely cover the non-clash region of cube
# Only those pieces (covering non-clash region) are returned
def break_up(cube_whole, cube_clash):
    cube_remaining_after_breakup = [list(x) for x in cube_whole]
    ret_val = []
    for i in range(len(cube_whole[0])):
        if cube_remaining_after_breakup[0][i] != cube_clash[0][i]:
            cube_to_add = [list(x) for x in cube_remaining_after_breakup]
            cube_to_add[1][i] = cube_clash[0][i]
            cube_to_add = (tuple(x) for x in cube_to_add)
            ret_val.append(tuple(cube_to_add))

        if cube_remaining_after_breakup[1][i] != cube_clash[0][i]:
            cube_to_add = [list(x) for x in cube_remaining_after_breakup]
            cube_to_add[0][i] = cube_clash[1][i]
            cube_to_add = (tuple(x) for x in cube_to_add)
            ret_val.append(tuple(cube_to_add))

        cube_remaining_after_breakup[0][i] = cube_clash[0][i]
        cube_remaining_after_breakup[1][i] = cube_clash[1][i]

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
        newest_cube = (tuple(min_pt), tuple(max_pt))

        # additional loop needed here .... while True:
        while True:
            # iterate through cubes_on to seek out clashes
            for cube in cubes_on:
                clash_cube = get_clash(cube, newest_cube)
                # if there's a clash, remove current from set cubes_on and break it up so clash is resolved
                if clash_cube:
                    cubes_on.remove(cube)
                    broken_up_cubes = break_up(cube, clash_cube)
                    # cubes_on.add(broken_up_cubes)
                    for broken_cube in broken_up_cubes:
                        cubes_on.add(broken_cube)
                    break # end for loop (for cube in cubes_on), since the set is now modified

            break # break out of while True loop (only runs if for loop runs to completion)

        if self.operation == 'on':
            cubes_on.add(newest_cube)

            
            # return all broken pieces that comprise non-clash to the set
        # start over with iteration to see if any other elements of the set clash
        # at end, if on add newest_cube to set of cubes .... alternatively if off, discard newest_cube
    


        # if self.operation == 'on':
        #     if True: # if no clash
        #         cubes_on.add(  ( (self.ranges['x'][0], self.ranges['y'][0], self.ranges['z'][0])  ,  (self.ranges['x'][1], self.ranges['y'][1], self.ranges['z'][1]) )  )

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

for cube in cubes_on:
    number_of_cubes += get_volume_from_block(cube)

print('The answer to part B is: ', end='')
# print('To Be Determined') # temporary
print(number_of_cubes) # eventual answer to the problem



