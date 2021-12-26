# adventOfCode 2021 day 21 part B, 2nd attempt
# https://adventofcode.com/2021/day/21

import copy

games_to_return_to = set() # set(GameUniverse([4,8]))
player_wins = [0,0]

class Player:
    # Initialize a player within a particular GameUniverse
    # This player doesn't know anything about any other players in this
    # or in any other universe.
    def __init__(self, start_position):
        self.position = start_position
        self.score = 0

    # Get the player's position
    def get_position(self):
        return self.position
    
    # Get the player's score
    def get_score(self):
        return self.score
    
    # This handles logic for a turn of this player
    def player_turn(self, move_distance):
        # calculate new position
        self.position = self.position + move_distance
        if self.position % 10 == 0:
            self.position = 10
        else:
            self.position = self.position % 10
        
        # calculate new score
        self.score += self.position

class GameUniverse:
    # This can be called using either of two types of other_param objects.
    #
    # If other_param is a list, then it must be a list of integers
    # that list the starting positions of the players.
    #
    # If other_param is a GameUniverse, then deepcopy it
    def __init__(self, other_param):
        # fill in the starting positions of the players

        # CHANGE THIS !!!!!!!!
        if isinstance(other_param, list):
            self.players = [Player(start_position) for start_position in other_param]

            # This value is one less than the first one used
            # (to accomodate incrementing it before the first use)
            self.playerIndex = -1

            self.move_distance = None
        
            dummy = 123
        # # if GameUniverse, deepcopy the object
        # elif isinstance(other_param, GameUniverse):
        #     self = copy.deepcopy(other_param)
        #     dummy = 123
        #     # return self

    # This increments the player index
    def get_next_player(self):
        self.playerIndex = (self.playerIndex + 1) % len(self.players)

    # This handles logic for one turn in the game.
    # It returns the player's index in the lists if the game is over.
    # It returns -1 if the game hasn't yet ended.
    def take_turn(self):
        # new_GameUniverse_objects = []
        self.get_next_player()

        # check if it's won here (before creating nine new ones)
        if self.players[self.playerIndex].get_score() >= 21:   # should be 21
            player_wins[self.playerIndex] += 1
            return True # stop taking turns

        if self.move_distance is None:
        # create eight alternative dice outcomes to be stored
            for local_move_distance in [2,3,3,4,4,4,5,5]:
                new_gameUniverse = copy.deepcopy(self)
                new_gameUniverse.move_distance = local_move_distance
                games_to_return_to.add(new_gameUniverse)

                dummy = 123

            # for self.move_distance in [2,3,3,4,4,4,5,5]:
                # games_to_return_to.add(self)

            # use the ninth outcome that will be dealt with immediately
            self.move_distance = 6

        self.players[self.playerIndex].player_turn(self.move_distance)
        self.move_distance = None
        return False # not yet finished

        # self.display_results()
        # return self.playerIndex, new_GameUniverse_objects
        # return -1, new_GameUniverse_objects

games_to_return_to.add(GameUniverse([4,8]))

while len(games_to_return_to) > 0:
    this_game = games_to_return_to.pop()
    while True:
        if this_game.take_turn():
            break

print(player_wins)
