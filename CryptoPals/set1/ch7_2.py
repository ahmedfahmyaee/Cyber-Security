"""
An AES ECB decryption and encryption program using pycryptodome library
"""

from Crypto.Cipher import AES
from base64 import b64decode, b64encode

with open(r'D:\PycharmProjects\CryptoPals\set1\ch7_b64.txt', 'r') as f:
    CIPHER_TEXT = b64decode(f.read())
KEY = 'YELLOW SUBMARINE'.encode()


def decrypt_ecb(key: bytes, cipher_text: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(cipher_text)


def encrypt_ecb(key: bytes, plain_text: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_ECB)
    return b64encode(cipher.encrypt(plain_text))


if __name__ == '__main__':
    print('Decrypted plain text:')
    print(decrypt_ecb(KEY, CIPHER_TEXT).decode())
