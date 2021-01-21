import math
from set1.WordScorer import WordScorer
from collections import Counter
from typing import Tuple


BYTES_HEX_STRING = bytes.fromhex('1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736')
BYTE_SIZE = 256
ENGLISH_ALPHABET_SIZE = 26
LETTER_OCCURRENCE = {
    'a': 8.2389258,    'b': 1.5051398,    'c': 2.8065007,    'd': 4.2904556,
    'e': 12.813865,    'f': 2.2476217,    'g': 2.0327458,    'h': 6.1476691,
    'i': 6.1476691,    'j': 0.1543474,    'k': 0.7787989,    'l': 4.0604477,
    'm': 2.4271893,    'n': 6.8084376,    'o': 7.5731132,    'p': 1.9459884,
    'q': 0.0958366,    'r': 6.0397268,    's': 6.3827211,    't': 9.1357551,
    'u': 2.7822893,    'v': 0.9866131,    'w': 2.3807842,    'x': 0.1513210,
    'y': 1.9913847,    'z': 0.0746517
}


def fitting_quotient(text: bytes) -> float:
    """
    Finds the fitting quotient of a text
    This is used to approximate how close a sentence is to english using frequency analysis
    """
    counter = Counter(text)
    dist_text = [(counter.get(ord(ch), 0) * 100) / len(text) for ch in LETTER_OCCURRENCE]
    return sum([abs(a - b) for a, b in zip(list(LETTER_OCCURRENCE.values()), dist_text)]) / ENGLISH_ALPHABET_SIZE


def single_byte_xor(text: bytes, key: int):
    return bytes([b ^ key for b in text])


def decipher(text: bytes) -> Tuple[bytes, int]:
    minimum_frequency = math.inf
    original_text = ''
    encryption_key = 0

    for key in range(BYTE_SIZE):
        decrypted_text = single_byte_xor(text, key)
        frequency = fitting_quotient(decrypted_text)

        if frequency < minimum_frequency:
            minimum_frequency, original_text = frequency, decrypted_text
            encryption_key = key

    return original_text, encryption_key


if __name__ == '__main__':
    plain_text, guessed_key = decipher(BYTES_HEX_STRING)
    print(f'Hidden text: {plain_text.decode()}')
    print(f'Key: {guessed_key}')

    # TODO test this piece of shit
    # test = [single_byte_xor(BYTES_HEX_STRING, i) for i in range(BYTE_SIZE)]
    # for i, output in enumerate(test):
    #     print(f'{i}, {output}')
    # print(WordScorer.guessed_word_from_list(test))









