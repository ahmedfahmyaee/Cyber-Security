"""
This is a command line program that can be used to decrypt and encrypt a text using the Ceaser Cipher
"""

import argparse
from string import ascii_lowercase
from string import ascii_uppercase

# Creating two lists of the alphabet for both lower case and upper case
UPPER_CASE_ALPHABET = list(ascii_uppercase)
LOWER_CASE_ALPHABET = list(ascii_lowercase)
ALPHABET_SIZE = 26

# Creating the command line argument parser
parser = argparse.ArgumentParser(description='Decrypt/Encrypt Ceaser cipher. If no decrypt or encrypt flag is given the default is to encrypt')
parser.add_argument('-k', '--key', type=int, required=True, help='Key used in the cipher')
parser.add_argument('-t', '--text', type=str, required=True, help='The text to be encrypted/decrypted')

# Creating flags
group = parser.add_mutually_exclusive_group()
group.add_argument('-d', '--decrypt', action='store_true', help='Decrypt the text given')
group.add_argument('-e', '--encrypt', action='store_true', help='Encrypt the text given')

# Parsing the arguments
args = parser.parse_args()


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
        elif char.islower():
            index = LOWER_CASE_ALPHABET.index(char)
            if decrypt:
                output += LOWER_CASE_ALPHABET[(index - key) % ALPHABET_SIZE]
            else:
                output += LOWER_CASE_ALPHABET[(index + key) % ALPHABET_SIZE]
        else:
            index = UPPER_CASE_ALPHABET.index(char)
            if decrypt:
                output += UPPER_CASE_ALPHABET[(index - key) % ALPHABET_SIZE]
            else:
                output += UPPER_CASE_ALPHABET[(index + key) % ALPHABET_SIZE]
    return output


if __name__ == '__main__':
    print()
    print(cipher(args.text, args.key, args.decrypt))

