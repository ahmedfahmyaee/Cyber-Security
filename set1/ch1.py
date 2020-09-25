from base64 import b64encode

HEX_STRING = bytes.fromhex('49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d')


def hex_to_b64(text: bytes) -> str:
    return b64encode(text).decode()


if __name__ == '__main__':
    print(hex_to_b64(HEX_STRING))

