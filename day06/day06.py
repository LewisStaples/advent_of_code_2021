# adventOfCode 2021 day 5, parts 1 and 2
# https://adventofcode.com/2021/day/5

# display output to match the problem statement
def print_special(fish_list):
    for i, fish in enumerate(fish_list):
        print(fish, end='')
        if i < len(fish_list)-1:
            print(',', end='')
    print()

def update(the_int):
    ret_val = the_int-1
    if ret_val<0:
        ret_val=6
    return ret_val

input_filename='input.txt'

with open(input_filename) as f:
    fish_list = [int(x) for x in f.readline().rstrip().split(',')]

# print('Initial state: ', end='')
# print_special(fish_list)

for day_number in range(1,81):

    # detect number of fish to add
    fish_to_add = fish_list.count(0)

    # update fish that are already there
    fish_list = [update(x) for x in fish_list]

    # now add the fish
    for dummy_variable in range(fish_to_add):
        fish_list.append(8)

    # display fish that are now there
    # print('After', end='')
    # print('{:3d}'.format(day_number), end='')
    # print(' days: ', end='')
    # print_special(fish_list)

    # # add fish, if appropriate
    # print(fish_list.count(6))
    
print()
print('On day # ', end='')
print(day_number, end='')
print(' there are ', end='')
print(len(fish_list), end='')
print(' fish')