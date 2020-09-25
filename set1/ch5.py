from itertools import cycle

SENTENCE = str.encode("Burning 'em, if you ain't quick and nimble I go crazy when I hear a cymbal")
KEY = str.encode('ICE')


def repeating_key_xor(text: bytes, key: bytes) -> bytes:
    output = bytearray()
    key_iterator = cycle(key)
    for byte in text:
        output.append(byte ^ next(key_iterator))
    return bytes(output)


if __name__ == '__main__':
    print(repeating_key_xor(SENTENCE, KEY).hex())

