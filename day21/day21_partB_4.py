# adventOfCode 2021 day 21 part B,  attempt 4
# https://adventofcode.com/2021/day/21

roll_list = (3,4,5,4,5,6,5,6,7,4,5,6,5,6,7,6,7,8,5,6,7,6,7,8,7,8,9)

win_list = [0,0]
# wins_1 = 0
# wins_2 = 0

def play(this_position, other_position, this_score, other_score, player_flag):
    for roll in roll_list:
        position = this_position + roll
        if position > 10:
            position -= 10
        score = this_score + position
        if score >= 11:  # 21    # taking 20 seconds
        # if score < 20:   # taking 3 seconds
            if player_flag == 1:
                win_list[0] += 1
                # global wins_1
                # wins_1 += 1
            else:
                win_list[1] += 1
                # global wins_2
                # wins_2 += 1
        else:
            play(other_position, position, other_score, score, -1 * player_flag)

# initial_game_state = (4,8,0,0)
# play(initial_game_state, 1)

play(4, 8, 0, 0, 1)

print('Results:')
print(win_list)
# print(wins_1)
# print(wins_2)

