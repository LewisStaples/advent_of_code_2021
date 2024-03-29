# adventOfCode 2021 day 18
# https://adventofcode.com/2021/day/18

import sys
import math  # for floor, ceil, prod functions

# This class defines a snailfish number
class SnailfishNumber:
    def __init__(self, in_str):
        self.sfnum = in_str

    # This function displays the snailfish number as a string
    def display(self):
        print(self.sfnum)

    # This function adds this (self) snailfish number to
    # another snailfish number named other_sfnum.
    # Note that this does not automatically trigger reduction
    # (that needs to be done with a call to reduce)
    def add(self, other_sfnum):
        # Safety check: see if other_sfnum is not SnailfishNumber:
        if not isinstance(other_sfnum, SnailfishNumber):
            sys.exit('cannot add other objects to a S.F.Number')
        # This does the actual addition.
        self.sfnum = '[' + self.sfnum + ',' + other_sfnum.sfnum + ']'

    # This function explodes a pair that starts at index i
    # This assumes that the string starting at i will be
    # opening bracket, number 1, comma, number 2, closing bracket
    def do_explosion(self, i, j):
        # get numbers in the pair that will be exploded
        [n1, n2] = self.sfnum[i+1:j].split(',')
        [n1, n2] = [int(n1), int(n2)]

        # this defines the strings before and after the pair being exploded
        left_string = self.sfnum[:i]
        right_string = self.sfnum[j+1:]

        # seek last number in left_string (if found, add n1)
        for index_last in range(i-1,-1,-1):
            if left_string[index_last].isdigit():
                for index_first in range(index_last,-1,-1):
                    if not left_string[index_first].isdigit():
                        old_value = int(left_string[index_first+1:index_last+1])
                        left_string = left_string[0:index_first+1] + \
                        str(old_value + n1) + left_string[index_last+1:]
                        break # break out of inner for loop
                break # break out of outer for loop

        # seek first number in right string (if found add n2)
        for index_first in range(0,len(right_string)):
            if right_string[index_first].isdigit():
                for index_last in range(index_first,len(right_string)):
                    if not right_string[index_last].isdigit():
                        old_value = int(right_string[index_first:index_last])
                        right_string = right_string[0:index_first] + \
                        str(old_value + n2) + right_string[index_last:]
                        break
                break
        
        # assemble the pieces together
        self.sfnum = left_string + '0' + right_string
        # end of method do_explosion

    # This function looks if an explosion is needed
    # If one is needed, it calls do_explosion
    # It assumes that the pair to be exploded is 
    # opening bracket number 1, comma, number 2, closing bracket
    #
    # The return value indicates whether an explosion has occured.
    def seek_explosion(self):
        level = 0
        for i, ch in enumerate(self.sfnum):                
            if ch == '[':
                level += 1
                if level == 5:
                    j = self.sfnum.find(']', i)
                    self.do_explosion(i,j)
                    return True
            elif ch == ']':
                level -= 1
        return False

    # This function performs a split if needed.
    # It assumes that no numbers can have three or more digits.
    # 
    # The return value indicates whether a split has occured.
    def split(self):
        
        for i in range(len(self.sfnum)-1):
            # Search for a pair of adjacent digits
            if self.sfnum[i].isdigit() and self.sfnum[i+1].isdigit():
                # Pair of digits found .... fail hard if there is a third out there 
                # (the next char should either be a comma or a close bracket)
                if i+2 >= len(self.sfnum) or self.sfnum[i+2].isdigit():
                    sys.exit('bad char after two digit number!')

                # Since a pair of digits have been found, a split will occur
                # Determine the three pieces to assemble when the split is complete
                left_str = self.sfnum[:i]
                old_int = int(self.sfnum[i]+self.sfnum[i+1])
                mid_str = '[' + str(math.floor(old_int/2)) + ',' + str(math.ceil(old_int/2)) + ']'
                right_str = self.sfnum[i+2:]
                # Assemble the three strings together for the post-split status.
                self.sfnum = left_str + mid_str + right_str
                # Inform calling program that a split occured
                return True
        
        # Inform calling program that no split occured, since this
        # line can only be reached if there was no split.
        return False

    # This function reduces a Snailfish number by looping through 
    # explosions and splits until neither is needed anymore.
    def reduce(self):
        while True:
            if self.seek_explosion():
                continue # explosion occured, so repeat this function
            if self.split():
                continue # a split occured, so repeat this function
            return # finished reduction

    # This function computes the magnitude for a Snailfish number
    # 
    # Note that this assumes that the number has been reduced
    # (therefore all numbers are single digit integers)
    def get_magnitude(self):
        # this is the value to be returned (the magnitude)
        ret_val = 0
        # this is an ongoing list of multipliers
        multiplier_list = []

        for ch in self.sfnum:
            if ch == '[':
                multiplier_list.append(3)
            elif ch == ',':
                multiplier_list.pop()
                multiplier_list.append(2)
            elif ch == ']':
                multiplier_list.pop()
            elif ch.isdigit():
                ret_val += int(ch) * math.prod(multiplier_list)

        return ret_val

# end of definition of Class SnailfishNumber


# main program for part a

# reading input from the input file
input_filename='input.txt'
with open(input_filename) as f:
    # read the first line into a sf number
    n1 = SnailfishNumber(f.readline().rstrip())
    # read each subsequent line into sf numbers:
    for in_string in f:
        n2 = SnailfishNumber(in_string.rstrip())
        n1.add(n2)
        n1.reduce()
    f.close()

print('For part a:')
print('The final snailfish number is: ', end='')
n1.display()    
print('The magnitude of the final snailfish number is: ', end='')
print(n1.get_magnitude())
print()
print()


# main program for part b

list_of_sfnum_strings = []
list_of_magnitudes = []
with open(input_filename) as f:
    for in_string in f:
        list_of_sfnum_strings.append(in_string.rstrip())

for i in range(len(list_of_sfnum_strings)):
    for j in range(len(list_of_sfnum_strings)):
        if i != j:
            n1 = SnailfishNumber(list_of_sfnum_strings[i])
            n2 = SnailfishNumber(list_of_sfnum_strings[j])
            n1.add(n2)
            n1.reduce()
            list_of_magnitudes.append(n1.get_magnitude())

print('For part b:')
print('The magnitude of the largest snailfish number is: ', end='')
print(max(list_of_magnitudes))
print()
print()


