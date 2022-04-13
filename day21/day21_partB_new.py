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
        # for player1_space in range(1, 11):
        #     for player2_space in range(1, 11):
                this_roll_input = Roll_Input(player1_score, player2_score, player1_space, player2_space)
                player1_wins = 0
                player2_wins = 0
                for roll1 in range(1, 4):
                    player1_score_round = (player1_score + roll1)
                    player1_space_round = (player1_space + roll1) % 10

                    # print(roll1, end=': ')
                    if player1_score_round > 20:
                        player1_wins += 1
                    else:
                        for roll2 in range(1, 4):
                            player2_score_round = (player2_score + roll2)
                            player2_space_round = (player2_space + roll2) % 10
                            if player2_score_round > 20:
                                player2_wins += 1
                            else:
                                player2_wins += game_outcome_dict[Roll_Input(player1_score_round, player2_score_round,player1_space_round, player2_space_round)].FinalPlayerOneScore
                                player1_wins += game_outcome_dict[Roll_Input(player1_score_round, player2_score_round,player1_space_round, player2_space_round)].FinalPlayerTwoScore
                    game_outcome_dict[this_roll_input] = Roll_Output(player1_wins, player2_wins) # player one has won

dummy = 123


