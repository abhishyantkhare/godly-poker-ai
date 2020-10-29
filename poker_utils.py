import pydealer
from pydealer.const import POKER_RANKS
from aenum import IntEnum
from collections import Counter

class PokerHands(IntEnum):
    HIGH_CARD = 0
    PAIR = 1
    TWO_PAIR = 2
    TRIPS = 3
    STRAIGHT = 4
    FLUSH = 5
    FULL_HOUSE = 6
    QUADS = 7
    STRAIGHT_FLUSH = 8
    ROYAL_FLUSH = 9

    def __str__(self):
        str_map = {
            PokerHands.HIGH_CARD: "High Card",
            PokerHands.PAIR: "Pair",
            PokerHands.TWO_PAIR: "Two Pair",
            PokerHands.TRIPS: "Trips",
            PokerHands.STRAIGHT: "Straight",
            PokerHands.FLUSH: "Flush",
            PokerHands.FULL_HOUSE: "Full House",
            PokerHands.QUADS: "Quads",
            PokerHands.STRAIGHT_FLUSH: "Straight Flush",
            PokerHands.ROYAL_FLUSH: "Royal Flush"
        }
        return str_map[self.value]

rank_values = POKER_RANKS['values']

def get_cards_value_sorted(cards):
    all_cards_value = [rank_values[card.value] for card in cards]
    all_cards_value.sort()
    return all_cards_value

def get_cards_suit(cards):
    all_cards_suit = [card.suit for card in cards]
    return all_cards_suit

def get_high_card(cards):
    return max(get_cards_value_sorted(cards)) + 1

def get_pair(cards):
    pair = 0
    all_cards_value = get_cards_value_sorted(cards)
    for i in range(len(all_cards_value) - 1):
        if all_cards_value[i] == all_cards_value[i + 1]:
            pair = all_cards_value[i] + 1
    return pair

# TODO: implement when two people get identical high two pair
def get_two_pair(cards):
    all_cards_value = get_cards_value_sorted(cards)
    if len(set(all_cards_value)) <= len(all_cards_value) - 2:
        return get_pair(cards) 
    return 0

def get_trips(cards):
    trips = 0
    all_cards_value = get_cards_value_sorted(cards)
    for i in range(len(all_cards_value) - 2):
        if all_cards_value[i] == all_cards_value[i + 1] and all_cards_value[i + 1] == all_cards_value[ i + 2]:
            trips = max(trips, all_cards_value[i]) + 1
    return trips 

def get_sub_straight(all_cards_value):
    if len(all_cards_value) < 5:
        return 0
    for i in range(len(all_cards_value) - 1):
        if (all_cards_value[i + 1] - all_cards_value[i]) != 1:
            return 0
    return all_cards_value[4] + 1

def get_straight(cards):
    all_cards_value = get_cards_value_sorted(cards) 
    straight_0_5 = get_sub_straight(all_cards_value[:4])
    straight_1_6 = get_sub_straight(all_cards_value[1:5])
    straight_2_7 = get_sub_straight(all_cards_value[2:6])
    return max(straight_0_5, straight_1_6, straight_2_7)

def get_flush(cards):
    card_suits = get_cards_suit(cards)
    suit_counter = Counter(card_suits)
    max_suit, num_count = suit_counter.most_common(1)[0]
    if num_count >= 5:
        suit_cards = [card for card in cards if card.suit == max_suit]
        return max(get_cards_value_sorted(suit_cards)) + 1
    return 0

def get_full_house(cards):
    pair = get_pair(cards)
    trips = get_trips(cards)
    if pair != 0 and trips != 0 and pair != trips:
        return max(pair, trips)
    return 0

def get_quads(cards):
    all_cards_value = get_cards_value_sorted(cards)
    value_counter = Counter(all_cards_value)
    quads, num_val = value_counter.most_common(1)[0]
    if num_val == 4:
        return quads + 1
    return 0

def get_straight_flush(cards):
    straight = get_straight(cards)
    if straight != 0:
        straight_cards = [card for card in cards if straight - rank_values[card.value] <=  4]
        return get_flush(straight_cards)
    return 0

def get_royal_flush(cards):
    straight_flush = get_straight_flush(cards)
    if straight_flush == 14:
        return 14
    return 0

def get_hand_value_list(cards):
    return [
        (PokerHands.HIGH_CARD, get_high_card(cards)), 
        (PokerHands.PAIR, get_pair(cards)),
        (PokerHands.TWO_PAIR, get_two_pair(cards)),
        (PokerHands.TRIPS, get_trips(cards)),
        (PokerHands.STRAIGHT, get_straight(cards)),
        (PokerHands.FLUSH, get_flush(cards)),
        (PokerHands.FULL_HOUSE, get_full_house(cards)),
        (PokerHands.QUADS, get_quads(cards)),
        (PokerHands.STRAIGHT_FLUSH, get_straight_flush(cards)),
        (PokerHands.ROYAL_FLUSH, get_royal_flush(cards))
    ]

def get_highest_hand(hand, board):
    hand_value_list = get_hand_value_list(hand + board)
    for i in range(len(hand_value_list) -1, -1, -1):
        if hand_value_list[i][1] != 0:
            return hand_value_list[i]

