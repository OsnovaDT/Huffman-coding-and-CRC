"""Module with tests"""

from random import randint

from unittest import TestCase

from huffman import (
    get_symbols_with_frequency, get_symbols_with_probability,
    get_probability_for_symbol, get_sorted_symbols_with_frequency,
    is_tree, get_huffman_code_tree
)

# Data for testing

# Message
MESSAGE_1 = "aabbbbbbbbccccdeeeee"

MESSAGE_2 = "beep boop beer!"

MESSAGE_3 = "Communication systems with over-the-air-programming"

MESSAGE_4 = ''

MESSAGE_5 = 'ab'

# Frequency
EXPECTED_FREQUENCY_FOR_MESSAGE_1 = {
    'a': 2, 'b': 8, 'c': 4, 'd': 1, 'e': 5
}

EXPECTED_FREQUENCY_FOR_MESSAGE_2 = {
    'b': 3, 'e': 4, 'p': 2, ' ': 2, 'o': 2, 'r': 1, '!': 1
}

EXPECTED_FREQUENCY_FOR_MESSAGE_3 = {
    'C': 1, 'o': 4, 'm': 5, 'u': 1, 'n': 3, 'i': 5, 'c': 1,
    'a': 3, 't': 4, ' ': 3, 's': 3, 'y': 1, 'e': 3, 'w': 1,
    'h': 2, 'v': 1, 'r': 4, '-': 3, 'p': 1, 'g': 2
}

EXPECTED_FREQUENCY_FOR_MESSAGE_4 = {}

EXPECTED_FREQUENCY_FOR_MESSAGE_5 = {'a': 1, 'b': 1}

# Sorted frequency
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

SORTED_FREQUENCY_FOR_MESSAGE_4 = {}

SORTED_FREQUENCY_FOR_MESSAGE_5 = {'a': 1, 'b': 1}

# Probability
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

EXPECTED_PROBABILITY_FOR_MESSAGE_4 = {}

EXPECTED_PROBABILITY_FOR_MESSAGE_5 = {'a': 0.5, 'b': 0.5}

# Code tree

EXPECTED_CODE_TREE_FOR_MESSAGE_1 = [(('d', ('c', 'a')), ('b', 'e'))]

EXPECTED_CODE_TREE_FOR_MESSAGE_2 = [(('e', 'b'), (('!', ('o', 'r')), ('p', ' ')))]

EXPECTED_CODE_TREE_FOR_MESSAGE_3 = [
    ((('m', 'i'), (('-', 'h'), ('s', 'e'))),
    ((('a', ' '), ('r', 'n')), (('o', 't'),
    ((('v', 'p'), ('y', 'w')), (('u', 'c'), ('g', 'C'))))))
]

EXPECTED_CODE_TREE_FOR_MESSAGE_4 = []

EXPECTED_CODE_TREE_FOR_MESSAGE_5 = [('a', 'b')]

# Data for testing get_symbols_with_frequency function
MESSAGE_AND_FREQUENCY = {
    MESSAGE_1: EXPECTED_FREQUENCY_FOR_MESSAGE_1,
    MESSAGE_2: EXPECTED_FREQUENCY_FOR_MESSAGE_2,
    MESSAGE_3: EXPECTED_FREQUENCY_FOR_MESSAGE_3,
    MESSAGE_4: EXPECTED_FREQUENCY_FOR_MESSAGE_4,
    MESSAGE_5: EXPECTED_FREQUENCY_FOR_MESSAGE_5,
}

# Data for testing get_symbols_with_probability function
FREQUENCY_AND_PROBABILITY = (
    (EXPECTED_FREQUENCY_FOR_MESSAGE_1, EXPECTED_PROBABILITY_FOR_MESSAGE_1),
    (EXPECTED_FREQUENCY_FOR_MESSAGE_3, EXPECTED_PROBABILITY_FOR_MESSAGE_3),
    (EXPECTED_FREQUENCY_FOR_MESSAGE_2, EXPECTED_PROBABILITY_FOR_MESSAGE_2),
    (EXPECTED_FREQUENCY_FOR_MESSAGE_4, EXPECTED_PROBABILITY_FOR_MESSAGE_4),
    (EXPECTED_FREQUENCY_FOR_MESSAGE_5, EXPECTED_PROBABILITY_FOR_MESSAGE_5),
)

