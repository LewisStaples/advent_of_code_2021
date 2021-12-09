# adventOfCode 2021 day 8 part a
# https://adventofcode.com/2021/day/8

input_filename='input.txt'

# count appearances of 1, 4, 7, or 8  (char lengths: 2, 4, 3, 7)
unique_seg_digit_count = 0

with open(input_filename) as f:
    # pull in each line from the input file
    for in_string in f:
        [signal_pattern, output_value] = in_string.split(' | ')
        output_value = output_value.rstrip()
        for output_digit in output_value.split(' '):
            if len(output_digit) in [2,4,3,7]:
                unique_seg_digit_count += 1

print()
print('The answer to part a is ', end='')
print(unique_seg_digit_count)
