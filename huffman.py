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


def get_probability_for_symbol(symbol_frequency, message_len):
    """Get probability for symbol"""

    return round(symbol_frequency / message_len, 5)


def calculate_symbols_probability(
        symbols_probability, symbols_frequency, message_len):
    """Calculate probability for all symbols in the message"""

    for symbol, frequency in symbols_frequency.items():
        probability_for_current_symbol = get_probability_for_symbol(
            frequency, message_len
        )

        symbols_probability[symbol] = probability_for_current_symbol


def get_symbols_probability(message):
    """Get probability for symbols in the message"""

    symbols_probability = dict()

    symbols_frequency = get_symbols_frequency(message)
    message_len = len(message)

    calculate_symbols_probability(
        symbols_probability, symbols_frequency, message_len
    )

    return symbols_probability


def get_sorted_symbols_by_frequency(symbols_frequency):
    """Get sorted symbols by frequency"""

    symbols_frequency = dict(sorted(
        symbols_frequency.items(),
        key=lambda item: item[1],
        reverse=True
    ))

    return symbols_frequency


def print_frequency_and_probability_for_symbols(
        symbols_frequency, symbols_probability):
    """Print frequency and probability for symbols"""

    symbols_frequency = get_sorted_symbols_by_frequency(symbols_frequency)
    symbols = symbols_frequency.keys()

    print('Symbol\tFrequency\tProbability\n')

    for symbol in symbols:
        symbol_frequency = symbols_frequency[symbol]
        symbol_probability = symbols_probability[symbol]

        print(f"{symbol}\t{symbol_frequency}\t\t{symbol_probability}")


def calculate_huffman_code(message):
    """Calculate Huffman code"""

    print(f'Initial message: {message}\n')

    symbols_frequency = get_symbols_frequency(message)
    symbols_probability = get_symbols_probability(message)

    print_frequency_and_probability_for_symbols(
        symbols_frequency, symbols_probability
    )


if __name__ == '__main__':
    calculate_huffman_code(MESSAGE)
