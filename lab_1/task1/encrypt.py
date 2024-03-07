from sys import argv
from constants import ALPHABET
import logging

KEYWORD = str(argv[1])
logging.basicConfig(level=logging.INFO)


def encryption(keyword: str, path: str) -> str:
    """
    Encrypt text using upgraded Caesar algorithm
    :param path:
    :param keyword:
    :return:
    """

    encrypted = []

    try:
        with open(path, 'r', encoding='utf-8') as input_file:
            input_text = input_file.readline()
    except Exception as ex:
        logging.error(f"File can't be open or was not found: {ex}\n")

    key_long = keyword * (len(input_text) // len(keyword)) + keyword[:len(input_text) % len(keyword)]

    for letter, key in zip(input_text, key_long):
        encrypted.append(''.join((symbol for symbol, code in ALPHABET.items() if code == (ALPHABET[letter] + ALPHABET[key]) % 33)))

    return ''.join(encrypted)


def write_result(keyword: str, path_encrypt: str, path_key: str, path_input: str) -> None:
    """
    Write encrypted text and keyword in file
    :param path_input:
    :param path_key:
    :param path_encrypt:
    :param keyword:
    :return:
    """
    try:
        with open(path_encrypt, 'w', encoding='utf-8') as encrypt_file:
            encrypt_file.write(f'{encryption(keyword, path_input)}\n')
    except Exception as ex:
        logging.error(f"Error in encryption or file can't be open or was not found: {ex}\n")

    try:
        with open(path_key, 'w', encoding='utf-8') as key_file:
            key_file.write(f'KEYWORD: {keyword}')
    except Exception as ex:
        logging.error(f"Error in encryption or file can't be open or was not found: {ex}\n")


if __name__ == "__main__":
    try:
        write_result(KEYWORD, 'files/encrypt.txt', 'files/key.txt', 'files/input.txt')
        logging.info(f"Text successfully encrypted and saved to file")
    except Exception as ex:
        logging.error(f"Error in encryption or file can't be open or was not found: {ex}\n")

