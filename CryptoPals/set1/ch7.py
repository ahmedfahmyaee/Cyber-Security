from base64 import b64decode
from typing import List
from collections import deque
from pyfinite import ffield

BLOCK_SIZE = 16
MATRIX_DIMENSION = 4
NUMBER_OF_ROUNDS = 10
BYTE_SIZE = 8
BINARY_BASE = 2
GALOIS_FIELD_GENERATOR = 0x11b
GALOIS_FIELD = ffield.FField(8, gen=GALOIS_FIELD_GENERATOR, useLUT=0)

KEY = 'YELLOW SUBMARINE'.encode()
with open(r'D:\PycharmProjects\CryptoPals\set1\ch7_b64.txt', 'r') as f:
    CIPHER_TEXT = b64decode(f.read())

S_BOX = (
        (0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76),
        (0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0),
        (0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15),
        (0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75),
        (0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84),
        (0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF),
        (0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8),
        (0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2),
        (0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73),
        (0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB),
        (0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79),
        (0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08),
        (0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A),
        (0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E),
        (0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF),
        (0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16)
)

INVERSE_S_BOX = (
        (0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb),
        (0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb),
        (0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e),
        (0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25),
        (0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92),
        (0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84),
        (0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06),
        (0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b),
        (0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73),
        (0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e),
        (0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b),
        (0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4),
        (0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f),
        (0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef),
        (0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61),
        (0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d)
)

MDS_MATRIX = (
    (2, 3, 1, 1),
    (1, 2, 3, 1),
    (1, 1, 2, 3),
    (3, 1, 1, 2)
)

INVERSE_MDS_MATRIX = (
    (14, 11, 13, 9),
    (9, 14, 11, 13),
    (13, 9, 14, 11),
    (11, 13, 9, 14)
)

ROUND_CONSTANT = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]


