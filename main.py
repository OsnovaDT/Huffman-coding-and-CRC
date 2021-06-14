from huffman import print_all_info_for_huffman_code
from crc import print_all_info_for_crc_code

HUFFMAN_MESSAGE = "Communication systems with over-the-air-programming"

HEX_MESSAGE = 'A4678FE1'
POLYNOMIAL = 'x^10 + x^9 + x^5 + x^4 + x + 1'


def print_all_info_for_huffman_code_and_crc():
    print('Huffman code: \n')
    print_all_info_for_huffman_code(HUFFMAN_MESSAGE)
    print()

    print_all_info_for_crc_code(HEX_MESSAGE, POLYNOMIAL)


if __name__ == '__main__':
    print_all_info_for_huffman_code_and_crc()
