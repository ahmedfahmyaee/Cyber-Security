from string import ascii_lowercase
from string import ascii_uppercase

ENCODING = ascii_uppercase + ascii_lowercase + '0123456789' + '+/'


def bit_string(text: bytes) -> str:
    """
    Returns binary string representation of a bytes object
    :param text:
    :return: binary string
    """
    output = ''
    for byte in text:
        temp = str(bin(byte))[2:]
        output += ((8 - len(temp)) * '0') + temp
    return output


def encode(text: bytes) -> str:
    """
    Encodes a text into base64
    :param text: text to be encoded
    :return: base64 encoded text
    """
    output = ''
    sequence = bit_string(text)     # Bit representation of the text

    padding = ''
    extra = len(sequence) % 6   # For measuring how much padding needs to be added
    if extra != 0:
        padding += (6 - extra) // 2 * '='   # Calculating the needed padding
        sequence += (6 - extra) * '0'

    for i in range(len(sequence) // 6):     # Encoding each 6 bits into their fitting representation
        output += ENCODING[int(sequence[i * 6:i * 6 + 6], 2)]
    return output + padding


def decode(text: str) -> bytes:
    """
    Decodes a base64 string into bytes
    :param text: text to be decoded
    :return: bytes object representing decoded text
    """
    output = ''
    padding_number = 0

    for ch in text:
        if ch != '=':
            bin_number = bin(ENCODING.index(ch))[2:]
            output += (6-len(bin_number)) * '0' + bin_number
        else:
            padding_number += 1

    if padding_number != 0:     # Remove the added bits due to padding if exists
        output = output[:-padding_number * 2]
    return int(output, 2).to_bytes(len(output) // 8, byteorder='big')   # Convert bit string to bytes object
