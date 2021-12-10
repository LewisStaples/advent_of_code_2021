# adventOfCode 2021 day 10
# https://adventofcode.com/2021/day/10

import sys
def part_a(str):
    char_stack = []
    char_pair = {
        '(':')',
        ')':'(',
        '[':']',
        ']':'[',
        '{':'}',
        '}':'{',
        '<':'>',
        '>':'<'
    }

    char_score = {
        ')':3,
        ']':57,
        '}':1197,
        '>':25137
    }

    for ch in str:
        if ch in ['(', '[', '{', '<']:
            char_stack.append(ch)
        elif char_stack[-1] == char_pair[ch]:
            char_stack.pop()
        elif ch in [')', ']', '}', '>']:
            # print('Expected ', end='')
            # print(char_pair[char_stack[-1]], end='')
            # print(', but found ', end='')
            # print(ch)
            return char_score[ch]
        else:
            # will handle this scenario better if it happens
            # I suspect that it won't happen at all
            sys.exit('Bad character: ' + ch)
    # print ('Remaining chars: ', end='')
    # print(char_stack)

    # incomplete
    return 0


# reading height input from the input file
input_filename='input.txt'
total_syntax_error_score = 0
with open(input_filename) as f:
    # pull in each line from the input file
    for in_string in f:
        in_string = in_string.rstrip()
        total_syntax_error_score += part_a(in_string)
        # print(in_string)
        # print(part_a(in_string))
        # print()

print()
print('The solution to part a is ', end='')
print(total_syntax_error_score)
print()
