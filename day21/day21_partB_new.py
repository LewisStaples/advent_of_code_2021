# adventOfCode 2021 day 21 part B
# https://adventofcode.com/2021/day/21

import sys
from collections import namedtuple
Roll_Input = namedtuple('Roll_Input', 'InitialPlayerOneScore InitialPlayerTwoScore PlayerOneSpace PlayerTwoSpace')
Roll_Output = namedtuple('Roll_Output', 'PlayerOneWinCount PlayerTwoWinCount')

def handle_space_overflow(space_in):
    space_out = space_in
    if space_in > 10:
        space_out -= 10
    return space_out

# for i in range(1,13):
#     print(i, end='   ')
#     print(handle_space_overflow(i))
# print()

# player1 is defined to be the player who has the next turn
# Any calls to a prior game_outcome_dict will reverse the players' identities
game_outcome_dict = dict()
# for player1_score in range(20, 19, -1):
#     for player2_score in range(20, 19, -1):
for player1_score in range(20, -1, -1):
    for player2_score in range(20, -1, -1):
        # for player1_space in range(1, 2):
        #     for player2_space in range(1, 2):
        for player1_space in range(1, 11):
            for player2_space in range(1, 11):
                this_roll_input = Roll_Input(player1_score, player2_score, player1_space, player2_space)
                player1_wins = 0
                player2_wins = 0
                for roll1 in range(1, 4):
                    for roll2 in range(1, 4):
                        for roll3 in range(1, 4):
                            player1_space_round = handle_space_overflow(player1_space + roll1 + roll2 + roll3)
                            player1_score_round = player1_score + player1_space_round

                            if player1_score_round > 20:
                                player1_wins += 1
                            else:
                                for roll4 in range(1, 4):
                                    for roll5 in range(1, 4):
                                        for roll6 in range(1, 4):
                                            player2_space_round = handle_space_overflow(player2_space + roll4 + roll5 + roll6)
                                            player2_score_round = player2_score + player2_space_round
                                            if player2_score_round > 20:
                                                player2_wins += 1
                                            else:
                                                try:
                                                    player2_wins += game_outcome_dict[Roll_Input(player1_score_round, player2_score_round, player1_space_round, player2_space_round)].PlayerTwoWinCount
                                                except KeyError:
                                                    print('Error!')
                                                    print(player1_score_round)
                                                    print(player2_score_round)
                                                    print(player1_space_round)
                                                    print(player2_space_round)
                                                    sys.exit('KeyError!')

                                                player1_wins += game_outcome_dict[Roll_Input(player1_score_round, player2_score_round,player1_space_round, player2_space_round)].PlayerOneWinCount
                            game_outcome_dict[this_roll_input] = Roll_Output(player1_wins, player2_wins) # player one has won

dummy = 123

print('Part B sample results are: ', end='')
try:
    print(game_outcome_dict[Roll_Input(InitialPlayerOneScore=0, \
    InitialPlayerTwoScore=0, \
    PlayerOneSpace=4, \
    PlayerTwoSpace=8)])
except Exception:
    sys.exit('\nError when attempting to print!')
