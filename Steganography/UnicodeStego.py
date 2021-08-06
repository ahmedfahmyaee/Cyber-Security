"""
This is a program for hiding and extracting hidden messages using unicode steganography
We use the mapping of:
ZERO WIDTH NON JOINER - U+200C: 0
ZERO WIDTH SPACE - U+200B: 1
With 0 and 1 indicating bit values
For hiding the message we simply put all the unicode values in the end of the string using the table above to represent
our message in binary

Note: This isn't a good implementation of unicode steganography, it was made to further my understanding of the subject

Useful information: https://en.wikipedia.org/wiki/Unicode
                    https://www.fontspace.com/unicode/analyzer
                    Unicode analyzer is a nice tool to further look into the hidden message and detect it
"""
import pyperclip
import argparse

ZERO_WIDTH_NON_JOINER = '\u200C'
ZERO_WIDTH_SPACE = '\u200B'
CHARACTER_ENCODING = 'utf-8'
BINARY_BLOCK_SIZE = 8
BINARY_BASE = 2
DECIPHER_TABLE = {ZERO_WIDTH_NON_JOINER: '0', ZERO_WIDTH_SPACE: '1'}
CIPHER_TABLE = {'0': ZERO_WIDTH_NON_JOINER, '1': ZERO_WIDTH_SPACE}


def bit_string(text: bytes) -> str:
    """
    :param text: text to be turned into a binary string
    :return: a binary string
    """
    return ''.join(['{:08b}'.format(letter) for letter in text])


def decipher(cipher_text: str) -> str:
    """
    The function gets a text with hidden unicode values inside as described above and decodes the message
    :param cipher_text: text with hidden message
    :return: the extracted message
    """
    binary_string = output = ''

    # Extracting the binary string hidden in the text
    for ch in cipher_text:
        if ch == ZERO_WIDTH_NON_JOINER or ch == ZERO_WIDTH_SPACE:
            binary_string += DECIPHER_TABLE[ch]

    # Parsing the string in 8 bit chunks
    while binary_string:
        output += chr(int(binary_string[:BINARY_BLOCK_SIZE], BINARY_BASE))
        binary_string = binary_string[BINARY_BLOCK_SIZE:]

    return output


def cipher(regular_text: str, hidden_text: str) -> str:
    """
    Hides a secret message inside the text using the method described above
    :param regular_text: The normal text of the message
    :param hidden_text: the message to be hidden inside
    :return: the regular string with a hidden message inside
    """
    binary_string = bit_string(hidden_text.encode(CHARACTER_ENCODING))

    # Hiding the unicode characters at the end of the string
    for bit in binary_string:
        regular_text += CIPHER_TABLE[bit]

    return regular_text


def configure_parser() -> argparse.ArgumentParser:
    # Creating the command line argument parser
    parser = argparse.ArgumentParser(description='This is a program for hiding and extracting hidden messages using unicode steganography (more detailed info in the source code)')
    parser.add_argument('text', type=str, help='The text to be encrypted/decrypted')
    parser.add_argument('-s', '--secret', type=str, required=False, help='The secret to encrypt if using the -e option')

    # Creating flags
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-d', '--decrypt', action='store_true', help='Decrypt the text given')
    group.add_argument('-e', '--encrypt', action='store_true', help='Encrypt the text using a given secret')

    # Returning the parsed arguments
    return parser


if __name__ == '__main__':
    configured_parser = configure_parser()
    args = configured_parser.parse_args()

    if args.decrypt:
        print(decipher(args.text))
    else:
        if not args.secret:
            configured_parser.error('Please specify a secret when encrypting')
        pyperclip.copy((cipher(args.text, args.secret)))
