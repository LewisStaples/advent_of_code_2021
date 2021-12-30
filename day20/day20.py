# adventOfCode 2021 day ??
# https://adventofcode.com/2021/day/??

import copy

input_filename='input.txt'

# image is a list of lists of one-char strings
image = []

num_of_enhancements = 2

# This is a dict.  Index is a string of nine bits.
# Value is a one-char string for a
# light or dark pixel ('#' or '.')
image_enhancement_lookup_tbl = {}

def get_size():
    ret_val = 0
    for row in image:
        for pixel in row:
            if pixel == '#':
                ret_val += 1
    return ret_val

def display_image():
    for row in image:
        print(row)

def get_binary_string(image_old, row_num, pixel_num, enhancement_number):
    ret_val = ''
    for i in [row_num-1, row_num, row_num+1]:
        for j in [pixel_num-1, pixel_num, pixel_num+1]:
            
            if True in [i < 0, j < 0, i >= len(image_old), j >= len(image_old[0])]:
                if image_enhancement_lookup_tbl['000000000'] == '.':
                    ret_val += '0'
                    continue

                if enhancement_number%2 == 0:
                    ret_val += '0'
                else:
                    ret_val += '1'
                continue
            
            if image_old[i][j] == '#':
                ret_val += '1'
            else:
                ret_val += '0'
    return ret_val

def enhance_image(image, i):
    image_old = copy.deepcopy(image)
    for row_num in range(len(image_old)):
        row_new = []
        for pixel_num in range(len(image_old[0])):
            bin_str = get_binary_string(image_old, row_num, pixel_num, i)
            new_value = image_enhancement_lookup_tbl[bin_str]
            row_new.append(new_value)
        # remove the old version of this row, and then insert the new one
        image.pop(row_num)
        image.insert(row_num, row_new)

with open(input_filename) as f:
    # Input the image enhancement algorithm
    in_string = f.readline().rstrip()
    for i,ch in enumerate(in_string):
        str_bin = format(i, 'b').zfill(9)
        image_enhancement_lookup_tbl[str_bin] = ch

    # insert dummy lines at top of image (to be replaced later ...
    # when we know the length of each line from having read 
    # data from the file)
    for i in range(num_of_enhancements):
        image.append([])

    # Input each line from the input image
    for in_string in f:
        in_string = in_string.rstrip()
        if len(in_string) > 0:
            # input a line into the row
            row_list = [ch for ch in in_string]

            # pad the row with additional dark pixels
            for i in range(num_of_enhancements):
                row_list.insert(0, '.')
                row_list.append('.')

            # add the row to the image data structure
            image.append(row_list)
            row_length = len(row_list)

# Add additional rows (on top and below with dark pixels to 
# support enhancements)

row_list = ['.' for j in range(row_length)]
for i in range(num_of_enhancements):
    image.pop(i) # remove temporary empty rows from the top
    image.insert(i, row_list) # replace top empty rows with rows of dark pixels
    image.append(row_list) # add rows of dark pixels to the bottom

print()
print('Initial image:')
for i in range(num_of_enhancements):
    display_image()
    enhance_image(image, i)
    print()

print('Final image:')
display_image()

print()
print('Final Size: ')
print(get_size())
print()
