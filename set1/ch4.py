import math
from set1.ch3 import decipher
from set1.ch3 import fitting_quotient


def solution() -> str:

    # Creating an array of deciphered single byte xor strings from our file
    strings = []

    with open('ch4_hex_files.txt', 'r') as f:
        # Running single byte xor deciphering on each string in the file
        for line in f:
            strings.append(decipher(bytes.fromhex(line))[0])

        # Finding the most likely string to be english using the fitting quotient function
        output = ''
        minimum_quotient = math.inf
        for string in strings:
            current_quotient = fitting_quotient(string)
            if current_quotient < minimum_quotient:
                minimum_quotient, output = current_quotient, string

    return output.strip()


if __name__ == '__main__':
    print(solution())
