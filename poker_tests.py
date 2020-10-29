import pytest
from pydealer import Card
import poker_utils
import aenum

def test_two_pair():

    testcases = [
        {
            'description': 'Test that we count two pair correctly',
            'cards': [
                Card('5', 'Clubs'),
                Card('6', 'Clubs'),
                Card('5', 'Hearts'),
                Card('Queen', 'Hearts'),
                Card('7', 'Diamonds'),
                Card('9', 'Clubs'),
                Card('Queen', 'Spades')
            ],
            'expected_two_pair_value': 12
        }
    ]
    for tc in testcases:
        two_pair_val = poker_utils.get_two_pair(tc['cards'])
        assert(two_pair_val == tc['expected_two_pair_value'])
