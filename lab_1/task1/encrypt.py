ALPHABET = {
    "А": 0, "Б": 1, "В": 2, "Г": 3, "Д": 4, "Е": 5, "Ж": 6,
    "З": 7, "И": 8, "Й": 9, "К": 10, "Л": 11, "М": 12, "Н": 13,
    "О": 14, "П": 15, "Р": 16, "С": 17, "Т": 18, "У": 19, "Ф": 20,
    "Х": 21, "Ц": 22, "Ч": 23, "Ш": 24, "Щ": 25, "Ъ": 26, "Ы": 27,
    "Ь": 28, "Э": 29, "Ю": 30, "Я": 31, " ": 32
}

KEYWORD = 'СТУДЕНТ'

def encryption(keyword: str) -> str:
    """
    Encrypt text using upgraded Cesar algorithm
    :param keyword:
    :return:
    """

    encrypted = []

    with open('files/input.txt', 'r', encoding='utf-8') as input_file:
        input_text = input_file.readline()

    key_long = keyword * (len(input_text) // len(keyword)) + keyword[:len(input_text) % len(keyword)]

    for letter, key in zip(input_text, key_long):
        encrypted.append(''.join((symbol for symbol, code in ALPHABET.items() if code == (ALPHABET[letter] + ALPHABET[key]) % 33)))

    return ''.join(encrypted)


def write_result(keyword: str) -> None:
    """
    Write encrypted text and keyword in file
    :param keyword:
    :return:
    """
    with open('files/encrypt.txt', 'a', encoding='utf-8') as result_file:
        result_file.write(f'{encryption(keyword)}\n')
        result_file.write(f'KEYWORD: {keyword}')


if __name__ == "__main__":
    write_result(KEYWORD)