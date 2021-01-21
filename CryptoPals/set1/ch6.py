from base64 import b64decode
from operator import itemgetter
from set1.ch3 import decipher

MIN_KEY_SIZE = 2
MAX_KEY_SIZE = 41
NUMBER_OF_KEYS = 1

with open('ch6_b64.txt') as f:
    CIPHER_TEXT = b64decode(f.read())


def bit_string(text: bytes) -> str:
    """
    Returns binary string representation of a bytes object
    """
    output = ''
    for byte in text:
        temp = str(bin(byte))[2:]
        output += ((8 - len(temp)) * '0') + temp
    return output


def hamming_distance(text1: bytes, text2: bytes) -> int:
    """
    Returns the hamming distance between two byte objects AKA the number of differing bits between them
    """
    count = 0
    for bit1, bit2 in zip(bit_string(text1), bit_string(text2)):
        if bit1 != bit2:
            count += 1
    return count


def normalized_hamming_distance(text: bytes, key_size: int) -> tuple[float, int]:
    distances = []
    blocked_text = divide_to_blocks(text, key_size)
    length = len(blocked_text)

    for i in range(0, length if length % 2 == 0 else length - 1, 2):
        distances.append(hamming_distance(blocked_text[i], blocked_text[i + 1]) / key_size)
    return sum(distances) / len(distances), key_size


def divide_to_blocks(text: bytes, block_size: int) -> list[bytes]:
    output = []
    for i in range(len(text) // block_size):
        output.append(text[i * block_size: i * block_size + block_size])
    return output


def n_smallest_key_sizes(text: bytes, n: int) -> list[int]:
    temp = []
    for i in range(MIN_KEY_SIZE, MAX_KEY_SIZE):
        temp.append(normalized_hamming_distance(text, i))
    temp.sort(key=itemgetter(0))

    keys = []
    for i in range(n):
        keys.append(temp[i][1])
    return keys


if __name__ == '__main__':
    possible_keys = n_smallest_key_sizes(CIPHER_TEXT, NUMBER_OF_KEYS)
    plain_text = ''

    for possible_key in possible_keys:
        blocked_output = []
        divided_text = divide_to_blocks(CIPHER_TEXT, possible_key)

        for i in range(possible_key):
            temp = bytearray()
            for block in divided_text:
                temp.append(block[i])
            blocked_output.append(decipher(temp)[0].decode())

        for i in range(possible_key):
            for block in blocked_output:
                plain_text += block[i]

    print(plain_text)
