"""Calculate Huffman code"""

from collections import defaultdict


MESSAGE = "Communication systems with over-the-air-programming"


def get_symbols_frequency(message):
    """Get frequency for symbols in the message"""

    symbols_frequency = defaultdict(int)

    for symbol in message:
        # Increment frequency for current symbol
        symbols_frequency[symbol] += 1

    return dict(symbols_frequency)


def get_symbols_probability(symbols_frequency):
    """Get probability for symbols in the message"""

    symbols_probability = dict()
    message_len = sum(symbols_frequency.values())

    for symbol, symbol_frequency in symbols_frequency.items():
        probability_for_current_symbol = get_probability_for_symbol(
            symbol_frequency, message_len
        )
        symbols_probability[symbol] = probability_for_current_symbol

    return symbols_probability


def get_probability_for_symbol(symbol_frequency, message_len):
    """Get probability for symbol"""

    return round(symbol_frequency / message_len, 5)


def get_symbols_sorted_by_frequency(symbols_frequency):
    """Get symbols sorted by frequency"""

    symbols_sorted_by_frequency = dict(sorted(
        symbols_frequency.items(),
        key=lambda symbol_and_frequency: symbol_and_frequency[1],
        reverse=True
    ))

    return symbols_sorted_by_frequency


def print_frequency_and_probability_for_symbols(
        symbols_frequency, symbols_probability):
    """Print frequency and probability for symbols"""

    symbols_sorted_by_frequency = get_symbols_sorted_by_frequency(
        symbols_frequency
    )
    symbols = symbols_sorted_by_frequency.keys()

    print('Symbol\tFrequency\tProbability\n')

    for symbol in symbols:
        symbol_frequency = symbols_sorted_by_frequency[symbol]
        symbol_probability = symbols_probability[symbol]

        print(f"{symbol}\t{symbol_frequency}\t\t{symbol_probability}")


def calculate_huffman_code(message):
    """Calculate Huffman code"""

    print(f'Initial message: {message}\n')

    symbols_frequency = get_symbols_frequency(message)
    symbols_probability = get_symbols_probability(symbols_frequency)

    print_frequency_and_probability_for_symbols(
        symbols_frequency, symbols_probability
    )


if __name__ == '__main__':
    calculate_huffman_code(MESSAGE)
