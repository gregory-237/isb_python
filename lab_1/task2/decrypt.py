from collections import Counter

f = open('files/encrypt_text.txt', 'r', encoding='utf-8')
ENCRYPT_TEXT = f.readline()

arr_encrypt_letters = [' ', 'Е', 'А', 'О', 'И', 'Н', 'Т', 'Р', 'С', 'В',
                       'М', 'П', 'Л', 'Д', 'Я', 'Ы', 'Х', 'Ь', 'К', 'Ч', 'Ф', 'У', 'З', 'Ж', 'Г', 'Ю',
                       'Б', 'Й', 'Ш', 'Э', 'Ц', 'Ъ', 'Щ']

def frequency(enc_text: str) -> list[list[str]]:
    """
    Returns list of different variations counts of letters in descending order

    :param enc_text:
    :return:
    """
    c = Counter(enc_text)
    dict_pairs = c.most_common()
    freq_variations = []
    for i in range(1, len(dict_pairs)):
        if dict_pairs[i - 1][1]  == dict_pairs[i][1]:
            freq_variations.append([tup[0] for tup in dict_pairs])
            tmp = dict_pairs[i - 1]
            dict_pairs[i - 1] = dict_pairs[i]
            dict_pairs[i] = tmp
            freq_variations.append([tup[0] for tup in dict_pairs])


    return freq_variations


def decrypt_text(text_for_decrypt: str, arr_decrypt_letters: list[str]) -> str:
    """
    Decrypt text using frequency analysis algorithm

    :param text_for_decrypt:
    :param arr_decrypt_letters:
    :return:
    """
    arr_encrypt_text = []

    dictionary = dict(zip(arr_decrypt_letters, arr_encrypt_letters))
    for symb in text_for_decrypt:
        arr_encrypt_text.append(dictionary[symb])
    text_for_decrypt = ''.join(arr_encrypt_text)
    return text_for_decrypt


def write_result() -> None:
    """
    Write decrypted text and keys in file
    :return:
    """
    with open('files/result.txt', 'a', encoding='utf-8') as f_result:
        f_result.write(f'{decrypt_text(ENCRYPT_TEXT, frequency(ENCRYPT_TEXT)[-1])}\n')
        keys = dict(zip(list(frequency(ENCRYPT_TEXT)[-1]), arr_encrypt_letters))
        f_result.write(f"code: {' '.join(keys.keys())}\n")
        f_result.write(f" key: {' '.join(keys.values())}")


if __name__ == "__main__":
    write_result()