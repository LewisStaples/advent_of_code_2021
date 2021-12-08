# adventOfCode 2021 day 1, parts 1 and 2
# https://adventofcode.com/2021/day/1


# Task 1:  Input Data
input_filename='input.txt'
input_numbers = []

with open(input_filename) as f:
    for in_string in f:
        in_num = int(in_string)
        input_numbers.append(in_num)


# Task 2:  Solve part a
total_increases = 0


for i in range(len(input_numbers)-1):
    if input_numbers[i+1] > input_numbers[i]:
        total_increases += 1

print()
print('The answer to part a is:', end=' ')
print(total_increases)
print()


# Task 3:  Solve part b
total_increases = 0


for i in range(len(input_numbers)-3):
    # to evaluate if the latter "three-measurement sliding window" 
    # is larger than the prior, it is OK to only compare the prior's 
    # earliest member and the latter's latest member, because the other
    # members are in both windows, so their effects are cancelled out
    if input_numbers[i+3] > input_numbers[i]:
        total_increases += 1

print()
print('The answer to part b is:', end=' ')
print(total_increases)
print()


