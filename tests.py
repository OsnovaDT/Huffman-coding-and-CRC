"""Module with tests"""

from unittest import TestCase, main as start_unittests

from huffman import (
    get_symbols_frequency, get_symbols_probability,
    get_probability_for_symbol, get_symbols_sorted_by_frequency
)


MESSAGE_1 = "aabbbbbbbbccccdeeeee"
MESSAGE_2 = "beep boop beer!"
MESSAGE_3 = "Communication systems with over-the-air-programming"

FREQUENCY_FOR_MESSAGE_1 = {
    'a': 2, 'b': 8, 'c': 4, 'd': 1, 'e': 5
}

FREQUENCY_FOR_MESSAGE_2 = {
    'b': 3, 'e': 4, 'p': 2, ' ': 2, 'o': 2, 'r': 1, '!': 1
}

FREQUENCY_FOR_MESSAGE_3 = {
    'C': 1, 'o': 4, 'm': 5, 'u': 1, 'n': 3, 'i': 5, 'c': 1,
    'a': 3, 't': 4, ' ': 3, 's': 3, 'y': 1, 'e': 3, 'w': 1,
    'h': 2, 'v': 1, 'r': 4, '-': 3, 'p': 1, 'g': 2
}

SORTED_FREQUENCY_FOR_MESSAGE_1 = {
    'b': 8, 'e': 5, 'c': 4, 'a': 2, 'd': 1
}

SORTED_FREQUENCY_FOR_MESSAGE_2 = {
    'e': 4, 'b': 3, 'p': 2, ' ': 2, 'o': 2, 'r': 1, '!': 1
}

SORTED_FREQUENCY_FOR_MESSAGE_3 = {
    'm': 5, 'i': 5, 'o': 4, 't': 4, 'r': 4, 'n': 3, 'a': 3, ' ': 3,
    's': 3, 'e': 3, '-': 3, 'h': 2, 'g': 2, 'C': 1, 'u': 1, 'c': 1,
    'y': 1, 'w': 1, 'v': 1, 'p': 1
}

EXPECTED_PROBABILITY_FOR_MESSAGE_1 = {
    'a': 0.1, 'b': 0.4, 'c': 0.2, 'd': 0.05, 'e': 0.25
}

EXPECTED_PROBABILITY_FOR_MESSAGE_2 = {
    'b': 0.2, 'e': 0.26667, 'p': 0.13333, ' ': 0.13333,
    'o': 0.13333, 'r': 0.06667, '!': 0.06667
}

EXPECTED_PROBABILITY_FOR_MESSAGE_3 = {
    'C': 0.01961, 'o': 0.07843, 'm': 0.09804, 'u': 0.01961,
    'n': 0.05882, 'i': 0.09804, 'c': 0.01961, 'a': 0.05882,
    't': 0.07843, ' ': 0.05882, 's': 0.05882, 'y': 0.01961,
    'e': 0.05882, 'w': 0.01961, 'h': 0.03922, 'v': 0.01961,
    'r': 0.07843, '-': 0.05882, 'p': 0.01961, 'g': 0.03922
}


class TestHuffmanCode(TestCase):
    """Class with tests for Huffman code"""

    def test_get_symbols_frequency(self):
        """Test get_symbols_frequency function"""

        self.assertEqual(
            get_symbols_frequency(MESSAGE_1), FREQUENCY_FOR_MESSAGE_1
        )
        self.assertEqual(
            get_symbols_frequency(MESSAGE_2), FREQUENCY_FOR_MESSAGE_2
        )
        self.assertEqual(
            get_symbols_frequency(MESSAGE_3), FREQUENCY_FOR_MESSAGE_3
        )

    def test_get_symbols_probability(self):
        """Test get_symbols_probability function"""

        self.assertEqual(
            get_symbols_probability(FREQUENCY_FOR_MESSAGE_1),
            EXPECTED_PROBABILITY_FOR_MESSAGE_1
        )
        self.assertEqual(
            get_symbols_probability(FREQUENCY_FOR_MESSAGE_2),
            EXPECTED_PROBABILITY_FOR_MESSAGE_2
        )
        self.assertEqual(
            get_symbols_probability(FREQUENCY_FOR_MESSAGE_3),
            EXPECTED_PROBABILITY_FOR_MESSAGE_3
        )

    def test_get_probability_for_symbol(self):
        """Test get_probability_for_symbol function"""

        self.assertEqual(
            get_probability_for_symbol(5, 40), 0.125
        )
        self.assertEqual(
            get_probability_for_symbol(2.5, 45), 0.05556
        )
        self.assertEqual(
            get_probability_for_symbol(10, 100), 0.1
        )

    def test_get_symbols_sorted_by_frequency(self):
        """Test get_symbols_sorted_by_frequency function"""

        self.assertEqual(
            get_symbols_sorted_by_frequency(FREQUENCY_FOR_MESSAGE_1),
            SORTED_FREQUENCY_FOR_MESSAGE_1
        )
        self.assertEqual(
            get_symbols_sorted_by_frequency(FREQUENCY_FOR_MESSAGE_2),
            SORTED_FREQUENCY_FOR_MESSAGE_2
        )
        self.assertEqual(
            get_symbols_sorted_by_frequency(FREQUENCY_FOR_MESSAGE_3),
            SORTED_FREQUENCY_FOR_MESSAGE_3
        )


if __name__ == '__main__':
    start_unittests()
