from enum import Enum
from typing import List

class ActionType(Enum):
    ROOT = 'ROOT'
    FOLD = 'FOLD'
    CHECK = 'CHECK'
    BET = 'BET'
    CALL = 'CALL'
    RAISE = 'RAISE'

class Action:
    def __init__(self, action_type: ActionType, amount: int = 0):
        if not isinstance(action_type, ActionType):
            raise TypeError(f"Expected action_type to be of type ActionType, got {type(action_type).__name__} instead.")
        if not isinstance(amount, int):
            raise TypeError(f"Expected amount to be of type int, got {type(amount).__name__} instead.")
        
        self.action_type = action_type
        self.amount = amount

    def __str__(self):
        return f'{self.action_type} {self.amount}'

    def __repr__(self):
        return self.__str__()

class Player:
    def __init__(self, name: str):
        if not isinstance(name, str):
            raise TypeError(f"Expected name to be of type str, got {type(name).__name__} instead.")

        self.name = name
        self.hand = []
        self.stack = 0

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return self.__str__()
    
    def make_decision(self, preflop: bool, betting_history: List[Action]) -> Action: 
        raise NotImplementedError("This method should be overridden by subclasses")

class Human(Player):
    def make_decision(self, preflop: bool, betting_history: List[Action]) -> Action:
        # Logic for human decision-making

        if len(betting_history) < 1:
            raise ValueError("This function shouldn't be called yet, since root does not exist")
        
        # Define action lists for different scenarios
        fcr = [ActionType.FOLD, ActionType.CALL, ActionType.RAISE]
        fchr = [ActionType.FOLD, ActionType.CHECK, ActionType.RAISE]

        last_element = betting_history[-1]
        allowed = None

        if preflop:
            if last_element.action_type == ActionType.ROOT:
                allowed = fcr
            elif last_element.action_type == ActionType.CALL and len(betting_history) == 2:
                allowed = fchr
            elif last_element.action_type == ActionType.RAISE:
                allowed = fcr
        else:
            if last_element.action_type == ActionType.ROOT:
                allowed = fchr
            elif last_element.action_type == ActionType.BET:
                allowed = fcr
            elif last_element.action_type == ActionType.CHECK:
                allowed = fchr
            elif last_element.action_type == ActionType.RAISE:
                allowed = fcr

        if allowed is None:
            raise RuntimeError("Seems like make decision failed, one of the cases should have been hit")

        print(f"{self.name}, it's your turn.")
        
        # Generate options dynamically based on allowed actions
        options = {i + 1: action for i, action in enumerate(allowed)}
        options_display = [f"{key}) {action}" for key, action in options.items()]
        
        print(f"Options: {', '.join(options_display)}")
        
        choice = int(input("Enter the number corresponding to your choice: "))
        
        # TODO: check all in conditions as well as min raise rules
        if choice in options:
            selected_action = options[choice]
            if selected_action in [ActionType.BET, ActionType.RAISE]:
                amount = int(input(f"Enter the amount to {selected_action.name.lower()}: "))
                return Action(selected_action, amount)
            else:
                return Action(selected_action)
        else:
            print("Invalid choice. Try again.")
            return self.make_decision(preflop, betting_history)


        
class AI(Player):
    def make_decision(self, preflop: bool, betting_history: List[Action]) -> Action:
        # Logic for AI decision-making can be implemented here
        # For example, you could implement a simple rule-based AI or a more complex one
        print(f"{self.name} (AI) is making a decision...")
        # Placeholder AI logic (just calls every time)
        return Action(ActionType.CALL)

player3 = Player('p3')
player1 = Human('p1')
player2 = AI('p2')
print(player1, player2, player1.stack, player1.hand)
# player3.make_decision()