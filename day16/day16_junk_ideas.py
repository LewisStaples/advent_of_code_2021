# adventOfCode 2021 day 16
# https://adventofcode.com/2021/day/16

import sys

# writing code to understand what is being asked for

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

# start of main program
print()

# read hexadecimal input
input_filename='input_sample1.txt'
with open(input_filename) as f:
    input = f.readline().rstrip()

print('')
print('Reading input file:  ', end='')
print(input_filename)
print()

print('hex input:')    
print(input)
# print()

print('converted to binary:')
input = hex_to_binary(input)
print(input)
print()

print('packet version (binary, dec)')
print(input[:3], end=', ')
print(int(input[:3],2))
print()

print('packet type ID (binary, dec)')
print(input[3:6], end=', ')
print(int(input[3:6],2))
print()

if input[3:6] == '100':
    print('Type 4 ... literal value')
    sys.exit('Closing program')

# for all types other than 4 ....

print('length ID is ', end='')
print(input[7])
if input[7] == '0':
    print('next 15 bits are total length in bits of subpackets')
elif input[7] == '1':
    print('next 11 bits are number of subpackets')
    sys.exit('Closing program')

# for lengthID 0 ....
print('total length of subpackets in bits: ', end='')
print(input[8:22], end ='')
print(' and in decimal: ', end='')
print(int(input[8:22],2))
print()

print('first subpacket version is (bin): ', end='')
print(input[22:25], end=', (dec): ')
print(int(input[22:25],2))
print()

print('first subpacket typeID is (bin): ', end='')
print(input[25:28], end=', (dec): ')
print(int(input[25:28],2))
print()

