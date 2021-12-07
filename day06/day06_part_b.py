# adventOfCode 2021 day 6, new approach for part b
# https://adventofcode.com/2021/day/6

# new approach
# solve full problem for a single fish with age=0
# repeat for single fish for 1, 2, 3, 4, 5, 6
# gather the total fish at end for each of these seven scenarios
# then sum up these for each of the initial fish and that 
# should give the final answer


# this modifies each fishes' numeric value
def update(the_int):
    ret_val = the_int-1
    if ret_val<0:
        ret_val=6
    return ret_val

input_filename='input.txt'

# fish_list = None
fish_list__by_init = {}

# this function updates and returns the fish_list
def update_f_l(fish_list, start_day, end_day):
    # for each day
    for day_number in range(start_day, end_day+1):
        # detect number of fish to add
        fish_to_add = fish_list.count(0)
        
        # update fish that are already there
        fish_list = [update(x) for x in fish_list]

        # now add the fish
        for dummy_variable in range(fish_to_add):
            fish_list.append(8)
    return fish_list

# This code creates fish_list__by_init
# This is a dict with index 0 to 8, and with
# value the a list of fish that would result after 128 runs
for age in range(9):
    # print(age)
    # fish_list = [age]
    fish_list__by_init[age] = update_f_l([age], 1, 128)
    # print(age, end=': ')
    # print(fish_list__by_init[age])
print()
# print()

# read text file and write into fish_list, which is a list of integers
with open(input_filename) as f:
    fish_list = [int(x) for x in f.readline().rstrip().split(',')]
# print(len(fish_list))

# this uses fish_list__by_init to create a list
# showing what fish would be present after 128 days
new_list = []
for x in fish_list:
    for y in fish_list__by_init[x]:
        new_list.append(y)
fish_list = new_list

# to avoid overwhelming computer resources,
# this code traverses the list of fish present after 128 days
# and calculates, for each of those 128-day fish, how many fish
# descendents would be around at 256 days.
sum = 0
for fish in fish_list:
    # print(fish)
    sum += len(fish_list__by_init[fish])

# This displays the sum of fish at 256 days to the screen
# This is the answer to part b
print('The answer to part b is: ', end='')
print(sum)
