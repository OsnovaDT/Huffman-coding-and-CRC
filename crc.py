"""Calculate CRC code"""

from collections import defaultdict
from re import findall
from pprint import pprint
from random import randint


MESSAGE = 'A4678FE1'

POLYNOMIAL = 'x^10 + x^9 + x^5 + x^4 + x + 1'


def get_truncated_to_4_symbols_binary_code(binary_code):
    """Delete excess zeroes and add symbols if it's need"""

    # TODO: Refactoring
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


def get_binary_code_from_hex(hex_code):
    """Get binary code from 16 bit code"""

    binary_code = ''

    for symbol in hex_code:
        symbol_binary_code = get_symbol_binary_code(symbol)

        binary_code += symbol_binary_code

    return binary_code


def get_w(polynomial):
    polynomial_items = polynomial.split(' + ')

    return int(findall('\d+', polynomial_items[0])[0])


def get_binary_code_from_polynomial(polynomial):
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


def main():
    # print('Binary code for message: ')
    binary_code_for_message = get_binary_code_from_hex(MESSAGE)
    w = get_w(POLYNOMIAL)
    binary_code_for_message = binary_code_for_message + '0' * w
    # print(binary_code_for_message)
    # print()

    # print('Binary code for polynomial: ')
    binary_code_for_polynomial = get_binary_code_from_polynomial(POLYNOMIAL)
    # print(binary_code_for_polynomial)

    crc_code = get_crc_code(
        binary_code_for_message, binary_code_for_polynomial
    )

    binary_code_for_message = get_binary_code_from_hex(MESSAGE)
    binary_code_for_message = binary_code_for_message + crc_code

    # Check message correct
    print('Correct:')
    print(get_crc_code(binary_code_for_message, binary_code_for_polynomial))

    # Check message incorrect
    binary_code_for_message = binary_code_for_message
    rand = randint(0, len(binary_code_for_message) - 1)

    rand_item = binary_code_for_message[rand]
    rand_item = '0' if rand_item == '1' else '1'
    binary_code_for_message = binary_code_for_message[:rand] + \
        rand_item + binary_code_for_message[rand+1:]
    print(get_crc_code(binary_code_for_message, binary_code_for_polynomial))


if __name__ == '__main__':
    main()
