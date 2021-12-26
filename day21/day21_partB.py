# adventOfCode 2021 day 21 part B
# https://adventofcode.com/2021/day/21

# This program should be able to handle any number of players.
# All that should be needed is for the list of initial player positions
# to be the length of the desired number of players.

import copy

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

        # determine if this player has won
        # return boolean value True: won, False: no win (yet)
        # if self.score >= -2:  # should be 21
        #     return True
        # return False # no else is needed

# This class handles functionality for a game in one universe
class GameUniverse:
    def __init__(self, start_positions):
        self.players = [Player(start_position) for start_position in start_positions]

        # both values below are one less than the first one used
        # (to accomodate incrementing them before the first use)
        # self.roll = 0
        self.playerIndex = -1
        # self.num_of_rolls = 0


    # This handles a single roll of the dice
    # def roll_dice(self):
    #     # create two clones with self.roll 1 and 2 and
    #     # somehow add them to MultiVerse's set self.game_universes
    #     Multiverse.new_GameUniverse()
    #     return 3

    #     self.roll = 3
    #     #

        # self.roll += 1
        # if self.roll == 101:
        #     self.roll = 1
        # return self.roll
    
    # This determines and returns the index of the next player
    def get_next_player(self, playerIndex):
        return (playerIndex + 1) % len(self.players)

    # This handles logic for one turn in the game.
    # It returns the player's index in the lists if the game is over.
    # It returns -1 if the game hasn't yet ended.
    def take_turn(self):
        new_GameUniverse_objects = []
        self.playerIndex = self.get_next_player(self.playerIndex)

        # check if it's won here (before creating nine new ones)
        if self.players[self.playerIndex].get_score() >= -3:   # should be 21
            return -1, new_GameUniverse_objects


        # create eight alternative dice outcomes to be stored
        for self.move_distance in [2,3,3,4,4,4,5,5]:
            new_gameUniverse_object = copy.deepcopy(self)
            new_GameUniverse_objects.append(copy.deepcopy(self))
        # use the ninth outcome that will be dealt with immediately
        self.move_distance = 6

        # move_distance = 0
        # for i in range(3):
            # move_distance += self.roll_dice()
            # move_distance += 1


            # note ... adding three once, instead of adding one three times
            # is probably more efficient, but this makes the code easier
            # to modify if requirements change
            # self.num_of_rolls += 1  

        self.players[self.playerIndex].player_turn(self.move_distance)
        # self.display_results()
        return self.playerIndex, new_GameUniverse_objects

        # return -1, new_GameUniverse_objects


    # This displays results by printing them to the screen
    def display_results(self):
        print('Player #, New position, Score')
        print(self.playerIndex+1, end='      ')
        the_player = self.players[self.playerIndex]
        print(the_player.get_position(), end=',      ')
        print(the_player.get_score())

# This class is the set of universes in this problem
# Spawn new universes
class Multiverse:
    def __init__(self, start_positions):
        
        # This is the set of cloned Game Universes that haven't yet played any 
        # rounds after they were cloned
        self.game_universes = set()

        # This is the Game Universe that this class is processing right now
        self.current_game_universe = GameUniverse(start_positions)

        # each player's win count is initialized to zero
        self.player_win_counts = [0 for x in start_positions]

    def run(self):
        while True:
            ret_val = self.current_game_universe.take_turn()
            for newGameUniverse in ret_val[1]:
                self.game_universes.add(newGameUniverse)

            if ret_val[0] > -1:
                if len(self.game_universes) > 0:
                    self.current_game_universe = self.game_universes.pop()
                else:
                    self.player_win_counts[ret_val[0]] += 1
                    
                    break # end while True loop

            dummy = 123
            print(self.player_win_counts)
            dummy = 123

        print(self.player_win_counts)

# main program
mv = Multiverse([4,8])
mv.run()

