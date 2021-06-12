"""Calculate Huffman code"""

from bisect import bisect_left
from collections import defaultdict
from pprint import pprint


MESSAGE = "Communication systems with over-the-air-programming"
# MESSAGE = "hello"


def get_symbols_with_frequency(message):
    """Get frequency for symbols in the message"""

    symbols_with_frequency = defaultdict(int)

    for symbol in message:
        # Increment frequency for current symbol
        symbols_with_frequency[symbol] += 1

    return dict(symbols_with_frequency)


def get_symbols_probability(symbols_with_frequency):
    """Get probability for symbols in the message"""

    symbols_probability = dict()
    message_len = sum(symbols_with_frequency.values())

    for symbol, symbol_frequency in symbols_with_frequency.items():
        probability_for_current_symbol = get_probability_for_symbol(
            symbol_frequency, message_len
        )
        symbols_probability[symbol] = probability_for_current_symbol

    return symbols_probability


def get_probability_for_symbol(symbol_frequency, message_len):
    """Get probability for symbol"""

    return round(symbol_frequency / message_len, 5)


def get_sorted_symbols_with_frequency(
        symbols_with_frequency, in_descending_order=True):
    """Get symbols sorted by frequency"""

    sorted_symbols_with_frequency = dict(sorted(
        symbols_with_frequency.items(),
        key=lambda symbol_and_frequency: symbol_and_frequency[1],
        reverse=in_descending_order
    ))

    return sorted_symbols_with_frequency


def print_frequency_and_probability_for_symbols(
        symbols_with_frequency, symbols_probability):
    """Print frequency and probability for symbols"""

    sorted_symbols_with_frequency = get_sorted_symbols_with_frequency(
        symbols_with_frequency
    )
    symbols = sorted_symbols_with_frequency.keys()

    print('Symbol\tFrequency\tProbability\n')

    for symbol in symbols:
        symbol_frequency = sorted_symbols_with_frequency[symbol]
        symbol_probability = symbols_probability[symbol]

        print(f"{symbol}\t{symbol_frequency}\t\t{symbol_probability}")


def get_huffman_code_tree(symbols_with_frequency):
    """Get Huffman code tree by symbols frequency"""

    code_tree = [
        list(symbols_with_frequency.keys()),
        list(symbols_with_frequency.values())
    ]

    while not is_tree_built(code_tree):
        add_node_created_by_first_2_nodes(code_tree)

    code_tree = code_tree[0]

    return code_tree


def add_node_created_by_first_2_nodes(tree):
    """Add node that is union of first 2 nodes"""

    tree_frequency = tree[1]
    new_node = get_new_node_created_by_first_2_nodes(tree)
    new_node_frequency = new_node[1]

    new_node_index = bisect_left(tree_frequency, new_node_frequency)

    insert_node(new_node, new_node_index, tree)


def get_tree_nodes_and_frequency(tree):
    """Get nodes and frequency for tree"""

    return tree[0], tree[1]


def insert_node(node, node_index, tree):
    """Insert node to tree by index"""

    tree_nodes, tree_frequency = get_tree_nodes_and_frequency(tree)
    node, node_frequency = node[0], node[1]

    tree_nodes.insert(node_index, node)
    tree_frequency.insert(node_index, node_frequency)


def is_tree_built(tree):
    """Check is tree built"""

    tree_frequency = tree[1]

    return len(tree_frequency) == 1


def get_new_node_created_by_first_2_nodes(tree):
    """Get new node that is union of first 2 nodes"""

    tree_nodes, tree_frequency = get_tree_nodes_and_frequency(tree)

    new_node_symbols = (tree_nodes[0], tree_nodes[1])
    new_node_frequency = tree_frequency[0] + tree_frequency[1]

    delete_first_2_nodes(tree)

    return new_node_symbols, new_node_frequency


def delete_first_2_nodes(tree):
    """Delete first 2 nodes from tree"""

    tree_nodes, tree_frequency = get_tree_nodes_and_frequency(tree)

    del tree_nodes[0]
    del tree_nodes[0]

    del tree_frequency[0]
    del tree_frequency[0]


def calculate_huffman_code(message):
    """Calculate Huffman code"""

    print(f'Initial message: {message}\n')

    symbols_with_frequency = get_symbols_with_frequency(message)
    sorted_symbols_with_frequency = get_sorted_symbols_with_frequency(
        symbols_with_frequency, False
    )

    symbols_probability = get_symbols_probability(symbols_with_frequency)

    print_frequency_and_probability_for_symbols(
        symbols_with_frequency, symbols_probability
    )

    print('\nHuffman code tree:')
    pprint(get_huffman_code_tree(sorted_symbols_with_frequency))


if __name__ == '__main__':
    calculate_huffman_code(MESSAGE)
