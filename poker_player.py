from poker_enums import PokerPosition, PokerRoundStage, PokerAction

class PokerPlayer:

    def __init__(self, name, position:PokerPosition, big_blind=20):
        self.hand = None
        self.position = position
        self.name = name
        self.big_blind = big_blind
        
    def set_stage_bet(self, stage):
        if stage == PokerRoundStage.PREFLOP:
            if self.position == PokerPosition.LB:
                self.bet = self.big_blind / 2
            if self.position == PokerPosition.BB:
                self.bet = self.big_blind
        self.bet = 0

    def get_bet(self):
        return self.bet

    def set_hand(self, hand):
        self.hand = hand

    def get_max_bet(self, stage):
        return (stage + 1)*60
 

    def play(self, stage, min_to_call, min_to_raise):
        print(f"{self.name} is playing as {self.position}")
        if self.position == PokerPosition.UTG:
            print(f"{self.name} FOLDED")    
            return PokerAction.FOLD
        if self.bet < self.get_max_bet(stage) and (self.position == PokerPosition.HJ or self.position == PokerPosition.BB):
            self.bet = min_to_call + 20
            print(f"{self.name} is RAISING: {self.bet}")
            return PokerAction.RAISE, self.bet
        print(f"{self.name} is CALLING: {min_to_call}")
        self.bet = min_to_call
        return PokerAction.CALL
            

    def __str__(self):
        return self.name

        

class PokerAIPlayer(PokerPlayer):

    def __init__(self, name, position:PokerPosition, big_blind=20):
        super().__init__(name, position, big_blind)

class PokerUserPlayer(PokerPlayer):

    def __init__(self, name, position:PokerPosition, big_blind=20):
        super().__init__(name, position, big_blind)

    def validate_raise_amt(self, amt, min_to_call, min_to_raise):
        if not amt.isdigit():
            return "Invalid. Please enter a positive integer. Avoid using decimals such as 10.0"
        amt = int(amt)
        if amt < (min_to_call + min_to_raise):
            return "Invalid. Please raise by at least as much as the previous raise."
        return None
    
    def play(self, stage, min_to_call, min_to_raise):
        print(f"You are playing as: {self.position}")
        print(f"Min To Call: {min_to_call}")
        print(f"Hand is: {self.hand}")
        action = input("Enter f to fold, c to call, or r to raise:\n")
        while action not in {'f', 'c', 'r'}:
            print("Invalid input. Please try again")
            action = input("Enter f to fold, c to call, or r to raise:\n")
        if action == "f":
            return PokerAction.FOLD
        if action == "c":
            return PokerAction.CALL
        if action == "r":
            amt = input("Enter a positive integer amount to set the new bet:\n")
            invalid_err = self.validate_raise_amt(amt, min_to_call, min_to_raise)
            while invalid_err:
                print(invalid_err)
                amt = input("Enter a positive integer amount to set the new bet:\n")
                invalid_err = self.validate_raise_amt(amt, min_to_call, min_to_raise)

            return PokerAction.RAISE, int(amt)
    