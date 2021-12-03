# adventOfCode 2021 day 3, parts 1 and 2
# https://adventofcode.com/2021/day/3

# Task 1:  Input Data, plus processing ...
input_filename='input.txt'
sum_list = []
gamma_rate_str = ''
epsilon_rate_str = ''

with open(input_filename) as f:
    for line_num, in_string in enumerate(f):
        # sum_list gets assigned all zeroes only once (before the first line's bits get included)
        if line_num == 0:
            sum_list = [0]*len(in_string.rstrip())
        # update sum_list to be a list of integers totalling bits from each line
        for char_num, ch in enumerate(in_string.rstrip()):
            # print(ch)
            sum_list[char_num] += int(ch)
        # print()

# print(sum_list)
# print(line_num)
# print()

# solve part a
for num in sum_list:
    # print(num/(line_num+1))
    if num/(line_num+1) > 0.5:
        gamma_rate_str += '1'
        epsilon_rate_str += '0'
    else:
        gamma_rate_str += '0'
        epsilon_rate_str += '1'
# print()
# print()
# print(gamma_rate_str)
# print(epsilon_rate_str)


print(int(gamma_rate_str,2))
print(int(epsilon_rate_str,2))

print('The solution to part a is ', end='')
print(int(gamma_rate_str,2)*int(epsilon_rate_str,2))
# Task 2:  Solve part a


