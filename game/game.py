from enum import Enum, auto
from player import Player

class GameType(Enum):
    HUNL = 'HUNL'

class Game:
    def __init__(self, player1: Player, player2: Player, sb: int=1, bb: int=2, starting_stack: int=200, game_type: GameType=GameType.HUNL):
        """
        Initialize the game with two players, blinds, starting stack, and game type.
        :param player1: Instance of Player class representing player 1.
        :param player2: Instance of Player class representing player 2.
        :param sb: Small Blind amount
        :param bb: Big Blind amount
        :param starting_stack: Starting stack in terms of Big Blinds
        :param game_type: Type of the game (default is Heads-Up No-Limit Hold'em).
        """
        # Type checking
        if not isinstance(player1, Player):
            raise TypeError(f"Expected player1 to be of type Player, got {type(player1).__name__} instead.")
        if not isinstance(player2, Player):
            raise TypeError(f"Expected player2 to be of type Player, got {type(player2).__name__} instead.")
        if not isinstance(sb, (int)):
            raise TypeError(f"Expected sb to be a number (int), got {type(sb).__name__} instead.")
        if not isinstance(bb, (int)):
            raise TypeError(f"Expected bb to be a number (int), got {type(bb).__name__} instead.")
        if not isinstance(starting_stack, (int)):
            raise TypeError(f"Expected starting_stack to be a number (int), got {type(starting_stack).__name__} instead.")
        if not isinstance(game_type, GameType):
            raise TypeError(f"Expected game_type to be of type GameType, got {type(game_type).__name__} instead.")

        self.player1 = player1
        self.player2 = player2
        self.sb = sb
        self.bb = bb
        self.starting_stack = starting_stack
        self.game_type = game_type
        
        # Set initial stacks
        self.player1.stack = self.starting_stack
        self.player2.stack = self.starting_stack

        # Determine who is SB and BB
        self.small_blind_player = player1
        self.big_blind_player = player2

        print(f"Game initialized: {player1} vs {player2}")
        print(f"Blinds: SB = {self.sb}, BB = {self.bb}")
        print(f"Starting stacks: {self.starting_stack} chips each")
        print(f"Game type: {self.game_type.name}")

    def start_hands(self):
        """
        Start playing hands in the game.
        """
        print(f"New hand started: {self.small_blind_player.name} is SB, {self.big_blind_player.name} is BB.")

        # Game logic to handle the hand can be added here
        while (self.player1.stack > 0 and self.player2.stack > 0):
            
            #TODO
            # play out a hand
            self.play_hand()

            # Swap blinds for next hand
            self.small_blind_player, self.big_blind_player = self.big_blind_player, self.small_blind_player

        # Determine the winner
        print("Game ended!")
        if self.player1.stack > 0:
            print(f"{self.player1.name} wins with {self.player1.stack} chips remaining!")
        else:
            print(f"{self.player2.name} wins with {self.player2.stack} chips remaining!")