def divide_into_blocks(text: bytes) -> List[bytes]:
    """
    :param text: Text to be divided into BLOCK_SIZE blocks and returned as a list of those blocks
    :return: A list of BLOCK_SIZE byte objects
    """
    output = []
    for block in range(len(text) // BLOCK_SIZE):
        output.append(text[block * BLOCK_SIZE: block * BLOCK_SIZE + BLOCK_SIZE])
    return output


def xor_bytes(first: iter, second: iter) -> bytearray:
    """
    Preforms a simple xor between the plain_text and key
    :param first:
    :param second:
    :return: xor product of first and second
    """
    output = bytearray()
    for byte1, byte2 in zip(first, second):
        output.append(byte1 ^ byte2)
    return output


def matrix_xor(first: List[List[int]], second: [List[List[int]]]):
    """
    preforms an xor operation between the two matrices and stores the values inside the first one (in place)
    :param first: matrix to be stored in
    :param second: matrix to be used for the xor operation
    :return: None
    """
    for i in range(MATRIX_DIMENSION):
        for j in range(MATRIX_DIMENSION):
            first[j][i] = first[j][i] ^ second[j][i]


def substitute_bytes(matrix: List[List[int]], inverse: bool):
    """
    Preform the SubBytes aes operation on a matrix
    Essentially preforms substitute_byte on every byte in our matrix
    :param matrix: The matrix to be transformed
    :param inverse: Indicating weather to use SubBytes function or its inverse
    :return: None
    """
    for i, row in enumerate(matrix):
        for j, cell in enumerate(row):
            matrix[i][j] = substitute_byte(cell, inverse)


def substitute_byte(number: int, inverse: bool) -> int:
    """
    Returns the fitting number from the S_box or Inverse_box
    :param number: number to be substituted
    :param inverse: Weather to return from inverse s_box or regular s_box
    :return: the fitting number from the fitting table
    """
    # Representing our byte as a binary number
    binary_string = str(bin(number))[2:]
    binary_string = (BYTE_SIZE - len(binary_string)) * '0' + binary_string

    row_index = int(binary_string[:BYTE_SIZE // 2], BINARY_BASE)
    column_index = int(binary_string[BYTE_SIZE // 2:], BINARY_BASE)

    return INVERSE_S_BOX[row_index][column_index] if inverse else S_BOX[row_index][column_index]


def create_matrix(block: bytes) -> List[List[int]]:
    """
    Represents our block using a 4x4 matrix of bytes with column order as follows:

    b0,b4,b8,b12
    b1,b5,b9,b13
    b2,b6,b10,b14
    b3,b7,b11,b15

    :param block: block to be represented as a matrix
    :return: a matrix representation of our block
    """
    output = [[0 for _ in range(MATRIX_DIMENSION)] for _ in range(MATRIX_DIMENSION)]    # Creating an empty 4x4 matrix
    for i in range(MATRIX_DIMENSION):
        for j in range(MATRIX_DIMENSION):
            output[j][i] = block[i * MATRIX_DIMENSION + j]
    return output


def shift_rows(matrix: List[List[int]], inverse: bool):
    """
    Preforms the shift rows function in place on the matrix
    :param matrix: The matrix representation of our block
    :param inverse: Decides weather to use the inverse function or not
    :return: None
    """
    for i in range(1, MATRIX_DIMENSION):    # Starting the loop at 1 as a shift of 0 is redundant
        matrix[i] = circular_shift(matrix[i], i if inverse else -i)


def mix_columns(matrix: List[List[int]], inverse: bool):
    """
    Preform the MixColumns aes operation on our matrix
    :param matrix: The matrix to be transformed
    :param inverse: a boolean indicating weather to use the mix_columns function or its inverse (encrypt/decrypt)
    :return: None
    """
    output = [[0 for _ in range(MATRIX_DIMENSION)] for _ in range(MATRIX_DIMENSION)]  # Creating an empty 4x4 matrix

    for i in range(MATRIX_DIMENSION):
        for j in range(MATRIX_DIMENSION):
            output[j][i] = matrix_multiplication(matrix, i, j, inverse)

    return output


def matrix_multiplication(matrix: List[List[int]], column_number: int, row_number: int, inverse: bool) -> int:
    """
    Multiples the MDS matrix against a column vector generating one cell for our mix columns matrix
    :param matrix: the matrix to be multiplied
    :param column_number: the column in the matrix to be multiplied
    :param row_number: the row number in the MDS matrix to be multiplied
    :param inverse: denotes which MDS matrix to use
    :return:
    """
    output = 0

    for column_index, cell in enumerate(INVERSE_MDS_MATRIX[row_number] if inverse else MDS_MATRIX[row_number]):
        temp = matrix[column_index][column_number]
        output ^= galois_multiplication(cell, temp)

    return output


def galois_multiplication(cell: int, number: int) -> int:
    """
    f(x) =
            {  number << 1 & 0xff ⊕ 0xb1, if number >= 127
            {  number << 1 & 0xff, if number < 127

    Using the rules of galois multiplication
    1 x number = 1
    2 x number = f(number)
    3 x number = (2 x number) ⊕ number = f(number) ⊕ number
    9 x number = number x 2 x 2 x 2 ⊕ number
    11 x number  = number x 2 x 2 ⊕ number x 2 ⊕ number
    13 x number  = number x 2 ⊕ number x 2 x 2 ⊕ number
    14 x number  = number x 2 ⊕ number x 2 ⊕ number x 2



    :param cell: the MDS matrix number to be multiplied against
    :param number: the number to multiply
    :return: A galois multiplication of the cell and number
    """
    return GALOIS_FIELD.Multiply(cell, number)


def circular_shift(row: List[int], shift_number: int):
    """
    Upward shift the right most column of the matrix
    :param row: The matrix to be operated upon
    :param shift_number:
    :return: None
    """
    temp = deque(row)
    temp.rotate(shift_number)
    return list(temp)


def key_schedule(key: List[List[int]], round_number: int) -> List[List[int]]:
    """
    :param key: matrix representation of the key
    :param round_number: indicates which round constant to use
    :return: A new key
    """
    output_key = [[0 for _ in range(MATRIX_DIMENSION)] for _ in range(MATRIX_DIMENSION)]

    # key schedule g function
    temp = [key[0][3], key[1][3], key[2][3], key[3][3]]    # temp = last column of key matrix
    temp = circular_shift(temp, -1)                        # circular shift
    for i, number in enumerate(temp):                      # substitute bytes
        temp[i] = substitute_byte(number, False)
    temp[0] ^= ROUND_CONSTANT[round_number]                # adding round constant

    key_first_column = [key[i][0] for i in range(MATRIX_DIMENSION)]
    output_key[0][0], output_key[1][0], output_key[2][0], output_key[3][0] = xor_bytes(key_first_column, temp)

    for i in range(1, MATRIX_DIMENSION):
        output_temp = [output_key[0][i-1], output_key[1][i-1], output_key[2][i-1], output_key[3][i-1]]
        key_temp = [key[0][i], key[1][i], key[2][i], key[3][i]]
        output_key[0][i], output_key[1][i], output_key[2][i], output_key[3][i] = xor_bytes(output_temp, key_temp)

    return output_key


def key_schedule_list(key: List[List[int]], number_of_rounds: int) -> List[List[List[int]]]:
    output = [key]
    for i in range(number_of_rounds):
        output.append(key_schedule(output[i], i))
    return output


def matrix_to_bytes(matrix: List[List[int]]) -> bytearray:
    output = bytearray()
    for i in range(MATRIX_DIMENSION):
        for j in range(MATRIX_DIMENSION):
            output.append(matrix[j][i])

    return output


def permutation(block_matrix: List[List[int]], inverse: bool):
    if inverse:
        block_matrix = mix_columns(block_matrix, inverse)
        shift_rows(block_matrix, inverse)
        substitute_bytes(block_matrix, inverse)
    else:
        substitute_bytes(block_matrix, inverse)
        shift_rows(block_matrix, inverse)
        block_matrix = mix_columns(block_matrix, inverse)

    return block_matrix


def encrypt(plain_text_block: bytes, key: bytes, number_of_rounds: int) -> str:
    key_list = key_schedule_list(create_matrix(key), number_of_rounds)  # Key expansion
    cipher_text = ''

    block_matrix = create_matrix(plain_text_block)
    matrix_xor(block_matrix, key_list[0])

    for i in range(1, number_of_rounds):
        block_matrix = permutation(block_matrix, False)
        matrix_xor(block_matrix, key_list[i])

    substitute_bytes(block_matrix, False)
    shift_rows(block_matrix, False)
    matrix_xor(block_matrix, key_list[number_of_rounds])

    cipher_text += matrix_to_bytes(block_matrix).hex()

    return cipher_text


def decrypt(cipher_text_block: bytes, key: bytes, number_of_rounds: int):
    key_list = key_schedule_list(create_matrix(key), number_of_rounds)
    cipher_text_block = create_matrix(cipher_text_block)

    matrix_xor(cipher_text_block, key_list[number_of_rounds])
    shift_rows(cipher_text_block, True)
    substitute_bytes(cipher_text_block, True)

    for i in range(number_of_rounds - 1, 0, -1):
        matrix_xor(cipher_text_block, key_list[i])
        cipher_text_block = mix_columns(cipher_text_block, True)
        shift_rows(cipher_text_block, True)
        substitute_bytes(cipher_text_block, True)

    matrix_xor(cipher_text_block, key_list[0])

    return matrix_to_bytes(cipher_text_block).hex()


def ecb(text: bytes, key: bytes, number_of_rounds: int, decipher: bool) -> str:
    block_list = divide_into_blocks(text)
    output = ''

    for block in block_list:
        output += decrypt(block, key, number_of_rounds) if decipher else encrypt(block, key, number_of_rounds)

    return output


if __name__ == '__main__':
    decrypted_text = ecb(CIPHER_TEXT, KEY, NUMBER_OF_ROUNDS, True)
    decoded_text = bytes.fromhex(decrypted_text).decode()
    print(bytes.fromhex(decrypted_text).decode())
