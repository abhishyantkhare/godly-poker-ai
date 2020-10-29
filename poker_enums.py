from aenum import IntEnum

class PokerPosition(IntEnum):
    LB = 0
    BB = 1
    UTG = 2
    LJ = 3
    HJ = 4
    CO = 5
    BTN = 6

    def __str__(self):
        str_map = {
            PokerPosition.LB: "Little Blind",
            PokerPosition.BB: "Big Blind",
            PokerPosition.UTG: "Under The Gun",
            PokerPosition.LJ: "Lojack",
            PokerPosition.HJ: "Hijack",
            PokerPosition.CO: "Cutoff",
            PokerPosition.BTN: "Button"
        }
        return str_map[self.value]



class PokerAction(IntEnum):
    FOLD = 0
    CALL = 1
    RAISE = 2 # Check will be defined as a raise of 0
    
class PokerRoundStage(IntEnum):
    PREFLOP = 0
    FLOP = 1
    TURN = 2
    RIVER = 3