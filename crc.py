"""Calculate CRC code"""

from collections import defaultdict
from random import randint
from re import findall


from colorama import Fore


HEX_MESSAGE = 'A4678FE1'
POLYNOMIAL = 'x ^ 10 + x ^ 9 + x ^ 5 + x ^ 4 + x + 1'


def get_binary_code_from_hex_code(hex_code):
    """Get binary code from hex code"""

    binary_code = bin(int(hex_code, 16))
    binary_code = binary_code.replace('0b', '')
    binary_code = binary_code.zfill(4)

    return binary_code


def get_binary_message_from_hex_message(hex_message):
    """Get binary message from hex message"""

    binary_message = ''

    for hex_code in hex_message:
        binary_code = get_binary_code_from_hex_code(hex_code)

        binary_message += binary_code

    return binary_message


def get_polynomial_degree(polynomial):
    """Get polynomial degree - position of the highest single bit"""

    polynomial_items = polynomial.split(' + ')
    first_polynomial_item = polynomial_items[0]
    number_for_first_polynomial_item = findall(r'\d+', first_polynomial_item)
    polynomial_degree = int(*number_for_first_polynomial_item)

    return polynomial_degree


def set_byte_1_for_exist_polynomial_items(
        polynomial_items, polynomial_item_degree_with_binary_code):
    """Set byte 1 for exist polynomial items"""

    for item in polynomial_items:
        if item == 'x':
            polynomial_item_degree_with_binary_code[1] = '1'
        elif item == '1':
            polynomial_item_degree_with_binary_code[0] = '1'
        else:
            polynomial_item_degree = int(findall(r'\d+', item)[0])
            polynomial_item_degree_with_binary_code[
                polynomial_item_degree
            ] = '1'


def set_byte_0_for_non_exist_polynomial_items(
        polynomial_degree, degrees_of_items_of_polynomial,
        polynomial_item_degree_with_binary_code):
    """Set byte 1 for exist polynomial items"""

    for degree in range(polynomial_degree + 1):
        if degree not in degrees_of_items_of_polynomial:
            polynomial_item_degree_with_binary_code[degree] = '0'


def get_binary_code_for_polynomial(polynomial):
    """Get binary code from polynomial"""

    polynomial_degree = get_polynomial_degree(polynomial)
    polynomial_items_with_bytes = get_polynomial_items_with_bytes(polynomial)
    binary_code_for_polynomial = ''
    polynomial_degrees = range(polynomial_degree + 1)[::-1]

    for degree in polynomial_degrees:
        polynomial_degree_binary_code = polynomial_items_with_bytes[degree]
        binary_code_for_polynomial += polynomial_degree_binary_code

    return binary_code_for_polynomial


def get_polynomial_items_with_bytes(polynomial):
    """Get dict that contains polynomial items and their bytes"""

    polynomial_items = polynomial.split(' + ')
    polynomial_items_with_bytes = defaultdict(str)
    polynomial_degree = get_polynomial_degree(polynomial)

    set_byte_1_for_exist_polynomial_items(
        polynomial_items, polynomial_items_with_bytes
    )

    degrees_of_items_of_polynomial = polynomial_items_with_bytes.keys()

    set_byte_0_for_non_exist_polynomial_items(
        polynomial_degree, degrees_of_items_of_polynomial,
        polynomial_items_with_bytes
    )

    return polynomial_items_with_bytes


def get_quotient_of_two_binary_codes(first_binary_code, second_binary_code):
    """Get quotient of two binary codes"""

    quotient = ''

    for code, _ in enumerate(second_binary_code):
        if first_binary_code[code] == second_binary_code[code]:
            quotient = quotient + '0'
        else:
            quotient = quotient + '1'

    quotient = quotient.lstrip('0')
    return quotient


def get_crc_code(divisible, divisor):
    """Get CRC code"""

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


def get_full_binary_message(incomplete_binary_message, degree_of_polynomial):
    """Get binary message supplemented with bits"""

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
        Fore.RED + invalid_byte + Fore.WHITE + \
        binary_message[correct_byte_index+1:]

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

    incomplete_binary_message = get_binary_message_from_hex_message(
        hex_message
    )
    degree_of_polynomial = get_polynomial_degree(polynomial)
    full_binary_message = get_full_binary_message(
        incomplete_binary_message, degree_of_polynomial
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
