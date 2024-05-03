import json
import logging

logging.basicConfig(level=logging.INFO)


def serialize_key(key: bytes, key_path: str) -> None:
    """
    Serialize the key and save it to a file.

    :param key: The key to be serialized.
    :param key_path: The path where the serialized key will be saved.
    """
    try:
        with open(key_path, 'wb') as key_file:
            key_file.write(key)
    except Exception as ex:
        logging.error(f"Incorrect path - {ex}")


def deserialize_key(key_path: str) -> bytes:
    """
    Deserialize the key from a file.

    :param key_path: The path from where to deserialize the key.
    :return: The deserialized key.
    """
    try:
        with open(key_path, 'rb') as key_file:
            return key_file.read()
    except Exception as ex:
        logging.error(f"Incorrect path - {ex}")


def read_text_file(text_path: str, mode: str, encoding=None) -> str:
    """
    Read text from a file.

    :param text_path: The path to the text file.
    :param mode: The mode to open the file in.
    :param encoding: (str, optional) The encoding of the text file. Defaults to None .

    :return: The content of the text file.
    """
    try:
        with open(text_path, mode=mode, encoding=encoding) as file:
            return file.read()
    except Exception as ex:
        logging.error(f"Incorrect path - {ex}")


def write_text_file(text: str, path: str) -> None:
    """
    Write text to a file.

    :param text: The text to write to the file.
    :param path: The path to the file.
    """
    try:
        with open(path, 'wb') as file:
            file.write(text)
    except Exception as ex:
        logging.error(f"Incorrect path - {ex}")


def read_json_file(path: str) -> dict:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            paths = json.load(f)
        return paths
    except Exception as ex:
        logging.error(f"Incorrect path - {ex}")
