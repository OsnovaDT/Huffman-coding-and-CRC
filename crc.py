"""Calculate CRC code"""

from collections import defaultdict
from random import randint
from re import findall


HEX_MESSAGE = 'A4678FE1'
POLYNOMIAL = 'x ^ 10 + x ^ 9 + x ^ 5 + x ^ 4 + x + 1'


def get_truncated_to_4_symbols_binary_code(binary_code):
    """Delete excess zeroes and add symbols if it's need"""

    binary_code = binary_code.lstrip('0')

    binary_code = binary_code.zfill(4)

    return binary_code


def get_symbol_binary_code(symbol):
    """Get binary code for symbol"""

    symbol_binary_code = (bin(int(symbol, 16))).replace('b', '')

    symbol_binary_code = get_truncated_to_4_symbols_binary_code(
        symbol_binary_code
    )

    return symbol_binary_code


def get_binary_message_from_hex(hex_code):
    """Get binary code from 16 bit code"""

    binary_code = ''

    for symbol in hex_code:
        symbol_binary_code = get_symbol_binary_code(symbol)

        binary_code += symbol_binary_code

    return binary_code


def get_degree_of_polynomial(polynomial):
    """Get position of the highest single bit"""

    polynomial_items = polynomial.split(' + ')

    return int(findall('\d+', polynomial_items[0])[0])


def get_binary_code_for_polynomial(polynomial):
    """Get binary code from polynomial"""

    # TODO: Refactoring
    polynomial_items = polynomial.split(' + ')
    polynomial_item_and_binary_code = defaultdict(str)

    w = int(findall('\d+', polynomial_items[0])[0])

    for item in polynomial_items:
        if item == 'x':
            polynomial_item_and_binary_code[1] = '1'
        elif item == '1':
            polynomial_item_and_binary_code[0] = '1'
        else:
            polynomial_item_number = findall('\d+', item)
            polynomial_item_and_binary_code[int(
                polynomial_item_number[0])] = '1'

    for i in range(w + 1):
        if i not in polynomial_item_and_binary_code.keys():
            polynomial_item_and_binary_code[i] = '0'

    a = ''

    for i in range(w + 1):
        a += polynomial_item_and_binary_code[i]

    return a[::-1]


def get_quotient_of_two_binary_codes(first, second):
    quotient = ''

    for code in range(len(second)):
        if first[code] == second[code]:
            quotient = quotient + '0'
        else:
            quotient = quotient + '1'

    quotient = quotient.lstrip('0')
    return quotient


def get_crc_code(divisible, divisor):
    divisor_length = len(divisor)

    divisible_initial_part = divisible[:divisor_length]
    divisible = divisible[divisor_length:]

    quotient = get_quotient_of_two_binary_codes(
        divisible_initial_part, divisor
    )

    while len(divisible) != 0:
        if len(quotient) != divisor_length:
            diff = divisor_length - len(quotient)
            for _ in range(diff):
                if len(divisible) == 0:
                    break
                quotient = quotient + divisible[0]
                divisible = divisible[1:]
        if len(divisible) == 0:
            break

        quotient = get_quotient_of_two_binary_codes(
            quotient, divisor
        )

    return quotient


def check_message(message, binary_code_for_polynomial):
    print(get_crc_code(message, binary_code_for_polynomial))


def get_full_binary_message(incomplete_binary_message, polynomial):
    """Get binary message supplemented with bits"""

    degree_of_polynomial = get_degree_of_polynomial(polynomial)
    additional_zeros_for_binary_message = '0' * degree_of_polynomial
    full_binary_message = incomplete_binary_message + \
        additional_zeros_for_binary_message

    return full_binary_message


def is_binary_message_with_crc_correct(
        binary_message_with_crc, binary_code_for_polynomial):
    """Check is binary message with CRC code correct"""

    print(f'\nCheck for message {binary_message_with_crc}')

    crc_code = get_crc_code(
        binary_message_with_crc,
        binary_code_for_polynomial
    )

    if crc_code == '0':
        print('Binary message with CRC is correct')
    else:
        print('Binary message with CRC is incorrect')


def get_opposite_byte(byte):
    """Convert byte to 0 if it's 1 and vice versa"""

    return '0' if byte == '1' else '1'


def get_incorrect_binary_message_with_crc(binary_message):
    """Get binary message with CRC with random mistake"""

    correct_byte_index = randint(0, len(binary_message) - 1)
    correct_byte = binary_message[correct_byte_index]

    invalid_byte = get_opposite_byte(correct_byte)
    incorrect_binary_message_with_crc = binary_message[:correct_byte_index] + \
        invalid_byte + binary_message[correct_byte_index+1:]

    return incorrect_binary_message_with_crc


def check_correct_and_incorrect_binary_message_with_crc(
        binary_message_with_crc, binary_code_for_polynomial):
    """Check correct and incorrect binary message with crc"""

    is_binary_message_with_crc_correct(
        binary_message_with_crc, binary_code_for_polynomial
    )

    incorrect_binary_message_with_crc = get_incorrect_binary_message_with_crc(
        binary_message_with_crc
    )
    is_binary_message_with_crc_correct(
        incorrect_binary_message_with_crc, binary_code_for_polynomial
    )


def print_all_info_for_crc_code(hex_message, polynomial):
    """Print all info for CRC code"""

    incomplete_binary_message = get_binary_message_from_hex(hex_message)
    full_binary_message = get_full_binary_message(
        incomplete_binary_message, polynomial
    )

    binary_code_for_polynomial = get_binary_code_for_polynomial(polynomial)

    crc_code = get_crc_code(
        full_binary_message, binary_code_for_polynomial
    )
    print(f'CRC code: {crc_code}')

    binary_message_with_crc = incomplete_binary_message + crc_code

    check_correct_and_incorrect_binary_message_with_crc(
        binary_message_with_crc, binary_code_for_polynomial
    )


if __name__ == '__main__':
    print_all_info_for_crc_code(HEX_MESSAGE, POLYNOMIAL)


# 168 - before Refactoring
