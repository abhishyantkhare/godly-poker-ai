import pydealer
import poker_game
from poker_game import PokerRound
from pydealer.const import POKER_RANKS

NUM_SAMPLES = int(1e4)

def sample_equity(deck, board, hands):

    wins = [0] * len(hands)
    for _ in range(NUM_SAMPLES):
        sample_deck = pydealer.Stack(cards=deck.cards, sort=False)
        sample_deck.shuffle()
        current_board = list(board)
        num_cards_to_deal = 5 - len(board)
        sample_board = sample_deck.deal(num_cards_to_deal) + current_board

        winning_player_idx, _, _ = PokerRound.determine_winner_helper(hands, sample_board)
        # print("==============")
        # print(hands[0])
        # print(hands[1])
        # print(sample_board)
        # print(winning_player_idx)
        wins[winning_player_idx] += 1

    print([float(win) / NUM_SAMPLES for win in wins])
    
if __name__ == "__main__":
    deck = pydealer.Deck(ranks=POKER_RANKS)
    deck.shuffle()
    player_1_hand = deck.deal(2)
    player_2_hand = deck.deal(2)

    board = [] #deck.deal(3)
    print("Player 1 hand:")
    print(player_1_hand)
    print("Player 2 hand:")
    print(player_2_hand)
    print("Board:")
    print(board)
    sample_equity(deck, board, [player_1_hand, player_2_hand])
