from huffman import print_all_info_for_huffman_code

HUFFMAN_MESSAGE = "Communication systems with over-the-air-programming"


def print_all_info_for_huffman_code_and_crc():
    print('Huffman code: \n')
    print_all_info_for_huffman_code(HUFFMAN_MESSAGE)


if __name__ == '__main__':
    print_all_info_for_huffman_code_and_crc()
