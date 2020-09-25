def xor_combination(buffer1: bytes, buffer2: bytes) -> bytearray:
    result = bytearray()
    for b1, b2 in zip(buffer1, buffer2):
        result.append(b1 ^ b2)
    return result


if __name__ == '__main__':
    buff1 = bytes.fromhex('1c0111001f010100061a024b53535009181c')
    buff2 = bytes.fromhex('686974207468652062756c6c277320657965')

    print(xor_combination(buff1, buff2).hex())

