# adventOfCode 2021 day 21
# https://adventofcode.com/2021/day/21

class Player:
    def __init__(self, start_position):
        self.position = start_position
        self.score = 0
    
    def get_position(self):
        return self.position
    
    def get_score(self):
        return self.score
    
    def process_roll(self, move_distance):
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
        if self.score >= 1000:
            return True
        return False # no else is needed
    
class Game:
    # Note that start_positions is a list of player starting positions
    # Players will only be identifiable by their index in this list
    # "Player 1" will be at index 0, "Player 2" will be at index 1,

    # (If part B increases the number of players then "Player 3" 
    # will be at index 2, and so on).  I'm guessing that that is the 
    # likely modification for part B.
    def __init__(self, start_positions):
        self.players = [Player(start_position) for start_position in start_positions]

        # both values below are one less than the first one used
        # (to accomodate incrementing them before the first use)
        self.roll = 0
        self.playerIndex = -1
        self.num_of_rolls = 0
    
    def roll_dice(self):
        self.roll += 1
        if self.roll == 101:
            self.roll = 1
        return self.roll
    
    def get_next_player(self, playerIndex):
        return (playerIndex + 1) % len(self.players)

    def print_submission(self, playerIndex):
        amount = self.num_of_rolls * \
            self.players[self.get_next_player(playerIndex)].get_score()
        print('The answer to part a is: ', end='')
        print(amount)

    def take_turn(self):
        self.playerIndex = self.get_next_player(self.playerIndex)
        move_distance = 0
        for i in range(3):
            move_distance += self.roll_dice()
            # note ... adding three once, instead of adding one three times
            # is probably more efficient, but this makes the code easier
            # to modify if requirements change
            self.num_of_rolls += 1  
        if self.players[self.playerIndex].process_roll(move_distance):
            self.print_submission(self.playerIndex)
            return True
        return False

    def display_results(self):
        print('Player #, New position, Score')
        print(self.playerIndex+1, end='      ')
        the_player = self.players[self.playerIndex]
        print(the_player.get_position(), end=',      ')
        print(the_player.get_score())
        
game = Game([4,8])
while True:
    if game.take_turn():
        break
