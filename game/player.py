from enum import Enum, auto

class PlayerType(Enum):
    HUMAN = 'HUMAN'
    AI = 'AI'

class Player:
    def __init__(self, player_type: PlayerType):
        if not isinstance(player_type, PlayerType):
            raise TypeError(f"Expected player_type to be of type PlayerType, got {type(player_type).__name__} instead.")
        self.player_type = player_type
        self.hand = []
        self.stack = 0

    def __str__(self):
        return f"({'Human' if self.player_type == PlayerType.HUMAN else 'AI'})"

    def __repr__(self):
        return self.__str__()

player1 = Player(PlayerType('HUMAN'))
player2 = Player(PlayerType('AI'))
print(player1, player2, player1.stack, player1.hand)