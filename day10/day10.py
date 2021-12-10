# adventOfCode 2021 day 10
# https://adventofcode.com/2021/day/10

import sys
import statistics

# this dict defines pairs of characters
# that go together 
# (i.e. opening and closing characters)
#
# this is used in both parts a and b
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

# this function calculates the score associated with illegal characters
# for a corrupted line 
# zero is returned for incomplete lines
# 
# this function is used in part a
def calc_illegal_score(in_string):
    # this list will contain the stack of opening characters
    char_stack = []

    # this lists the numeric score associated 
    # with each individual illegal character
    char_score = {
        ')':3,
        ']':57,
        '}':1197,
        '>':25137
    }

    # traverse the string, one character at a time
    for ch in in_string:
        # if the current character opens a group, add it to the stack
        if ch in ['(', '[', '{', '<']:
            char_stack.append(ch)
        
        # if the current character matches the most recent 
        # opening character on the stack, then remove that
        # most recent opening character from the stack
        elif char_stack[-1] == char_pair[ch]:
            char_stack.pop()
        
        # check if the current character is a closing character
        # if yes, then return the score associated with that
        # character
        elif ch in [')', ']', '}', '>']:
            return char_score[ch]
        
        # this will only be reached if the character is not any
        # of the opening or closing characters.
        # I would handle this scenario better if it happens
        # but it isn't happening with the data that we
        # have been given
        else:
            sys.exit('Bad character: ' + ch)

    # this happens if the string is incomplete
    # (which is handled by part b)
    return 0

# this function calculates the autocomplete score
# for an incomplete line
# zero is returned for corrupted lines
# 
# this function is used in part b
def calc_autocomplete_score(in_string):
    
    # this list will contain the stack of opening characters
    char_stack = []

    # this lists the numeric score associated 
    # with each opening character that remains
    # on the stack at the end (thus requiring completion)
    # (Note:  the specification lists scores by closing character,
    # but this program stores these numbers by the opening character)
    char_score = {
        '(':1,
        '[':2,
        '{':3,
        '<':4
    }

    # traverse the string, one character at a time
    for ch in in_string:
        # if the current character opens a group, add it to the stack
        if ch in ['(', '[', '{', '<']:
            char_stack.append(ch)
        
        # if the current character matches the most recent 
        # opening character on the stack, then remove that
        # most recent opening character from the stack
        elif char_stack[-1] == char_pair[ch]:
            char_stack.pop()
        
        # this will happen if there is corruption in the string
        else:
            # return zero, because this is not the scenario
            # that this function is testing for
            return 0

    # this happens if the string is incomplete
    # go through each character on char_stack, and add up the
    # sum of scores associated with each character
    # and then return it to end the function
    autocomplete_score = 0
    for i in range(len(char_stack)-1,-1,-1):
        autocomplete_score = autocomplete_score * 5 + char_score[char_stack[i]]
    return autocomplete_score


# this value is the answer to part a
total_syntax_error_score = 0

# this list of integers is the autocomplete score
# associated with each incomplete line
# this is used in part b
list_of_autocomplete_scores = []

# reading input from the input file
input_filename='input.txt'
with open(input_filename) as f:
    # pull in each line from the input file
    for in_string in f:
        in_string = in_string.rstrip()

        # calculate score for part a
        total_syntax_error_score += calc_illegal_score(in_string)

        # calculate score for part b
        # get each line's autocomplete score and put it in a list of integers
        list_of_autocomplete_scores.append(calc_autocomplete_score(in_string))

        # remove zeros from list_of_autocomplete_scores (zeros are for corrupted lines)
        list_of_autocomplete_scores = [x for x in list_of_autocomplete_scores if x != 0]

print()
print('The solution to part a is ', end='')
print(total_syntax_error_score)

print()
print('The solution to part b is ', end='')
# then get the median from the list of autocomplete scores
# (the specification line below is a definition of median
# "is found by sorting all of the scores and then taking the middle score")
print(statistics.median(list_of_autocomplete_scores))
print()

