# adventOfCode 2021 day 21 part B, 3rd attempt
# https://adventofcode.com/2021/day/21

import sys

# Note that number of players must equal the number of scores
class GameState:
    def __init__(self, game_state):
        # The dictionary's index is a tuple.
        #
        # The first element of the tuple is the number of the player
        # whose turn it is to go now.  This value starts at one.
        #
        # The rest of the values in the tuple are player positions,
        # followed by players' scores.  The positions are at indices
        # 1 through the number of players.  The scores are at indices
        # (1+self.NUM_PLAYERS) through (2*self.NUM_PLAYERS)
        #
        # The dict's value is the number of games in that state
        self.all_game_states = {game_state: 1}

        # This is the number of players
        self.NUM_PLAYERS = len(game_state)//2

        # This dict records the number of wins so far for each player
        self.wins = [0,0]

    # get a game_state with a value of at least one
    def get_next_game_state(self):
        for pair in self.all_game_states.items():
            # skip all game_states with a zero count
            if pair[1] == 0:
                continue
            
            # get this game_state, after dropping its count
            self.all_game_states[pair[0]] -= 1
            return pair[0]
        
        # If no games remain, then notify calling code
        return None

    def play(self):
        roll_list = [3,4,5,4,5,6,5,6,7,4,5,6,5,6,7,6,7,8,5,6,7,6,7,8,7,8,9]
        while True:
            game_state = self.get_next_game_state()
            if game_state is None:
                break

            player_number = game_state[0]

            for roll_total in roll_list:
                # move the player
                player_position = game_state[player_number] + roll_total
                if player_position % 10 == 0:
                    player_position = 10
                else:
                    player_position = player_position % 10

                # Calculate new score
                player_score = game_state[player_number + self.NUM_PLAYERS] + player_position

                # Handle a win
                if player_score >= 21: # >= 21
                    self.wins[player_number-1] += 1
                    break
            
                # Continue this game
                next_game_parameters = []

                # Get next player number
                next_player_number = player_number + 1
                if next_player_number > self.NUM_PLAYERS:
                    next_player_number = 1
                next_game_parameters.append(next_player_number)

                # Loop through all players
                for i_player_num in range(1, self.NUM_PLAYERS+1):
                    # For the player of this (ended turn), use calculated results
                    if i_player_num == player_number:
                        next_game_parameters.insert(i_player_num, player_position)
                        next_game_parameters.insert(i_player_num + self.NUM_PLAYERS, player_score)
                    # For any other player, repeat what was inputted to this turn
                    else:
                        next_game_parameters.insert(i_player_num, game_state[i_player_num])
                        next_game_parameters.insert(i_player_num + self.NUM_PLAYERS, game_state[i_player_num + self.NUM_PLAYERS])
                nextGameState = tuple(next_game_parameters)

                if nextGameState in self.all_game_states:
                    self.all_game_states[nextGameState] += 1
                else:
                    self.all_game_states[nextGameState] = 1

    def display_wins(self):
        for player_index in range(1, self.NUM_PLAYERS+1):
            print('Player# ', end='')
            print(player_index, end=' ')
            print('has ', end='')
            print(self.wins[player_index-1])

# Specify the original state of the game
game_state = GameState((1,4,8,0,0))
game_state.play()
game_state.display_wins()
