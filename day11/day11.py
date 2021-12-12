# adventOfCode 2021 day 11
# https://adventofcode.com/2021/day/11


import enum

# this enum defines the states of an octopus during a step:
class FlashStatus(enum.Enum):
    # it hasn't flashed yet in the current step
    NOT_FLASHED = 0

    # it has just flashed
    JUST_FLASHED = 1

    # it flashed earlier (the adjacent octpuses already had energy increased)
    PREVIOUSLY_FLASHED = 2


# this class defines the status of a particular octopus
class OctopusStatus:
    def __init__(self, energy):
        self.energy = energy
        self.flashed = FlashStatus.NOT_FLASHED
        
        # total number of times that this octopus has flashed
        self.flash_tally = 0

    # get the current value of energy
    def get_energy(self):
        return self.energy
    
    # this determines if the octopus has been flashed
    def get_flashed(self):
        return self.flashed

    # get total number of times that this octopus has flashed
    def get_flash_tally(self):
        return self.flash_tally

    # increase energy, update associated flash statuses
    def increment_energy(self):
        self.energy += 1
        if self.energy == 10:
            self.flashed = FlashStatus.JUST_FLASHED
            self.flash_tally += 1

    # update flash status to PREVIOUSLY_FLASHED
    def post_flashed(self):
        self.flashed = FlashStatus.PREVIOUSLY_FLASHED

    # (at the end of a step) reset octopus status
    def reset_energy(self):
        self.energy = 0
        self.flashed = FlashStatus.NOT_FLASHED


# this class holds the data structure for all octopuses,
# and implements associated logic
class Octopus:
    def __init__(self):
        self.oct_status = []

    # returns True/False, if all octopuses are flashing right now
    # 
    # this function should be called before reset_to_zero is run
    # (since it is designed to capture the state before that is run)
    def are_all_octopuses_flashing(self):
        # traverse all octopuses ... return False immediately if an unflashed octopus is found
        for i in range(len(self.oct_status)):
            for j in range(len(self.oct_status[i])):
                if self.oct_status[i][j].get_flashed() == FlashStatus.NOT_FLASHED:
                    return False

        # if the end gets reached, then the answer is True (all octopuses are flashing)
        return True

    # calculates total number of times that all octupuses have flashed (in the past as well as now)
    def get_flash_tally(self):
        ret_val = 0
        for i in range(len(self.oct_status)):
            for j in range(len(self.oct_status[i])):
                ret_val += self.oct_status[i][j].get_flash_tally()
        return ret_val

    # this displays a grid display of octopus energies
    def display(self):
        for line in self.oct_status:
            str_list = line
            for oct in str_list:
                print(oct.get_energy(), end='')
            print()

    # this is used when importing energy numbers into a row of octopuses
    # line is a string of single digit integers, representing energy
    def add_line(self, line):
        oct_line = []
        for digit in line:
            oct_line.append(OctopusStatus(int(digit)))
        self.oct_status.append(oct_line)

    # this function increases the energy of a
    # single octopus at coordinates (i,j)
    # returns zero if the increment didn't cause a flash
    # returns one if the increment caused a flash
    def increment_one_oct(self, i, j):
        # protect against (i,j) outside of the grid
        if True in [i<0, j<0, i>=len(self.oct_status), j>=len(self.oct_status[0])]:
            return 0

        # increment the octopus' energy
        self.oct_status[i][j].increment_energy()
        
        # detect if flash has just been triggered by this call
        if self.oct_status[i][j].get_flashed() == FlashStatus.JUST_FLASHED:
            return 1
        else:
            return 0

    # this function resets the energy to zero of any 
    # octopuses whose energy was greater than nine
    # (this is designed to be used at the end of a step)
    def reset_to_zero(self):
        for i in range(len(self.oct_status)):
            for j in range(len(self.oct_status[i])):
                if self.oct_status[i][j].get_energy() > 9:
                    self.oct_status[i][j].reset_energy()

    # this function increases the score of all
    # octopuses by one
    def increment_all_octs(self):
        for i in range(len(self.oct_status)):
            for j in range(len(self.oct_status[i])):
                self.increment_one_oct(i,j)

    # this function determines if flashes are necessary and then does them
    # if subsequent flashes become necessary after the first round, it triggers them too
    def flashes(self):
        while True:
            flash_count = 0
            # look for any octopuses that just flashed
            # if found, increment the adjacent octopuses
            for i in range(len(self.oct_status)):
                for j in range(len(self.oct_status[i])):
                    if self.oct_status[i][j].get_flashed() == FlashStatus.JUST_FLASHED:
                        self.oct_status[i][j].post_flashed()
                        flash_count += self.increment_one_oct(i-1,j-1)
                        flash_count += self.increment_one_oct(i-1,j)
                        flash_count += self.increment_one_oct(i-1,j+1)
                        flash_count += self.increment_one_oct(i,j-1)
                        flash_count += self.increment_one_oct(i,j+1)
                        flash_count += self.increment_one_oct(i+1,j-1)
                        flash_count += self.increment_one_oct(i+1,j)
                        flash_count += self.increment_one_oct(i+1,j+1)
            # stop repeating if no new flashes have happened
            if flash_count == 0:
                break

    # this function performs a single step (for parts a and b)
    # the return value (for part b only) is whether all octpuses are lit at this time
    # all other information passed to the calling program are embedded in the 
    # octopus' oct_status data structure
    def perform_step(self):
        ret_val = None
        self.increment_all_octs()
        self.flashes()
        ret_val = self.are_all_octopuses_flashing()
        self.reset_to_zero()
        return ret_val


# reading energy input from the input file
input_filename='input.txt'
octopus = Octopus()
with open(input_filename) as f:
    # pull in each line from the input file
    for in_string in f:
        octopus.add_line(in_string.rstrip())

# if desired, the initial state could be displayed
# print()
# print('Initial state:')
# octopus.display()

print()

# range parameter needs to be set high enough to deliver answers to a and b
for i in range(327):

    # this calls the code to perform the step
    # and it checks if all octopuses are lit up
    if octopus.perform_step():
        print('Step# ' + str(i+1) + ' has all octopuses illuminated')

    # add numbers to list for steps you wish to display
    # the step number and the whole grid of energies will be shown
    # you need to type in one less than the step number(s) to display in the list
    if i in [99, 323]:  
        print('After step # ' + str(i+1) + ', the number of flashes is ', end='')
        print(octopus.get_flash_tally())        
        print()

        octopus.display()
        print()
        print()

