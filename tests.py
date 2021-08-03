"""Module with unit tests"""

from random import randint

from unittest import TestCase
from unittest.mock import patch, call

from huffman import (
    get_symbols_with_frequency, get_symbols_with_probability,
    get_probability_for_symbol, get_sorted_symbols_with_frequency,
    is_tree, get_huffman_code_tree, get_tree_nodes_and_frequency,
    is_tree_built, delete_first_2_nodes, get_entropy,
    print_frequency_and_probability_for_symbols, get_symbols_with_code,
    get_average_length_of_code_message, get_huffman_code,
    print_all_info_for_huffman_code, get_new_node_created_by_first_2_nodes,
    insert_node, add_node_created_by_first_2_nodes
)

# DATA FOR TESTING

TEST_MESSAGES = (
    "aabbbbbbbbccccdeeeee",
    "beep boop beer!",
    "Communication systems with over-the-air-programming",
    '',
    'ab'
)

TEST_MESSAGES_AMOUNT = len(TEST_MESSAGES)

EXPECTED_FREQUENCIES = (
    {'a': 2, 'b': 8, 'c': 4, 'd': 1, 'e': 5},
    {'b': 3, 'e': 4, 'p': 2, ' ': 2, 'o': 2, 'r': 1, '!': 1},
    {
        'C': 1, 'o': 4, 'm': 5, 'u': 1, 'n': 3, 'i': 5, 'c': 1,
        'a': 3, 't': 4, ' ': 3, 's': 3, 'y': 1, 'e': 3, 'w': 1,
        'h': 2, 'v': 1, 'r': 4, '-': 3, 'p': 1, 'g': 2
    },
    {},
    {'a': 1, 'b': 1},
)

EXPECTED_SORTED_FREQUENCIES = (
    {'b': 8, 'e': 5, 'c': 4, 'a': 2, 'd': 1},
    {'e': 4, 'b': 3, 'p': 2, ' ': 2, 'o': 2, 'r': 1, '!': 1},
    {
        'm': 5, 'i': 5, 'o': 4, 't': 4, 'r': 4, 'n': 3, 'a': 3, ' ': 3,
        's': 3, 'e': 3, '-': 3, 'h': 2, 'g': 2, 'C': 1, 'u': 1, 'c': 1,
        'y': 1, 'w': 1, 'v': 1, 'p': 1
    },
    {},
    {'a': 1, 'b': 1},
)

EXPECTED_PROBABILITIES = (
    {'a': 0.1, 'b': 0.4, 'c': 0.2, 'd': 0.05, 'e': 0.25},
    {
        'b': 0.2, 'e': 0.26667, 'p': 0.13333, ' ': 0.13333,
        'o': 0.13333, 'r': 0.06667, '!': 0.06667
    },
    {
        'C': 0.01961, 'o': 0.07843, 'm': 0.09804, 'u': 0.01961,
        'n': 0.05882, 'i': 0.09804, 'c': 0.01961, 'a': 0.05882,
        't': 0.07843, ' ': 0.05882, 's': 0.05882, 'y': 0.01961,
        'e': 0.05882, 'w': 0.01961, 'h': 0.03922, 'v': 0.01961,
        'r': 0.07843, '-': 0.05882, 'p': 0.01961, 'g': 0.03922
    },
    {},
    {'a': 0.5, 'b': 0.5},
)

EXPECTED_HUFFMAN_CODE_TREES = (
    [(('d', ('c', 'a')), ('b', 'e'))],
    [(('e', 'b'), (('!', ('o', 'r')), ('p', ' ')))],
    [
        ((('m', 'i'), (('-', 'h'), ('s', 'e'))),
        ((('a', ' '), ('r', 'n')), (('o', 't'),
        ((('v', 'p'), ('y', 'w')), (('u', 'c'), ('g', 'C'))))))
    ],
    [],
    [('a', 'b')],
)

