# adventOfCode 2021 day 25
# https://adventofcode.com/2021/day/25

class SeaCucumber:
    def __init__(self):
        # Lists to list east-bound and south-bound herds
        # Each will be a list of coordinates (each coordinate will be a list)
        self.east_herd = []
        self.south_herd = []
        
        # Reading input from the input file
        input_filename='input_sampleN.txt'
        with open(input_filename) as f:
            # Pull in each line from the input file
            for row_number, in_string in enumerate(f):
                in_string = in_string.rstrip()
                print(row_number, end=': ')
                print(in_string)

seaCucumber = SeaCucumber()
