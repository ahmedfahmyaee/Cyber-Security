"""
This is a command line program that can be used to decrypt and encrypt a text using the Ceaser Cipher
This can additionally be used to break Ceaser Cipher encryption without an encryption key using frequency analysis
"""

import math
import argparse
from collections import Counter
from string import ascii_lowercase
from typing import Tuple, List

ALPHABET = ascii_lowercase
ALPHABET_SIZE = 26
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


"""
Using the schema A-> 0, B-> 1, C-> 2 ... Z -> 25
We can decipher the letter x being given the key k using the formula:
D(x) = (x - k) mod 26
Similarly we can encrypt the letter x given the key k using the formula:
E(x) = (x + k) mod 26
"""


def cipher(text: str, key: int, decrypt: bool) -> str:
    output = ''

    for char in text:
        # If the character is not in the english alphabet don't change it.
        if not char.isalpha():
            output += char
            continue

        index = ALPHABET.index(char.lower())

        if decrypt:
            char = ALPHABET[(index - key) % ALPHABET_SIZE]
        else:
            char = ALPHABET[(index + key) % ALPHABET_SIZE]

        # Setting the right case for the letter
        if not char.islower():
            char = char.upper()
        output += char

    return output


"""
Creating an array which contains all possible deciphering shifts
"""


def create_brute_force_array(text: str) -> List[str]:
    return [cipher(text, i, True) for i in range(ENGLISH_ALPHABET_SIZE)]


"""
Finds the fitting quotient of a text
This is used to approximate how close a sentence is to english using frequency analysis
"""


def fitting_quotient(text: bytes) -> float:
    counter = Counter(text)
    dist_text = [(counter.get(ord(ch), 0) * 100) / len(text) for ch in LETTER_OCCURRENCE]
    return sum([abs(a - b) for a, b in zip(list(LETTER_OCCURRENCE.values()), dist_text)]) / ENGLISH_ALPHABET_SIZE


"""
Brute forces Ceaser Cipher using frequency analysis
Works poorly with short sentences or words
"""


def brute_force_decipher(text: str) -> Tuple[str, int]:

    outputs = create_brute_force_array(text)
    minimum_frequency = math.inf
    original_text = ''
    encryption_key = 0

    for i, output in enumerate(outputs):
        frequency = fitting_quotient(bytes(output.encode()))

        if frequency < minimum_frequency:
            minimum_frequency, original_text = frequency, output
            encryption_key = i

    return original_text, encryption_key


"""
Creates a parser and parses the command line arguments passed to the program
"""


def parse():
    # Creating the command line argument parser
    parser = argparse.ArgumentParser(description='Decrypt/Encrypt Ceaser cipher. If no decrypt or encrypt flag is given the default is to encrypt')
    parser.add_argument('text', type=str, help='The text to be encrypted/decrypted')
    parser.add_argument('-k', '--key', type=int, required=False, help='Key used in the cipher')

    # Creating flags
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-d', '--decrypt', action='store_true', help='Decrypt the text given')
    group.add_argument('-e', '--encrypt', action='store_true', help='Encrypt the text given')
    parser.add_argument('-b', '--bruteforce', action='store_true', help='Brute force all options and output guess using frequency analysis')

    # Returning the parsed arguments
    return parser


if __name__ == '__main__':
    # Getting the command line arguments
    configured_parser = parse()
    args = configured_parser.parse_args()

    if args.bruteforce:
        text, key = brute_force_decipher(args.text)
        print(f'Text: {text}\nKey: {key}')
    else:
        if args.key is None:
            configured_parser.error('Specifying a key (-k) is required when not using brute force options (-b)')
        print(cipher(args.text, args.key, args.decrypt))

        
        
