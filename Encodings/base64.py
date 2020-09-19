from string import ascii_lowercase
from string import ascii_uppercase


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
Encodes a text into base64
"""


def encode(text: bytes) -> str:
    encodes = ascii_uppercase + ascii_lowercase + '0123456789' + '+/'
    output = ''
    sequence = bit_string(text)     # Bit representation of the text

    padding = ''
    extra = len(sequence) % 6   # For measuring how much padding needs to be added
    if extra != 0:
        padding += (6 - extra) // 2 * '='   # Calculating the needed padding
        sequence += (6 - extra) * '0'

    for i in range(len(sequence) // 6):     # Encoding each 6 bits into their fitting representation
        output += encodes[int(sequence[i * 6:i * 6 + 6], 2)]
    return output + padding


"""
Decodes a base64 string into bytes
"""


def decode(text: str) -> bytes:
    output = ''
    decodes = ascii_uppercase + ascii_lowercase + '0123456789' + '+/'
    padding_number = 0

    for ch in text:
        if ch != '=':
            bin_number = bin(decodes.index(ch))[2:]
            output += (6-len(bin_number)) * '0' + bin_number
        else:
            padding_number += 1

    if padding_number != 0:     # Remove the added bits do to padding if exists
        output = output[:-padding_number * 2]
    return int(output, 2).to_bytes(len(output) // 8, byteorder='big')   # Convert bit string to bytes object

