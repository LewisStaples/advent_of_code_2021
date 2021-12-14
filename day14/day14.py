# adventOfCode 2021 day ??
# https://adventofcode.com/2021/day/??

# this function determines the string length after 10 steps
# I do this, because I want to know if the length will be
# longer than what my computer can handle
def display_length_results(length):
    print('initial length:           ', end='')
    print(length)
    for i in range(1,11):
        length += (length-1)
        print('length after step  ', end='')
        print(i, end=': ')
        print(length)

# reading input from the input file
input_filename='input_sample0.txt'
with open(input_filename) as f:
    in_string = f.readline().rstrip()
    display_length_results(len(in_string))

    # # pull in each line from the input file
    # for in_string in f:
    #     print(in_string.rstrip())

