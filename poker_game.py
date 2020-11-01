import pydealer
from aenum import IntEnum
from pydealer.const import POKER_RANKS
import poker_utils
from poker_enums import PokerAction, PokerPosition, PokerRoundStage
from poker_player import PokerUserPlayer, PokerAIPlayer


class PokerRound:

    def __init__(self, ai_players, player, big_blind=20):
        self.ai_players = ai_players
        self.player = player
        self.deck = pydealer.Deck(ranks=POKER_RANKS)
        self.deck.shuffle()
        self.players_in_round = self.ai_players + [self.player]
        self.players_in_round = sorted(self.players_in_round, key=lambda x: x.position)
        self.min_to_call = big_blind
        self.min_to_raise = 0
        self.pot = 0
        self.board = []

    def get_deck_copy(self):
        return pydealer.Stack(self.deck.cards)

    def set_bets(self, stage):
        for player in self.players_in_round:
            player.set_stage_bet(stage)

    def deal(self):
        for ai in self.ai_players:
            hand = self.deck.deal(2)
            ai.set_hand(hand)
        player_hand = self.deck.deal(2)
        self.player.set_hand(player_hand)

    def play_round(self):
        self.deal()
        self.play_stage(PokerRoundStage.PREFLOP)
        self.extend_board(3)
        self.play_stage(PokerRoundStage.FLOP)
        self.extend_board(1)
        self.play_stage(PokerRoundStage.TURN)
        self.extend_board(1)
        self.play_stage(PokerRoundStage.RIVER)
        self.determine_winner()

    def get_start_ind(self, stage):
        if stage == PokerRoundStage.PREFLOP:
            return 2
        return 0

    def get_stage_initial_last_ind(self, stage):
        if stage == PokerRoundStage.PREFLOP:
            return 1
        return -1

    def calculate_pot(self):
        stage_bet_total = 0
        for player in self.players_in_round:
            stage_bet_total += player.get_bet()
            print(f"Bet for {player.name}: {player.get_bet()}")
        self.pot += stage_bet_total

    def play_stage(self, stage):
        self.set_bets(stage)
        folded_players = []
        player_ind = self.get_start_ind(stage)
        last_ind = self.get_stage_initial_last_ind(stage)
        last_player = self.get_player_at_ind(last_ind)
        self.min_to_raise = 0
        while(True):
            player = self.get_player_at_ind(player_ind)
            if player in folded_players:
                player_ind += 1
                continue
            player_action = player.play(stage, self.min_to_call, self.min_to_raise)
            if player_action == PokerAction.FOLD:
                folded_players.append(player)
            elif player_action != PokerAction.CALL:
                raise_amt = player_action[1]
                self.min_to_raise = raise_amt - self.min_to_call
                self.min_to_call = raise_amt
                last_player = self.get_player_at_ind(player_ind - 1)
            if player == last_player:
                break
            player_ind += 1

        self.players_in_round = [player for player in self.players_in_round
                                 if player not in folded_players]
        self.print_players()
        self.calculate_pot()
        print(f"The pot is: {self.pot}")

    def get_player_at_ind(self, i):
        return self.players_in_round[i % len(self.players_in_round)]

    def print_players(self):
        print("Players Left:")
        for player in self.players_in_round:
            print(player)

    def extend_board(self, amt):
        self.board.extend(self.deck.deal(amt))
        self.print_board()

    def print_player_hands(self):
        for player in self.players_in_round:
            print(f"{player.name} hands are:\n{player.hand}")
            print("\n")

    def print_board(self):
        print("The board is:\n")
        for card in self.board:
            print(card)
        print("\n")


    # TODO: implement ties & ties with kickers
    def determine_winner(self):
        self.print_board()
        self.print_player_hands()
        winning_player_idx, winning_hand, winning_value = PokerRound.determine_winner_helper([player.hand for player in self.players_in_round], self)
        print(f"The winning player is: {self.players_in_round[winning_player_idx]} with hand: {winning_hand}")
        print(f"Hand is: {player.hand}")
        self.print_board()

    def determine_winner_helper(hands, board):
        winning_player_idx = 0
        winning_hand, winning_value = poker_utils.get_highest_hand(hands[0], board)
        for i in range(len(hands)):
            player_hand, player_value = poker_utils.get_highest_hand(hands[i], board)
            if player_hand > winning_hand:
                winning_player_idx = i
                winning_hand, winning_value = player_hand, player_value
            if player_hand == winning_hand and player_value > winning_value:
                winning_player_idx = i
                winning_hand, winning_value = player_hand, player_value
        winning_hand = poker_utils.PokerHands(winning_hand)

        return winning_player_idx, winning_hand, winning_value

class PokerGame:

    def __init__(self, big_blind=20):
        self.num_ai = 6  # TODO: change this from being hardcoded
        self.set_initial_ai()
        self.player = PokerUserPlayer("Player", PokerPosition.BTN)
        self.big_blind = big_blind

    def set_initial_ai(self):
        pos = PokerPosition.LB
        self.ai_players = []
        for i in range(self.num_ai):
            self.ai_players.append(PokerAIPlayer(f"AI: {int(pos)}", pos))
            pos = PokerPosition(pos + 1)

    def play_round(self):
        round = PokerRound(self.ai_players, self.player, self.big_blind)
        round.play_round()

    def end_round(self):
        for ai_player in self.ai_players:
            ai_player.position = (ai_player.position + 1) % 7
        self.player.position = (self.player.position + 1) % 7

if __name__ == "__main__":

    game = PokerGame()
    print("Starting Poker Game: ...\n\n\n")

    game.play_round()
    game.end_round()
