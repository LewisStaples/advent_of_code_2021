# adventOfCode 2021 day 8 part b
# https://adventofcode.com/2021/day/8


# Below is an outline of my approach in English.
#
# I will sort the lettered code as I input it.  As per the problem statement of part b, 
# both fcadb and cdbaf are 3 .... these are the same group of letters that are ordered 
# differently.  Therefore, I believe that the sorting will be helpful 
# (it will allow tests of equality)

# Below is a table with information that can be used to recognize digits.  The first 
# four rows (already covered in part a) have four digits with unique numbers of segments 
# used.  The remainer have two groups of digits, where each group has the identical 
# number of segements but they can be distinguished by comparing with digits 1 and 4.
#
# num of segments  digit
#      2             1
#      3             7
#      4             4
#      7             8
#      5             2, 3, or 5
#          3 has two segments from 1, whereas 2 and 5 only have one segment
#          2 shares two segments in common with 4, wheras 5 shares three segments
#      6             0, 6, or 9
#          6 shares only one segment from 1, whereas 0 and 9 both share two
#          9 shares four segments with 4, whereas 0 shares three segments
# (end of approach outline)

input_filename='input.txt'
total_ans_b = 0

# class to handle mapping between strings and digits
class Stringcode_digit_mapping:
    # this looks up a digit from the dict
    def get_digit(self, stringcode):
        return self.string_to_digit[stringcode] 

    # this function counts the number of characters 
    # that are common between strings str1 and str2
    # and it returns the count as an integer
    # (both str1 and str2 are assumed not to have any characters repeat
    # more than once)
    def shared_segments(self,str1, str2):
        ret_val = 0
        for ch in str2:
            if ch in str1:
                ret_val += 1
        return ret_val

    def __init__(self, signal_plus_output_set):
        # dictionary with key strong from input and the resulting digit
        # this will be used for all 10 digits
        self.string_to_digit = {}

        # this is the reverse of the above dictionary
        # this will only be used for digits 1 and 4,
        # since those are the only ones that need to be looked up
        # (in the future I might seek out an alternative 
        # data structure that allows mapping in both directions)
        self.digit_to_string = {}

        five_segm_set = set()
        six_segm_set = set()
        for string in signal_plus_output_set:
            # if segment len is 2,3,4,or 7 ... it is now known,
            # because these four have unique 1-to-1 relationships
            if len(string) == 2:
                self.string_to_digit[string] = 1
                self.digit_to_string[1] = string
            elif len(string) == 3:
                self.string_to_digit[string] = 7
            elif len(string) == 4:
                self.string_to_digit[string] = 4
                self.digit_to_string[4] = string
            elif len(string) == 7:
                self.string_to_digit[string] = 8
            
            # if segment length is 5 or 6 ... set aside for 
            # after loop signal_plus_output_set is completed
            elif len(string) == 5:
                five_segm_set.add(string)
            elif len(string) == 6:
                six_segm_set.add(string)

        # now add mapping for digits with segment length 5
        for string in five_segm_set:
            if self.shared_segments(string, self.digit_to_string[1]) == 2:
                self.string_to_digit[string] = 3
            elif self.shared_segments(string, self.digit_to_string[4]) == 2:
                self.string_to_digit[string] = 2
            else:
                self.string_to_digit[string] = 5

        # now add mapping for digits with segment length 6
        for string in six_segm_set:
            if self.shared_segments(string, self.digit_to_string[1]) == 1:
                self.string_to_digit[string] = 6
            elif self.shared_segments(string, self.digit_to_string[4]) == 4:
                self.string_to_digit[string] = 9
            else:
                self.string_to_digit[string] = 0
    # end of __init__() definition
# end of class Stringcode_digit_mapping

with open(input_filename) as f:
    # pull in each line from the input file
    for in_string in f:
        # this is a set of strings in the combined signal plus output
        # (each string is sorted)
        signal_plus_output_set = set()

        # this will used to store the four strings from output
        # (each string here will be sorted alphabetically)
        output_value_sorted = []

        # split each input line by pipe char, and then rstrip both resulting strings
        [signal_pattern, output_value] = in_string.split(' | ')
        signal_pattern = signal_pattern.rstrip()
        output_value = output_value.rstrip()
        
        # split both input lines into further strings (10 before pipe, and 4 after the pipe)
        # the 10 before the pipe go into a set signal_plus_output_set for decoding
        # the 4 after the pipe also go into the set signal_plus_output_set
        # and the 4 after the pipe also get stored in list output_value_sorted
        for signal_digit in signal_pattern.split(' '):
            signal_plus_output_set.add(''.join(sorted(signal_digit)))
        for output_digit in output_value.split(' '):
            output_digit_sorted = ''.join(sorted(output_digit))
            signal_plus_output_set.add(output_digit_sorted)
            output_value_sorted.append(output_digit_sorted)

        # instantiate the class to handle mapping between strings and digits
        string_to_digit = Stringcode_digit_mapping(signal_plus_output_set)

        # decode the output for this particular line of input
        output_uncoded = ''
        for coded_output_digit in output_value_sorted:
            output_uncoded += str(string_to_digit.get_digit(coded_output_digit))

        # add the value from this line to the total (for the answer)
        total_ans_b += int(output_uncoded)

# outputting the answer
print('The answer to Day8 part b is ', end='')
print(total_ans_b)