EXPECTED_NODES_WITH_FREQUENCY = (
    (['a', 'b', 'c', 'd', 'e'], [2, 8, 4, 1, 5]),
    (['b', 'e', 'p', ' ', 'o', 'r', '!'], [3, 4, 2, 2, 2, 1, 1]),
    (
        [
            'C', 'o', 'm', 'u', 'n', 'i', 'c', 'a', 't',' ',
            's','y', 'e','w', 'h', 'v', 'r', '-', 'p', 'g'
        ],
        [1, 4, 5, 1, 3, 5, 1, 3, 4, 3, 3, 1, 3, 1, 2, 1, 4, 3, 1, 2]
    ),
    ([], []),
    (['a', 'b'], [1, 1])
)

EXPECTED_ENTROPIES = (2.04145, 2.65657, 4.10876, 0, 1)

EXPECTED_AVERAGE_LENGTHS = (
    2.1, 2.66667, 4.13729, None, 1.0
)

EXPECTED_HUFFMAN_CODES = [
    '110111010000000011111111111111001010101010',
    '0011111010100001101110101000111110001001',
    '1110101111000000111011100100111100001101100001111110010111010011100101'\
        + '0011000101000010001111000100011100101100111111110001101011101101'\
        + '0110010110010110100110001110110101000011011111101111101011000000'\
        + '0001100110111',
    '',
    '01',
]

TEST_CODE_TREES = (
    [('b', ('e', (('d', 'a'), 'c')))],
    [(('b', (' ', 'o')), ((('r', '!'), 'p'), 'e'))],
    [
        (
            (('m', 'i'), (('s', 'e'), ('a', ' '))),
            (
                ((('p', ('w', 'v')), 'n'), ('-', ('h', 'g'))),
                (('t', 'r'), ((('c', 'y'), ('C', 'u')), 'o'))
            )
        )
    ],
    None,
    [('a', 'b')],
)

TEST_SYMBOLS_WITH_CODE = (
    {'b': '0', 'e': '10', 'c': '111', 'd': '1100', 'a': '1101'},
    {
        'b': '00', ' ': '010', 'o': '011', 'e': '11',
        'p': '101', 'r': '1000', '!': '1001'
    },
    {
        'm': '000', 'i': '001', 's': '0100', 'e': '0101', 'a': '0110',
        ' ': '0111', 'n': '1001', 'p': '10000', 'w': '100010', 'v': '100011',
        '-': '1010', 'h': '10110', 'g': '10111', 't': '1100', 'r': '1101',
        'o': '1111', 'c': '111000', 'y': '111001', 'C': '111010', 'u': '111011'
    },
    None,
    {'a': '0', 'b': '1'}
)

# Data for testing is_tree function
TEST_OBJECTS_TREES = ((1, 2, 3), (1,), ('string1', 'string2'))

TEST_OBJECTS_ARE_NOT_TREES = (1, [1, 2, 3], 'string', None, 0)

# Data for testing is_tree_built function
TEST_BUILT_TREES = (
    [[((('c', 'd'), 'e'), ('a', 'b'))], [20]],
    [[(('e', 'b'), (('!', ('o', 'r')), ('p', ' ')))], [15]],
    [
        [
            (
                (('m', 'i'), (('-', 'h'), ('s', 'e'))),
                (
                    (('a', ' '), ('r', 'n')),
                    (
                        ('o', 't'),
                        (
                            (('v', 'p'), ('y', 'w')),
                            (('u', 'c'), ('g', 'C'))
                        )
                    )
                )
            )
        ],
        [51]
    ],
    [[('a', 'b')], [2]],
)

TEST_UNBUILT_TREES = (
    [[((('c', 'd'), 'e'))], [2, 3]],
    [[('e', 'b')], [1, 1, 2]],
    [[(('e', 'b'), ('a', 'c'))], [4, 1, 2, 5, 2]]
)

