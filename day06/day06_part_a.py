# adventOfCode 2021 day 6, part a only 
# https://adventofcode.com/2021/day/6

# this modifies each fishes' numeric value
def update(the_int):
    ret_val = the_int-1
    if ret_val<0:
        ret_val=6
    return ret_val

input_filename='input.txt'

with open(input_filename) as f:
    fish_list = [int(x) for x in f.readline().rstrip().split(',')]

# for each day
for day_number in range(1,81):

    # detect number of fish to add
    fish_to_add = fish_list.count(0)

    # update fish that are already there
    fish_list = [update(x) for x in fish_list]

    # now add the fish
    for dummy_variable in range(fish_to_add):
        fish_list.append(8)

print()
print('The answer to part a is:')
print('On day # ', end='')
print(day_number, end='')
print(' there are ', end='')
print(len(fish_list), end='')
print(' fish')