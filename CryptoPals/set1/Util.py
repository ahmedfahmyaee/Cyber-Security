from typing import List, Union


def divide_into_blocks(text: Union[bytes, bytearray, str], block_size: int) -> List[bytes]:
    """
    Assumes text % block_size = 0 (otherwise the last text % block_size of text will be omitted)
    :param text: Text to be divided into block_size blocks and returned as a list of those blocks
    :param block_size size of blocks
    :return: A list of block_size byte objects
    """
    return [text[i * block_size: i * block_size + block_size] for i in range(len(text) // block_size)]

