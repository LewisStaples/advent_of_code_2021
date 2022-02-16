# adventOfCode 2021 day 24 helper 3
# https://adventofcode.com/2021/day/24

from random import randint

w = x = y = z = 0
integer_variables = {'w':0, 'x':0, 'y':0, 'z':0}
model_number = None
model_number_index = 0

# The specifications indicate that b could either be a value (such as 0) or a variable (such as w).
def get_b(b_string):
    # Assume that w,x,y,z are the only variables that it could be
    if b_string in ['w', 'x', 'y', 'z']:
        # return the value of the variable
        return integer_variables[b_string]

    # return the value itself, since it is not a variable.
    return int(b_string)

def get_a(a_string):
    return integer_variables[a_string]

def set_a(a_string, a_value_string):
    integer_variables[a_string] = a_value_string


def inp(param):
    global model_number_index
    global model_number
    integer_variables[param] = model_number[model_number_index]
    model_number_index += 1

def add(params):
    pass

def mul(params):
    var_str, mult_str = params.split(' ')   
    multiple = get_a(var_str) * get_b(mult_str)
    set_a(var_str, multiple)
    pass

def div(params):
    pass

def mod(params):
    pass

def eql(params):
    pass


for i in range(1):  # Number of random lists to try out   ... later use 10 or 20
    # ONE ... Randomly create a list of fourteen numbers between 1 and 9

    # model_number = [randint(0, 9) for x in range(14)]
    model_number = [2,7,11] # development / debug only


    # TWO ... See results (all z values) from running directly from input.txt

    input_filename='input_scenario0.txt'
    # Reading input from the input file
    with open(input_filename) as f:
        # Pull in each line from the input file
        for in_string in f:
            in_string = in_string.rstrip()
            print(in_string)

            instruction_line = in_string.split(' ',1)
            call_fxn = eval(instruction_line[0])
            call_fxn(instruction_line[1])

            dummy = 123

    # THREE ... See results (all z values) from the equations that I have written up

    # FOUR ... Compare those z results


