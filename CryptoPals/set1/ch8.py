from set1.Util import divide_into_blocks


def repeat_block_count(text: str, block_size: int):
    """
    Return the number of repeated blocks of block_size size in text
    :param text: text to be used
    :param block_size: size of blocks
    :return: number of repeated blocks
    """
    divided_text = divide_into_blocks(text, block_size)
    repeated_blocks = set(divided_text)

    return len(divided_text) - len(repeated_blocks)


def detect_aes_ecb(path: str, block_size=16) -> str:

    max_counter = 0
    encrypted_text = ''

    for line in open(path, 'r'):
        line = line.strip()
        current_counter = repeat_block_count(line, block_size)
        if current_counter > max_counter:
            max_counter, encrypted_text = current_counter, line

    return encrypted_text


if __name__ == '__main__':
    output = detect_aes_ecb('ch8_hex_files.txt')
    print('Detected ECB here:')
    print(output)
