# adventOfCode 2021 day 1, part a
#
# this code was later refactored
# (day01.py, which handles parts a and b, is the final)
# this code uses less memory, because the input isn't stored,
# but the full program (parts a and b) would have been much 
# more complicated
#
# also this code mixes logic of reading data from the input file
# with the logic of determining the answer 

input_filename='input.txt'
prior_value = float("inf")
total_increases = 0

with open(input_filename) as f:
    for in_string in f:
        in_num = int(in_string)
        print(in_num)
        if in_num > prior_value:
            total_increases += 1
        prior_value = in_num

print('The answer to part a is:', end=' ')
print(total_increases)
