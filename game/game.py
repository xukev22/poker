from enum import Enum
from player import Player, Action, ActionType, Human, AI
from cards import Deck

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

        # FINAL FIELDS
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

        # init placeholders
        self.deck = None
        self.option = None
        self.pot = None
        self.preflop = None
        self.betting_history = None

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

    def play_hand(self):
        """
        Play out a single hand of poker according to standard No-Limit Texas Hold'em rules.
        """
        self.play_hand_init(2)

        if (self.play_hand_post_blinds()):
            print(f"Special case: action was done since stacks are less than blind reqs.")
            print(f"{self.pot} chips were in play")
            return
        else:
            print(f"Blinds posted: {self.small_blind_player.name} posts {self.sb}, {self.big_blind_player.name} posts {self.bb}")
            print(f"Pot is now {self.pot} chips")

        # inits
        self.preflop = True
        self.option = self.small_blind_player
        self.betting_history = [Action(ActionType.ROOT)]

        # start preflop betting round
        if (self.exec_betting_round()):
            self.runout()
            self.reward_winners()
        
        self.betting_history.append(Action(ActionType.ROOT))

        #TODO flop and beyond...

    # returns true if we go tor unout
    def exec_betting_round(self):
        while (not self.betting_done()):
            action = self.option.make_decision(self.preflop, self.betting_history)
            self.betting_history.append(action)

            penultimate_element = self.betting_history[-2]
            antepenultimate_element = self.betting_history[-3]

            # add to pot/decrease stacks if neccessary
            if (action.action_type == ActionType.CALL):
                if penultimate_element.action_type == ActionType.ROOT:
                    call_amt = self.bb - self.sb
                    self.update_pot_ps(call_amt)
                elif penultimate_element.action_type == ActionType.BET:
                    self.update_pot_ps(penultimate_element.amount)
                else: # calling a raise
                    # NOTE: RAISE means raise to that amount, not add on to the prev bet said amount
                    if antepenultimate_element.action_type == ActionType.CALL:
                        prev_amt = self.bb  
                    else:
                        prev_amt = antepenultimate_element.amount
                    call_amt = penultimate_element.amount - prev_amt
                    self.update_pot_ps(call_amt)
            elif (action.action_type == ActionType.BET):
                self.update_pot_ps(action.amount)
            elif (action.action_type == ActionType.RAISE):
                if penultimate_element.action_type == ActionType.CALL:
                    call_amt = action.amount - self.bb
                    self.update_pot_ps(call_amt)
                elif penultimate_element.action_type == ActionType.ROOT:
                    call_amt = action.amount - self.sb
                    self.update_pot_ps(call_amt)
                elif penultimate_element.action_type == ActionType.BET: 
                    self.update_pot_ps(action.amount)
                else: # raising a raise
                    if (antepenultimate_element.action_type == ActionType.ROOT) or (antepenultimate_element.action_type == ActionType.CALL): 
                        call_amt = action.amount - self.bb 
                        self.update_pot_ps(call_amt)
                    else: # should be a bet or raise, behave the same either way
                        call_amt = action.amount - antepenultimate_element.amount
                        self.update_pot_ps(call_amt)

        if self.player1.stack == 0 or self.player2.stack == 0:
            return True


    def update_pot_ps(self, call_amt):
        self.option.stack -= call_amt
        self.pot += call_amt


        # PLAN:

        # shuffle a new deck instance, deal cards
        # post blinds from each player

        # if noone is all in from blinds, proceed
            # if so, proceed to a runout with correct pot contributions, assume we can runout properly with the function runout()

        # place action on SB and wait for response (either manual from human or auto from ai) (they can call, fold, or raise)
        # once responded, place action on BB and act according to rules of poker
        # once action concludes for preflop, deal out 3 cards. 
            # if folded, ship pot to last player standing
            # if runout, proceed to runout with correct pot contributions

        # place action on BB for flop, perform same queries

        # place action on BB for turn, perform same queries

        # place action on BB for river, perform same queries
            # at this point we may need to see a showdown, where betting agressor must show first or muck

        # update stacks knowing who has won what, assume we can evaluate who won with the function find_winners()

    def play_hand_init(self, amount: int):
        if not isinstance(amount, int):
            raise TypeError(f"Expected amount to be of type int, got {type(amount).__name__} instead.")

        # Initialize a new deck and shuffle it
        self.deck = Deck()
        self.deck.shuffle()

        # Deal two cards to each player
        self.player1.hand = self.deck.deal(2)
        self.player2.hand = self.deck.deal(2)

        # Init pot and action history
        self.pot = 0
        self.action = None
    
    # returns true if the hand requires no further action (special case triggered)
    def play_hand_post_blinds(self):
        # SPECIAL CASES:

        # if either player under or equal to SB, we are flipping for the short stack
        # now both players must have more than SB.
        # if SBp <= BB, and BBp <= BB then we must decide to call off or not
        # if BBp <= BB, then we must decide to call off or not

        if (self.small_blind_player.stack <= self.sb or self.big_blind_player.stack <= self.sb):
            smaller_stack = min(self.small_blind_player.stack, self.big_blind_player.stack)
            self.pot += smaller_stack * 2
            self.small_blind_player.stack -= smaller_stack
            self.big_blind_player.stack -= smaller_stack

            self.runout()
            self.reward_winners()
            return True
        elif (self.small_blind_player.stack <= self.bb and self.big_blind_player.stack <= self.bb) or (self.big_blind_player.stack <= self.bb):
            smaller_stack = min(self.small_blind_player.stack, self.big_blind_player.stack)
            if self.small_blind_player.prompt_calloff(self.small_blind_player.stack - smaller_stack):
                self.pot += smaller_stack * 2
                self.big_blind_player.stack -= smaller_stack
                self.small_blind_player -= smaller_stack

                self.runout()
                self.reward_winners()
            else:
                self.small_blind_player -= self.sb
                self.big_blind_player += self.sb
            return True

    # returns true if betting is done based on the betting history
    def betting_done(self):

        # betting is done when you see F, or a C that isnt first in list, or checks around
        if self.betting_history.__len__ < 1:
            raise ValueError("This function shouldn't be called yet, since root does not exist")
        
        last_element = self.betting_history[-1]
        penultimate_element = self.betting_history[-2]

        if last_element.action_type == ActionType.FOLD:
            return True
        if last_element.action_type == ActionType.CALL and self.betting_history.__len__ > 2:
            return True
        if last_element.action_type == ActionType.CHECK and penultimate_element.action_type == ActionType.CHECK:
            return True
        
        return False

game = Game(Human('p1'), AI('p2'))
game.start_hands()

