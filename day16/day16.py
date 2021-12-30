# adventOfCode 2021 day 16
# https://adventofcode.com/2021/day/16

import sys
import math
import operator

# This converts strings of binary to int values
def binary_to_decimal(in_string):
    return int(in_string, 2)

# This converts hex strings to binary strings
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


# This class has data and logic for packets.
class Packet:
    def __init__(self, in_string):
        self.binary_string = in_string
        self.version_total = 0

    # This function returns the version of this Packet
    def get_version(self):
        return binary_to_decimal(self.binary_string[0:3])

    # This function returns the typeID of this Packet
    def get_typeID(self):
        return binary_to_decimal(self.binary_string[3:6])

    # This function returns the typeID of this Packet
    def get_lengthID(self):
        if self.get_typeID() == 4:
            sys.exit('Type 4 packets do not have a lengthID ... exiting program')
        # since it isn't four:
        return int(self.binary_string[6])

    # This function gets the next bit group from a literal value packet
    # It returns a dict with:
    #      last_one: True/False if this is the end of the packet
    #      this_bit_group: a string with four char, these four bits
    #      char_index: the index of the character after this bit group
    def get_bit_group(self, char_index):
        ret_val = {}
        ret_val['last_one'] = False \
            if self.binary_string[char_index] == '1' else True
        ret_val['this_bit_group'] = \
            self.binary_string[char_index+1:char_index+5]
        ret_val['char_index'] = char_index + 5
        return ret_val

    # This is used on an operator packet.  It calls get_typeID to get
    # the packet's typeID, and then runs the function / operator 
    # associated with the operator packet.
    def get_value(self, values_list):
        func_dict = {
            0: sum,
            1: math.prod,
            2: min,
            3: max,
            5: operator.gt,
            6: operator.lt,
            7: operator.eq
        }

        # Handle functions called on single argument ... a full list
        if self.get_typeID() in [0,1,2,3]:
            return func_dict[self.get_typeID()](values_list)

        # Handle binary operators called on two arguments 
        # (list elements one and two)
        elif self.get_typeID() in [5,6,7]:
            return 1 if func_dict[self.get_typeID()] \
                (values_list[0], values_list[1]) else 0

    # This function parses the packet (including all subpackets).  
    # It returns a dictionary tuple with indices version_total, 
    # next_character, and value to the calling packet.
    def parse_packet(self):
        self.version_total = self.get_version()

        # Determine if this is a literal value packet
        if self.get_typeID() == 4:
            char_index = 6
            bit_string = ''

            # Loop through all bit groups within the literal value packet
            while True:
                ret_val = self.get_bit_group(char_index)
                char_index = ret_val['char_index']
                bit_string += ret_val['this_bit_group']
                if ret_val['last_one']:
                    break

            # Return dict with multiple values to the calling packet
            return {'version_total': self.version_total, \
                'next_character': char_index, \
                'value': binary_to_decimal(bit_string)}

        # The rest of function parse_packet() will parse operator packets 
        # (with 1 or more subpackets)
        values_list = []
        if self.get_lengthID() == 0:
            length_subpackets = binary_to_decimal(self.binary_string[7:22])
            char_index = 22
            end_of_subpackets = char_index + length_subpackets

            # Loop through each of this packet's subpackets
            while char_index < end_of_subpackets:
                # Make new substring starting with the start of this subpacket, 
                # and ending with the end of the last subpacket.
                new_string = self.binary_string[char_index:]
                # Make recursive call to parse this subpacket.
                ret_val = Packet(new_string).parse_packet()
                char_index += ret_val['next_character']
                self.version_total += ret_val['version_total']
                values_list.append(ret_val['value'])

        # Since length_type_ID is 1, bits 7 through 17 has the 
        # number of subpackets contained in this packet
        elif self.get_lengthID() == 1:
            num_of_subpackets = binary_to_decimal(self.binary_string[7:18])
            char_index = 18

            # Loop through each of this packet's subpackets
            for i in range(num_of_subpackets):
                # Make new substring starting with the start of this subpacket, 
                # and ending with the end of the last subpacket.
                new_string = self.binary_string[char_index:]
                # Make recursive call to parse this subpacket.
                ret_val = Packet(new_string).parse_packet()
                char_index += ret_val['next_character']
                self.version_total += ret_val['version_total']
                values_list.append(ret_val['value'])
        else:
            sys.exit('Bad lengthID ... it is not a bit ... closing program')

        # Return dict with multiple values to the calling packet
        return{'version_total':self.version_total, \
            'next_character': char_index, 'value': self.get_value(values_list)}
        
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

ret_val = Packet(in_string).parse_packet()

print('The answer to part a is: ', end='')
print(ret_val['version_total'])

print('The answer to part b is: ', end='')
print(ret_val['value'])

