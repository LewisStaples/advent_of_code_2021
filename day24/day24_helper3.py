# adventOfCode 2021 day 24 helper 3
# https://adventofcode.com/2021/day/24

from random import randint

w = x = y = z = 0
integer_variables = {'w':0, 'x':0, 'y':0, 'z':0}
model_number = None
model_number_index = -1

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
    magic_number_dict = {4: -16, 5: -11, 6: -6, 9: -10, 10: -8, 11: -11, 13: -15}

    # evaluate_input()

    global model_number_index
    global model_number

    model_number_index += 1
    print('Before import # ', end='')
    print(model_number_index, end='')
    print(' the variables\' values are:', end='')
    print(integer_variables)
    # print()

    if model_number_index == len(model_number):
        return # None additional are needed

    
    # model_number_index += 1



    if model_number[model_number_index] == None:
        magic_number = magic_number_dict[model_number_index]
        model_number[model_number_index] = integer_variables['z'] % 26 + magic_number
        dummy = 123

    integer_variables[param] = model_number[model_number_index]

def add(params):
    par1, par2 = params.split(' ')   
    try:
        sum = get_a(par1) + get_b(par2)
    except TypeError:
        dummy = 123
    set_a(par1, sum)

def mul(params):
    par1, par2 = params.split(' ')   
    product = get_a(par1) * get_b(par2)
    set_a(par1, product)

def div(params):
    par1, par2 = params.split(' ')   
    quotient = get_a(par1) // get_b(par2)
    set_a(par1, quotient)

def mod(params):
    par1, par2 = params.split(' ')   
    result = get_a(par1) % get_b(par2)
    set_a(par1, result)

def eql(params):
    par1, par2 = params.split(' ')   
    if get_a(par1) == get_b(par2):
        set_a(par1, 1)
    else:
        set_a(par1, 0)

# def evaluate_input():
#     pass
#     # print('Need to implement input evaluation logic!  ', end='')
#     # print('And compare to using equations from notes.txt')

for i in range(1):  # Number of random lists to try out   ... later use 10 or 20
    # ONE ... Randomly create a list of fourteen numbers between 1 and 9

    # model_number = [randint(0, 9) for x in range(14)] # This is for the real program

    model_number = [None for x in range(14)] # This is for the real program
    for i in [0,1,2,3,7,8,12]:
        model_number[i] = randint(0, 9)

    # model_number = [3,9] # development / debug only

    # TWO ... See results (all z values) from running directly from input.txt

    input_filename='input.txt'
    # Reading input from the input file
    with open(input_filename) as f:
        # Pull in each line from the input file
        for in_string in f:
            in_string = in_string.rstrip()


            instruction_line = in_string.split(' ',1)
            call_fxn = eval(instruction_line[0])
            call_fxn(instruction_line[1])

            # evaluate_input()
            # print(in_string)

            dummy = 123

        dummy = 123
    print('final variable values: ', end='')
    print(integer_variables)
    print()

    # THREE ... See results (all z values) from the equations that I have written up
    # NEXT ....
        # (1) Replace i# with model_number elements
        # (1a) Maybe replace z# with something else .... need to think about this one
        # (2) Need to change model_number calculation to handle z# constraints ... should be done now

    z0 = model_number[0] + 5
    z1 = 26*z0 + model_number[1] + 14
    z2 = 26*z1 + model_number[2] + 15
    z3 = 26*z2 + model_number[3] + 16
    z4 = z3//26
    z5 = z4//26
    z6 = z5//26 
    z7 = 26*z6 + model_number[7] + 13
    z8 = 26*z7 + model_number[8] + 16
    z9 = z8//26
    z10 = z9//26
    z11 = z10//26
    z12 = 26*z11 + model_number[12] + 11
    z13 = z12//26

    for i in range(14):
        print('z' + str(i), end =': ')
        print(eval('z'+str(i)))

    # FOUR ... Compare those z results
    print()
    print('Input ... NOMAD digits')
    print(model_number)