# Data for testing get_new_node_created_by_first_2_nodes function
TEST_TREES_AND_EXPECTED_NEW_NODES = (
    (
        [
            ['C', 'u', 'c', 'y', 'w', 'v', 'p', 'h', 'g', 'n', 'a']
            + [' ', 's', 'e', '-', 'o', 't', 'r', 'm', 'i'],
            [1, 1, 1, 1, 1, 1, 1, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4, 4, 5, 5]
        ],
        (('C', 'u'), 2)
    ),
    (
        [
            ['-', ('h', 'g'), (('c', 'y'), ('C', 'u')), 'o', 't', 'r',]
            + ['m', 'i', ('s', 'e'), ('a', ' '), (('p', ('w', 'v')), 'n')],
            [3, 4, 4, 4, 4, 4, 5, 5, 6, 6, 6]
        ],
        (('-', ('h', 'g')), 7)
    ),
    (
        [
            [
                ((('p', ('w', 'v')), 'n'), ('-', ('h', 'g'))),
                (('t', 'r'), ((('c', 'y'), ('C', 'u')), 'o')),
                (('m', 'i'), (('s', 'e'), ('a', ' ')))
            ],
            [13, 16, 22]
        ],
        (
            (
                ((('p', ('w', 'v')), 'n'), ('-', ('h', 'g'))),
                (('t', 'r'), ((('c', 'y'), ('C', 'u')), 'o'))
            ), 29
        )
    )
)

# Data for testing delete_first_2_nodes function
TEST_TREE_AND_TREE_AFTER_DELETING_FIRST_2_NODES = (
    (
        [['b', 'e', 'c', 'a', 'd'], [8, 5, 4, 2, 1]],
        [['c', 'a', 'd'], [4, 2, 1]]
    ),
    (
        [['c', 'a', 'd', ('b', 'e')], [4, 2, 1, 13]],
        [['d', ('b', 'e')], [1, 13]]
    ),
    (
        [['d', ('c', 'a'), ('b', 'e')], [1, 6, 13]],
        [[('b', 'e')], [13]]
    ),
    (
        [[('d', ('c', 'a')), ('b', 'e')], [7, 13]],
        [[], []]
    ),
)

# Data for testing test_insert_node function
TEST_TREES_BEFORE_ADDING_NODE = (
    # Tree 1
    [
        [
            'c', 'y', 'w', 'v', 'p', 'h', 'g', 'n', 'a', ' ',
            's', 'e', '-', 'o', 't', 'r', 'm', 'i'
        ],
        [1, 1, 1, 1, 1, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4, 4, 5, 5]
    ],

    # Tree 2
    [
        [
            'h', 'g', ('p', ('w', 'v')), 'n', 'a', ' ', 's', 'e',
            '-', 'o', 't', 'r', 'm', 'i'
        ],
        [2, 2, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 5, 5]
    ],
)

TEST_TREES_AFTER_ADDING_NODE = [
    # Tree 1
    (
        [
            [
                'c', 'y', 'w', 'v', 'p', ('C', 'u'), 'h', 'g', 'n', 'a',
                ' ', 's', 'e', '-', 'o', 't', 'r', 'm', 'i'
            ],
            [1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4, 4, 5, 5]
        ]
    ),

    # Tree 2
    (
        [
            [
                'h', 'g', ('p', ('w', 'v')), 'n', 'a', ' ', 's', 'e', '-',
                (('c', 'y'), ('C', 'u')), 'o', 't', 'r', 'm', 'i'
            ], 
            [2, 2, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5]
        ]
    )
]

TEST_NODES_AND_INDEXES_FOR_ADDING_NODE = (
    ((('C', 'u'), 2), 5),
    (((('c', 'y'), ('C', 'u')), 4), 9),
)

