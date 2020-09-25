from base64 import b64decode
from typing import List
from set1.ch3 import decipher

MIN_KEY_SIZE = 2
MAX_KEY_SIZE = 40

with open('ch6_b64.txt', 'r') as f:
    CIPHER_TEXT = b64decode(f.read())

"""
Returns binary string representation of a bytes object
"""


def bit_string(text: bytes) -> str:
    output = ''
    for byte in text:
        temp = str(bin(byte))[2:]
        output += ((8 - len(temp)) * '0') + temp
    return output


"""
Returns the hamming distance between two byte objects AKA the number of differing bits between them
"""


def hamming_distance(text1: bytes, text2: bytes) -> int:
    count = 0
    for bit1, bit2 in zip(bit_string(text1), bit_string(text2)):
        if bit1 != bit2:
            count += 1
    return count


def normalized_list(text: bytes) -> List[float]:
    output = []
    for key_size in range(MIN_KEY_SIZE, MAX_KEY_SIZE):
        first = text[0:key_size]
        second = text[key_size:key_size * 2]
        output.append(hamming_distance(first, second) / key_size)
    return output


def get_key(key_list: List[float]) -> int:
    return key_list.index(min(key_list)) + 2


def blockify(cipher_text: bytes, key: int):
    array = []
    for i in range(len(cipher_text) // key):
        array.append(cipher_text[i * key: i * key + key])
    return array


def solve(cipher_text: bytes) -> bytes:
    blocked_list = blockify(cipher_text, get_key(normalized_list(cipher_text)))
    output = ''
    for i in range(len(blocked_list[0])):
        to_solve = ''
        for block in blocked_list:
            to_solve += str(block[i])
        output += str(decipher(bytes(to_solve.encode()))[0])
    return bytes(output.encode())


print(solve(CIPHER_TEXT))