# Data for testing get_sorted_symbols_with_frequency function
FREQUENCY_AND_SORTED_FREQUENCY = (
    (EXPECTED_FREQUENCY_FOR_MESSAGE_1, SORTED_FREQUENCY_FOR_MESSAGE_1),
    (EXPECTED_FREQUENCY_FOR_MESSAGE_2, SORTED_FREQUENCY_FOR_MESSAGE_2),
    (EXPECTED_FREQUENCY_FOR_MESSAGE_3, SORTED_FREQUENCY_FOR_MESSAGE_3),
    (EXPECTED_FREQUENCY_FOR_MESSAGE_4, SORTED_FREQUENCY_FOR_MESSAGE_4),
    (EXPECTED_FREQUENCY_FOR_MESSAGE_5, SORTED_FREQUENCY_FOR_MESSAGE_5),
)

# Data for testing is_tree function
OBJECTS_TREES = ((1, 2, 3), (1,), ('string1', 'string2'))

OBJECTS_ARE_NOT_TREES = (1, [1, 2, 3], 'string', None, 0)

# Data for testing get_huffman_code_tree function
FREQUENCY_AND_CODE_TREE = (
    (SORTED_FREQUENCY_FOR_MESSAGE_1, EXPECTED_CODE_TREE_FOR_MESSAGE_1),
    (SORTED_FREQUENCY_FOR_MESSAGE_2, EXPECTED_CODE_TREE_FOR_MESSAGE_2),
    (SORTED_FREQUENCY_FOR_MESSAGE_3, EXPECTED_CODE_TREE_FOR_MESSAGE_3),
    (SORTED_FREQUENCY_FOR_MESSAGE_4, EXPECTED_CODE_TREE_FOR_MESSAGE_4),
    (SORTED_FREQUENCY_FOR_MESSAGE_5, EXPECTED_CODE_TREE_FOR_MESSAGE_5),
)


class TestHuffmanCode(TestCase):
    """Class with tests for Huffman code"""

    def test_get_symbols_with_frequency(self):
        """Test get_symbols_with_frequency function"""

        for message, expected_frequency in MESSAGE_AND_FREQUENCY.items():
            real_frequency = get_symbols_with_frequency(message)

            self.assertEqual(real_frequency, expected_frequency)

    def test_get_symbols_with_probability(self):
        """Test get_symbols_with_probability function"""

        for frequency, expected_probability in FREQUENCY_AND_PROBABILITY:
            real_probability = get_symbols_with_probability(frequency)

            self.assertEqual(real_probability, expected_probability)

    def test_get_probability_for_symbol(self):
        """Test get_probability_for_symbol function"""

        for frequency in range(0, 100, 2):
            with self.subTest(f'Frequency = {frequency}'):
                message_length = randint(frequency + 10, 200)
                expected_symbol_probability = round(frequency / message_length, 5)
                real_symbol_probability = get_probability_for_symbol(
                    frequency, message_length
                )

                self.assertEqual(
                    real_symbol_probability,
                    expected_symbol_probability
                )

    # TODO:
    def test_get_sorted_symbols_with_frequency(self):
        """Test get_sorted_symbols_with_frequency function"""

        for frequency, expected_sorted_frequency in FREQUENCY_AND_SORTED_FREQUENCY:
            real_sorted_frequency = get_sorted_symbols_with_frequency(
                frequency, False
            )
            self.assertEqual(real_sorted_frequency, expected_sorted_frequency)

    def test_is_tree(self):
        """Test is_tree function"""

        for tree in OBJECTS_TREES:
            with self.subTest(f'Tree: {tree}'):
                self.assertTrue(is_tree(tree))

        for object in OBJECTS_ARE_NOT_TREES:
            with self.subTest(f'Object: {object}'):
                self.assertFalse(is_tree(object))

    def test_get_huffman_code_tree(self):
        """Test get_huffman_code_tree function"""

        for frequency, expected_code_tree in FREQUENCY_AND_CODE_TREE:
            real_code_tree = get_huffman_code_tree(frequency)

            self.assertEqual(real_code_tree, expected_code_tree)
