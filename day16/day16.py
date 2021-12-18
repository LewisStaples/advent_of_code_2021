# adventOfCode 2021 day 16
# https://adventofcode.com/2021/day/16

import sys

def binary_to_decimal(in_string):
    return int(in_string, 2)

def hex_to_binary(in_string):
    char_dict = {}
    char_dict['0'] = '0000'
    char_dict['1'] = '0001'
    char_dict['2'] = '0010'
    char_dict['3'] = '0011'
    char_dict['4'] = '0100'
    char_dict['5'] = '0101'
    char_dict['6'] = '0110'
    char_dict['7'] = '0111'
    char_dict['8'] = '1000'
    char_dict['9'] = '1001'
    char_dict['A'] = '1010'
    char_dict['B'] = '1011'
    char_dict['C'] = '1100'
    char_dict['D'] = '1101'
    char_dict['E'] = '1110'
    char_dict['F'] = '1111'

    ret_val = ''
    for i in range(len(in_string)):
        ret_val += char_dict[in_string[i]]
    return ret_val
# END OF def hex_to_binary(in_string):


class Packet:
    def __init__(self, in_string):
        # print('hex input string: ', end='')
        # print(hex_string)

        # self.binary_string = hex_to_binary(hex_string)
        # print('binary string: ', end='')
        # print(self.binary_string)

        self.binary_string = in_string
        self.version_total = 0

    # this function returns the version of this  ((binary string))
    def get_version(self):
        return binary_to_decimal(self.binary_string[0:3])

    # this function returns the typeID of this packet
    def get_typeID(self):
        return binary_to_decimal(self.binary_string[3:6])

    def get_lengthID(self):
        if self.get_typeID() == 4:
            sys.exit('Type 4 packets do not have a lengthID ... exiting program')
        # since it isn't four:
        return int(self.binary_string[6])


    # this function gets the next bit group of within a literal value packet
    # it returns a dict with:
    #      last_one: True/False if this is the end of the packet
    #      this_bit_group: a string with four char, these four bits
    #      char_index: the index of the character after this bit group
    def get_bit_group(self, char_index):
        ret_val = {}
        ret_val['last_one'] = False if self.binary_string[char_index] == '1' else True
        ret_val['this_bit_group'] = self.binary_string[char_index+1:char_index+5]
        ret_val['char_index'] = char_index + 5
        return ret_val

    # this function parses the packet (including all subpackets),
    # ??? or string of packets
    # to calculate the sum of all versions

    # parsing a packet
    # determine if it is a literal value packet .... if yes, do (what's already known)
    # otherwise it is an operator packet
    # if length_type_ID is 0, you can chop off the trailing zeroes
    # if length_type_ID is 1, you know the number of packets
    # send it to a magic function that reads the values and splits them
    # 	either condition above will guide it in knowing when to stop
    # then use recursion on it
    def parse_version(self):
        self.version_total = self.get_version()

        if self.get_typeID() == 4:
            # type 4 packets (literal value packets) have no subpackets, 
            # so self.version_total won't be changed in here

            char_index = 6
            bit_string = ''

            # loop through all bit groups within the literal value packet
            while True:
                ret_val = self.get_bit_group(char_index)
                char_index = ret_val['char_index']
                bit_string += ret_val['this_bit_group']
                if ret_val['last_one']:
                    break

            # return tuple with multiple values to the calling packet
            return {'version_total': self.version_total, \
                'next_character': char_index, \
                'literal_value': binary_to_decimal(bit_string)}

        # this code is only for for operator packets (with 1 or more
        # subpackets)

        if self.get_lengthID() == 0:
            length_subpackets = binary_to_decimal(self.binary_string[7:22])
            char_index = 22
            end_of_subpackets = char_index + length_subpackets
            # make loop ...
            while char_index < end_of_subpackets:
                # make new substring for recursive call (binary)
                new_string = self.binary_string[char_index:]
                # make recursive call (probably more than once)
                ret_val = Packet(new_string).parse_version()
                char_index += ret_val['next_character']
                self.version_total += ret_val['version_total']
            dummy = 123

        elif self.get_lengthID() == 1:
            num_of_subpackets = binary_to_decimal(self.binary_string[7:18])
            char_index = 18
            # for loop making that number of recursive 
            for i in range(num_of_subpackets):
                # make new substring for recursive call (binary)
                new_string = self.binary_string[char_index:]
                # make recursive call (probably more than once)
                ret_val = Packet(new_string).parse_version()
                char_index += ret_val['next_character']
                self.version_total += ret_val['version_total']
        else:
            sys.exit('Bad lengthID ... it is not a bit ... closing program')

        return{'version_total':self.version_total, 'next_character': char_index}
        
# start of main program
print()

# read hexadecimal input
input_filename='input.txt'
with open(input_filename) as f:
    in_string = f.readline().rstrip()

print('Reading input file:  ', end='')
print(input_filename)
print()

if len(in_string) < 20:
    print('Hex input string: ', end='')
    print(in_string)

in_string = hex_to_binary(in_string)

if len(in_string) < 100:
    print('input string converted to binary: ', end='')
    print(in_string)

ret_val = Packet(in_string).parse_version()

print('The answer is: ', end='')
print(ret_val['version_total'])
