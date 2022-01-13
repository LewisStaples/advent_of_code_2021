# adventOfCode 2021 day 22
# https://adventofcode.com/2021/day/22

input_cube_reset_instructions = []
reactor = set()

class CubeResetInstruction:
    # Load a line of input instructions into memory
    def __init__(self, str_input):
        self.operation, str_input = str_input.split(' ')
        self.ranges = {}
        for str_input in str_input.split(','):
            axis, str_input = str_input.split('=')
            self.ranges[axis] = str_input.split('..')
            self.ranges[axis] = list(map(int, self.ranges[axis]))

            # Restrict to range -50 through +50
            if self.ranges[axis][0] < -50:
                self.ranges[axis][0] = -50
            if self.ranges[axis][1] > 50:
                self.ranges[axis][1] = 50
            if self.ranges[axis][0] > self.ranges[axis][1]:
                self.operation = False
                break
    # End of __init__ declaration

    # Execute this one instruction
    def execute(self):
        for i in range(self.ranges['x'][0], 1 + self.ranges['x'][1]):
            for j in range(self.ranges['y'][0], 1 + self.ranges['y'][1]):
                for k in range(self.ranges['z'][0], 1 + self.ranges['z'][1]):
                    this_cube = (i,j,k)
                    if self.operation == 'on':
                        reactor.add(this_cube)
                    if self.operation == 'off':
                        reactor.discard(this_cube)

# Reading input from the input file
input_filename='input.txt'
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
    icri.execute()

print('The answer to part A is: ', end='')
print(len(reactor))