# Data for testing add_node_created_by_first_2_nodes function
TEST_TREE_AND_TREE_AFTER_ADDING_NODES = (
    # Tree 1
    [
        # Tree before adding nodes
        [
            [
                'C', 'u', 'c', 'y', 'w', 'v', 'p', 'h', 'g', 'n', 'a', ' ',
                's', 'e', '-', 'o', 't', 'r', 'm', 'i'
            ],
            [1, 1, 1, 1, 1, 1, 1, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4, 4, 5, 5]
        ],

        # Tree after adding nodes
        [
            [
                'c', 'y', 'w', 'v', 'p', ('C', 'u'), 'h', 'g', 'n', 'a', ' ',
                's', 'e', '-', 'o', 't', 'r', 'm', 'i'
            ],
            [1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4, 4, 5, 5]
        ]
    ],

    # Tree 2
    [
        # Tree before adding nodes
        [
            [
                'm', 'i', ('s', 'e'), ('a', ' '), (('p', ('w', 'v')), 'n'),
                ('-', ('h', 'g')), ('t', 'r'), ((('c', 'y'), ('C', 'u')), 'o')
            ],
            [5, 5, 6, 6, 6, 7, 8, 8]
        ],

        # Tree after adding nodes
        [
            [
                ('s', 'e'), ('a', ' '), (('p', ('w', 'v')), 'n'),
                ('-', ('h', 'g')), ('t', 'r'),
                ((('c', 'y'), ('C', 'u')), 'o'),('m', 'i')
            ],
            [6, 6, 6, 7, 8, 8, 10]
        ]
    ],

    # Tree 3
    [
        # Tree before adding nodes
        [
            [
                ('m', 'i'), (('s', 'e'), ('a', ' ')),
                ((('p', ('w', 'v')), 'n'),('-', ('h', 'g'))),
                (('t', 'r'), ((('c', 'y'), ('C', 'u')), 'o'))
            ],
            [10, 12, 13, 16]
        ],

        # Tree after adding nodes
        [
            [
                ((('p', ('w', 'v')), 'n'), ('-', ('h', 'g'))),
                (('t', 'r'), ((('c', 'y'), ('C', 'u')), 'o')),
                (('m', 'i'), (('s', 'e'), ('a', ' ')))
            ],
            [13, 16, 22]
        ],
    ]
)


