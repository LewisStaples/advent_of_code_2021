# adventOfCode 2021 day 21 part B
# https://adventofcode.com/2021/day/21

from collections import namedtuple
Roll_Input = namedtuple('Roll_Input', 'InitialPlayerOneScore InitialPlayerTwoScore PlayerOneSpace PlayerTwoSpace')
Roll_Output = namedtuple('Roll_Output', 'FinalPlayerOneScore FinalPlayerTwoScore')

# player1 is defined to be the player who has the next turn
# Any calls to a prior game_outcome_dict will reverse the players' identities
game_outcome_dict = dict()
for player1_score in range(20, 18, -1):
    for player2_score in range(20, 19, -1):
# for player1_score in range(20, -1, -1):
#     for player2_score in range(20, -1, -1):
        for player1_space in range(1, 2):
            for player2_space in range(1, 2):
                this_roll_input = Roll_Input(player1_score, player2_score, player1_space, player2_space)
        # for player1_space in range(1, 11):
        #     for player2_space in range(1, 11):
                for roll in range(1, 4):
                    player1_score_final = (player1_score + roll) % 10
                    player1_wins_final = 0
                    player2_wins_final = 0
                    print(roll, end=': ')
                    if player1_score+roll > 20:
                        player1_wins_final += 1
                    game_outcome_dict[this_roll_input] = Roll_Output(player1_wins_final, player2_wins_final) # player one has won

dummy = 123


