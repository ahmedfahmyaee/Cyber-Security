"""
This is a command line program that can be used to decrypt and encrypt a text using the Caesar Cipher
This can additionally be used to break Caesar Cipher encryption without an encryption key using frequency analysis
"""

import math
import argparse
from collections import Counter
from string import ascii_lowercase
from typing import Tuple, List

ALPHABET = ascii_lowercase
ALPHABET_SIZE = 26
LETTER_OCCURRENCE = {
    'a': 8.2389258,    'b': 1.5051398,    'c': 2.8065007,    'd': 4.2904556,
    'e': 12.813865,    'f': 2.2476217,    'g': 2.0327458,    'h': 6.1476691,
    'i': 6.1476691,    'j': 0.1543474,    'k': 0.7787989,    'l': 4.0604477,
    'm': 2.4271893,    'n': 6.8084376,    'o': 7.5731132,    'p': 1.9459884,
    'q': 0.0958366,    'r': 6.0397268,    's': 6.3827211,    't': 9.1357551,
    'u': 2.7822893,    'v': 0.9866131,    'w': 2.3807842,    'x': 0.1513210,
    'y': 1.9913847,    'z': 0.0746517
}


def cipher(text: str, key: int, decrypt: bool) -> str:
    """
    Using the schema A-> 0, B-> 1, C-> 2 ... Z -> 25
    We can decipher the letter x being given the key k using the formula:
    D(x) = (x - k) mod 26
    Similarly we can encrypt the letter x given the key k using the formula:
    E(x) = (x + k) mod 26
    :param text: text to be encrypted/decrypted
    :param key: the key to be used
    :param decrypt: a boolean value indicating weather to encrypt or decrypt
    :return: the cipher text
    """
    output = ''

    for char in text:
        # If the character is not in the english alphabet don't change it.
        if not char.isalpha():
            output += char
            continue

        index = ALPHABET.index(char.lower())

        if decrypt:
            new_char = ALPHABET[(index - key) % ALPHABET_SIZE]
        else:
            new_char = ALPHABET[(index + key) % ALPHABET_SIZE]

        # Setting the right case for the letter and adding it to the output
        output += new_char.upper() if char.isupper() else new_char

    return output


def create_brute_force_array(text: str) -> List[str]:
    """
    Creating an array which contains all possible deciphering shifts
    :param text: text to be shifted
    :return: an array which contains all possible deciphering shifts
    """
    return [cipher(text, key, True) for key in range(ALPHABET_SIZE)]


def fitting_quotient(text: str) -> float:
    """
    Finds the fitting quotient of a text
    This is used to approximate how close a sentence is to english using frequency analysis
    :param text: text to be used
    :return: fitting quotient
    """
    counter = Counter(text)
    dist_text = [counter.get(ch, 0) * 100 / len(text) for ch in LETTER_OCCURRENCE]
    return sum([abs(a-b) for a, b in zip(list(LETTER_OCCURRENCE.values()), dist_text)]) / ALPHABET_SIZE


def brute_force_decipher(text: str) -> Tuple[str, int]:
    """
    Brute forces Caesar Cipher using frequency analysis
    Works poorly with short sentences or words
    :param text: cipher text
    :return: guessed plain text using frequency analysis
    """

    outputs = create_brute_force_array(text)
    minimum_frequency = math.inf
    original_text = ''
    encryption_key = 0

    for key, output in enumerate(outputs):
        frequency = fitting_quotient(output)

        if frequency < minimum_frequency:
            minimum_frequency, original_text = frequency, output
            encryption_key = key

    return original_text, encryption_key


def parse() -> argparse.ArgumentParser:
    """
    Creates a parser and parses the command line arguments passed to the program
    :return: configured ArgumentParser object
    """
    # Creating the command line argument parser
    parser = argparse.ArgumentParser(description='Decrypt/Encrypt Caesar cipher. If no decrypt or encrypt flag is given the default is to encrypt (In case the brute force option is chose there\'s no need to specify any other flag)')
    parser.add_argument('text', type=str, help='The text to be encrypted/decrypted')
    parser.add_argument('-k', '--key', type=int, required=False, help='Key used in the cipher')
    parser.add_argument('-b', '--bruteforce', action='store_true', help='Brute force all options and output a guess using frequency analysis')
    parser.add_argument('-l', '--bruteforcelist', action='store_true', help='Output all brute forced options in addition to the guess (Can only be used with the -b flag)')

    # Creating flags
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-d', '--decrypt', action='store_true', help='Decrypt the text given')

    # Returning the parsed arguments
    return parser


if __name__ == '__main__':
    # Getting the command line arguments
    configured_parser = parse()
    args = configured_parser.parse_args()

    if args.bruteforce:
        if args.bruteforcelist:
            shifts = create_brute_force_array(args.text)
            for i, shift in enumerate(shifts):
                print(f'Key:{i}, Text: {shift}')
        print('\nGuess:')
        guessed_text, guessed_key = brute_force_decipher(args.text)
        print(f'Text: {guessed_text}\nKey: {guessed_key}')
    else:
        if args.key is None:
            configured_parser.error('Specifying a key (-k) is required when not using brute force options (-b)')
        if args.bruteforcelist:
            configured_parser.error('Cannot use (-l) option when not using (-b) option')
        print(cipher(args.text, args.key, args.decrypt))