class TestHuffmanCode(TestCase):
    """Class with tests for Huffman code"""

    def test_get_symbols_with_frequency(self):
        """Test get_symbols_with_frequency function"""

        for i in range(TEST_MESSAGES_AMOUNT):
            with self.subTest(f'Message = {TEST_MESSAGES[i]}'):
                expected_message_frequency = EXPECTED_FREQUENCIES[i]
                real_message_frequency = get_symbols_with_frequency(
                    TEST_MESSAGES[i]
                )

                self.assertEqual(
                    real_message_frequency, expected_message_frequency
                )

    def test_get_symbols_with_probability(self):
        """Test get_symbols_with_probability function"""

        for i in range(TEST_MESSAGES_AMOUNT):
            message_frequency = EXPECTED_FREQUENCIES[i]

            with self.subTest(f'Message frequency = {message_frequency}'):
                expected_message_probability = EXPECTED_PROBABILITIES[i]
                real_message_probability = get_symbols_with_probability(
                    message_frequency
                )

                self.assertEqual(
                    real_message_probability, expected_message_probability
                )

    def test_get_probability_for_symbol(self):
        """Test get_probability_for_symbol function"""

        for frequency in range(0, 100, 2):
            with self.subTest(f'Frequency = {frequency}'):
                message_length = randint(frequency + 10, 200)

                expected_symbol_probability = round(
                    frequency / message_length, 5
                )

                real_symbol_probability = get_probability_for_symbol(
                    frequency, message_length
                )

                self.assertEqual(
                    real_symbol_probability, expected_symbol_probability
                )

    def test_get_sorted_symbols_with_frequency(self):
        """Test get_sorted_symbols_with_frequency function"""

        for i in range(TEST_MESSAGES_AMOUNT):
            real_sorted_frequency = get_sorted_symbols_with_frequency(
                EXPECTED_FREQUENCIES[i], False
            )
            self.assertEqual(real_sorted_frequency, EXPECTED_SORTED_FREQUENCIES[i])

    def test_is_tree(self):
        """Test is_tree function"""

        for tree in TEST_OBJECTS_TREES:
            with self.subTest(f'Tree: {tree}'):
                self.assertTrue(is_tree(tree))

        for object in TEST_OBJECTS_ARE_NOT_TREES:
            with self.subTest(f'Object: {object}'):
                self.assertFalse(is_tree(object))

    def test_get_huffman_code_tree(self):
        """Test get_huffman_code_tree function"""

        for i in range(TEST_MESSAGES_AMOUNT):
            real_code_tree = get_huffman_code_tree(EXPECTED_SORTED_FREQUENCIES[i])

            self.assertEqual(real_code_tree, EXPECTED_HUFFMAN_CODE_TREES[i])

    def test_get_tree_nodes_and_frequency(self):
        """Test get_tree_nodes_and_frequency function"""

        for i in range(TEST_MESSAGES_AMOUNT):
            expected_node_and_frequency = EXPECTED_NODES_WITH_FREQUENCY[i]
            frequency = EXPECTED_FREQUENCIES[i]

            with self.subTest(f'Expected: {expected_node_and_frequency}'):
                code_tree = [
                    list(frequency.keys()), list(frequency.values())
                ]
                real_node_and_frequency = get_tree_nodes_and_frequency(code_tree)

                self.assertEqual(real_node_and_frequency, expected_node_and_frequency)

    def test_is_tree_built(self):
        """Test is_tree_built function"""

        for built_tree in TEST_BUILT_TREES:
            with self.subTest(f'Tree: {built_tree}'):
                self.assertTrue(is_tree_built(built_tree))

        for unbuilt_tree in TEST_UNBUILT_TREES:
            with self.subTest(f'Tree: {unbuilt_tree}'):
                self.assertFalse(is_tree_built(unbuilt_tree))

    def test_delete_first_2_nodes(self):
        """Test delete_first_2_nodes function"""

        for tree, expected_tree_after_deleting in TEST_TREE_AND_TREE_AFTER_DELETING_FIRST_2_NODES:
            with self.subTest(f'Expected tree: {expected_tree_after_deleting}'):
                delete_first_2_nodes(tree)

                self.assertEqual(tree, expected_tree_after_deleting)

    def test_get_entropy(self):
        """Test get_entropy function"""

        for i in range(TEST_MESSAGES_AMOUNT):
            expected_entropy = EXPECTED_ENTROPIES[i]

            with self.subTest(f'Expected entropy: {expected_entropy}'):
                real_entropy = get_entropy(TEST_MESSAGES[i])

                self.assertEqual(real_entropy, expected_entropy)

        # for message, expected_entropy in MESSAGE_AND_ENTROPY.items():
        #     with self.subTest(f'Expected entropy: {expected_entropy}'):
        #         real_entropy = get_entropy(message)

        #         self.assertEqual(real_entropy, expected_entropy)

    def test_get_average_length_of_code_message(self):
        """Test get_average_length_of_code_message function"""

        for i in range(TEST_MESSAGES_AMOUNT):
            if i == 3:
                continue

            symbols_with_code = TEST_SYMBOLS_WITH_CODE[i]
            frequency = EXPECTED_FREQUENCIES[i]
            expected_average_length = EXPECTED_AVERAGE_LENGTHS[i]

            with self.subTest(f'Expected average length: {expected_average_length}'):
                real_average_length = get_average_length_of_code_message(
                    symbols_with_code, frequency
                )

                self.assertEqual(real_average_length, expected_average_length)

    def test_get_huffman_code(self):
        """Test get_huffman_code function"""

        for i in range(TEST_MESSAGES_AMOUNT):
            expected_huffman_code = EXPECTED_HUFFMAN_CODES[i]

            with self.subTest(f'Expected huffman code: {expected_huffman_code}'):
                real_huffman_code = get_huffman_code(
                    TEST_SYMBOLS_WITH_CODE[i], TEST_MESSAGES[i]
                )

                self.assertEqual(real_huffman_code, expected_huffman_code)

    def test_get_symbols_with_code(self):
        """Test get_symbols_with_code function"""

        for i in range(TEST_MESSAGES_AMOUNT):
            if i == 3:
                continue

            expected_symbols_with_code = TEST_SYMBOLS_WITH_CODE[i]

            with self.subTest(f'Expected symbols with code: {expected_symbols_with_code}'):
                real_symbols_with_code = get_symbols_with_code(
                    *TEST_CODE_TREES[i], {}
                )

                self.assertEqual(
                    real_symbols_with_code, expected_symbols_with_code
                )

    def test_get_new_node_created_by_first_2_nodes(self):
        """Test get_new_node_created_by_first_2_nodes function"""

        for tree, expected_new_nodes in TEST_TREES_AND_EXPECTED_NEW_NODES:
            real_new_nodes = get_new_node_created_by_first_2_nodes(tree)

            self.assertEqual(real_new_nodes, expected_new_nodes)

    def test_insert_node(self):
        """Test insert_node function"""

        for i in range(len(TEST_TREES_BEFORE_ADDING_NODE)):
            insert_node(
                TEST_NODES_AND_INDEXES_FOR_ADDING_NODE[i][0],
                TEST_NODES_AND_INDEXES_FOR_ADDING_NODE[i][1],
                TEST_TREES_BEFORE_ADDING_NODE[i]
            )

            self.assertEqual(TEST_TREES_BEFORE_ADDING_NODE[i], TEST_TREES_AFTER_ADDING_NODE[i])

    def test_add_node_created_by_first_2_nodes(self):
        """Test add_node_created_by_first_2_nodes function"""

        for tree, expected_tree_after_adding_nodes_ in TEST_TREE_AND_TREE_AFTER_ADDING_NODES:
            with self.subTest(f'Expected tree {expected_tree_after_adding_nodes_}'):
                add_node_created_by_first_2_nodes(tree)

                self.assertEqual(tree, expected_tree_after_adding_nodes_)

    @patch('builtins.print')
    def test_print_all_info_for_huffman_code(self, mocked_print):
        """Test print_all_info_for_huffman_code function"""

        for i in range(TEST_MESSAGES_AMOUNT):
            if i == 3:
                continue

            letter_calls = [
                call('Symbol\tFrequency\tProbability\n')
            ]

            for letter, letter_frequency in EXPECTED_SORTED_FREQUENCIES[i].items():
                letter_probability = EXPECTED_PROBABILITIES[i][letter]

                letter_calls.append(
                    call(f'{letter}\t{letter_frequency}\t\t{letter_probability}')
                )
            mocked_print.mock_calls = []

            print_all_info_for_huffman_code(TEST_MESSAGES[i])

            self.assertEqual(
                mocked_print.mock_calls,
                [
                    call(f'Initial message: {TEST_MESSAGES[i]}\n'),
                    *letter_calls,
                    call('\nEntropy:', EXPECTED_ENTROPIES[i]),
                    call('\nAverage length of code message:', EXPECTED_AVERAGE_LENGTHS[i]),
                    call('\nHuffman code:', EXPECTED_HUFFMAN_CODES[i]),
                ]
            )

    @patch('builtins.print')
    def test_print_frequency_and_probability_for_symbols(self, mocked_print):
        """Test print_frequency_and_probability_for_symbols function"""

        for i in range(TEST_MESSAGES_AMOUNT):
            not_sorted_frequency = EXPECTED_FREQUENCIES[i]
            sorted_frequency = EXPECTED_SORTED_FREQUENCIES[i]
            probability = EXPECTED_PROBABILITIES[i]

            with self.subTest(sorted_frequency):
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
# 670