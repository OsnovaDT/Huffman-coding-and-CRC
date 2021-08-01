"""Module with tests"""

from random import randint

from unittest import TestCase
from unittest.mock import patch, call

from huffman import (
    get_symbols_with_frequency, get_symbols_with_probability,
    get_probability_for_symbol, get_sorted_symbols_with_frequency,
    is_tree, get_huffman_code_tree, get_tree_nodes_and_frequency,
    is_tree_built, delete_first_2_nodes,
    print_frequency_and_probability_for_symbols
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

# Nodes and frequency
EXPECTED_NODES_WITH_FREQUENCY_FOR_MESSAGE_1 = (
    ['a', 'b', 'c', 'd', 'e'], [2, 8, 4, 1, 5]
)

EXPECTED_NODES_WITH_FREQUENCY_FOR_MESSAGE_2 = (
    ['b', 'e', 'p', ' ', 'o', 'r', '!'], [3, 4, 2, 2, 2, 1, 1]
)

EXPECTED_NODES_WITH_FREQUENCY_FOR_MESSAGE_3 = (
    [
        'C', 'o', 'm', 'u', 'n', 'i', 'c', 'a', 't',' ',
        's','y', 'e','w', 'h', 'v', 'r', '-', 'p', 'g'
    ],
    [1, 4, 5, 1, 3, 5, 1, 3, 4, 3, 3, 1, 3, 1, 2, 1, 4, 3, 1, 2]
)

EXPECTED_NODES_WITH_FREQUENCY_FOR_MESSAGE_4 = ([], [])

EXPECTED_NODES_WITH_FREQUENCY_FOR_MESSAGE_5 = (['a', 'b'], [1, 1])

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

# Data for testing get_tree_nodes_and_frequency function
FREQUENCY_AND_NODES_WITH_FREQUENCY = (
    (EXPECTED_FREQUENCY_FOR_MESSAGE_1, EXPECTED_NODES_WITH_FREQUENCY_FOR_MESSAGE_1),
    (EXPECTED_FREQUENCY_FOR_MESSAGE_2, EXPECTED_NODES_WITH_FREQUENCY_FOR_MESSAGE_2),
    (EXPECTED_FREQUENCY_FOR_MESSAGE_3, EXPECTED_NODES_WITH_FREQUENCY_FOR_MESSAGE_3),
    (EXPECTED_FREQUENCY_FOR_MESSAGE_4, EXPECTED_NODES_WITH_FREQUENCY_FOR_MESSAGE_4),
    (EXPECTED_FREQUENCY_FOR_MESSAGE_5, EXPECTED_NODES_WITH_FREQUENCY_FOR_MESSAGE_5),
)

# Data for testing test_is_tree_built function
BUILT_TREES = (
    [[((('c', 'd'), 'e'), ('a', 'b'))], [20]],
    [[(('e', 'b'), (('!', ('o', 'r')), ('p', ' ')))], [15]],
    [
        [
            ((('m', 'i'), (('-', 'h'),
            ('s', 'e'))), ((('a', ' '),
            ('r', 'n')), (('o', 't'),
            ((('v', 'p'), ('y', 'w')),
            (('u', 'c'), ('g', 'C'))))))
        ],
        [51]
    ],
    [[('a', 'b')], [2]],
)

UNBUILT_TREES = (
    [[((('c', 'd'), 'e'))], [2, 3]],
    [[('e', 'b')], [1, 1, 2]],
    [[(('e', 'b'), ('a', 'c'))], [4, 1, 2, 5, 2]]
)

# Data for testing delete_first_2_nodes function
TREE_BEFORE_AND_AFTER_FIRST_2_NODES_DELETING = (
    ([['b', 'e', 'c', 'a', 'd'], [8, 5, 4, 2, 1]], [['c', 'a', 'd'], [4, 2, 1]]),
    ([['c', 'a', 'd', ('b', 'e')], [4, 2, 1, 13]], [['d', ('b', 'e')], [1, 13]]),
    ([['d', ('c', 'a'), ('b', 'e')], [1, 6, 13]], [[('b', 'e')], [13]]),
    ([[('d', ('c', 'a')), ('b', 'e')], [7, 13]], [[], []]),
)

# Data for testing print_frequency_and_probability_for_symbols function
probability_and_frequency_with_sorted_frequency = (
    (
        EXPECTED_PROBABILITY_FOR_MESSAGE_1,
        (EXPECTED_FREQUENCY_FOR_MESSAGE_1, SORTED_FREQUENCY_FOR_MESSAGE_1)
    ),
    (
        EXPECTED_PROBABILITY_FOR_MESSAGE_2,
        (EXPECTED_FREQUENCY_FOR_MESSAGE_2, SORTED_FREQUENCY_FOR_MESSAGE_2)
    ),
    (
        EXPECTED_PROBABILITY_FOR_MESSAGE_3,
        (EXPECTED_FREQUENCY_FOR_MESSAGE_3, SORTED_FREQUENCY_FOR_MESSAGE_3)
    ),
    (
        EXPECTED_PROBABILITY_FOR_MESSAGE_4,
        (EXPECTED_FREQUENCY_FOR_MESSAGE_4, SORTED_FREQUENCY_FOR_MESSAGE_4)
    ),
    (
        EXPECTED_PROBABILITY_FOR_MESSAGE_5,
        (EXPECTED_FREQUENCY_FOR_MESSAGE_5, SORTED_FREQUENCY_FOR_MESSAGE_5)
    ),
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

    def test_get_tree_nodes_and_frequency(self):
        """Test get_tree_nodes_and_frequency function"""

        for frequency, expected_node_and_frequency in FREQUENCY_AND_NODES_WITH_FREQUENCY:
            with self.subTest(f'Expected: {expected_node_and_frequency}'):
                code_tree = [
                    list(frequency.keys()), list(frequency.values())
                ]
                real_node_and_frequency = get_tree_nodes_and_frequency(code_tree)

                self.assertEqual(real_node_and_frequency, expected_node_and_frequency)

    def test_is_tree_built(self):
        """Test is_tree_built function"""

        for built_tree in BUILT_TREES:
            with self.subTest(f'Tree: {built_tree}'):
                self.assertTrue(is_tree_built(built_tree))

        for unbuilt_tree in UNBUILT_TREES:
            with self.subTest(f'Tree: {unbuilt_tree}'):
                self.assertFalse(is_tree_built(unbuilt_tree))

    def test_delete_first_2_nodes(self):
        """Test delete_first_2_nodes function"""

        for tree, expected_tree_after_deleting in TREE_BEFORE_AND_AFTER_FIRST_2_NODES_DELETING:
            with self.subTest(f'Expected tree: {expected_tree_after_deleting}'):
                delete_first_2_nodes(tree)

                self.assertEqual(tree, expected_tree_after_deleting)

    @patch('builtins.print')
    def test_print_frequency_and_probability_for_symbols(self, mocked_print):
        """Test print_frequency_and_probability_for_symbols function"""

        for probability, frequencies in probability_and_frequency_with_sorted_frequency:
            not_sorted_frequency = frequencies[0]
            sorted_frequency = frequencies[1]

            with self.subTest(frequencies):
                mocked_print.mock_calls = []
                letter_calls = []

                print_frequency_and_probability_for_symbols(
                    not_sorted_frequency, probability
                )

                for letter, letter_frequency in sorted_frequency.items():
                    letter_probability = probability[letter]

                    letter_calls.append(
                        call(f'{letter}\t{letter_frequency}\t\t{letter_probability}')
                    )

                self.assertEqual(
                    mocked_print.mock_calls,
                    [
                        call('Symbol\tFrequency\tProbability\n'),
                    ] + letter_calls
                )
