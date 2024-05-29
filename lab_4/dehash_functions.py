import hashlib
import logging
import time
import multiprocessing as mp
import matplotlib.pyplot as plt

from tqdm import tqdm

from utility import write_json_file, read_json_file

logging.basicConfig(level=logging.INFO)


def check_hash(x: int, bins: tuple, hash: str, last_numbers: str) -> tuple:
    """Hash verification function

    :param x: (int) the intended digits of the card number
    :param bins: (tuple) a tuple with the intended BIN
    :param hash: (str) hash value
    :param last_numbers: (str) the last 4 digits of the number
    :return tuple: in case of a match, a tuple with the BIN, the correct number and the last digits.
    """
    x = str(x).zfill(6)
    for bin in bins:
        if hashlib.sha256(f"{bin}{x}{last_numbers}".encode()).hexdigest() == hash:
            return bin, x, last_numbers


def find_card_data(bins: tuple, hash: str, last_numbers: str, data_path: str) -> str:
    """Card data search function

    :param bins: (tuple) a tuple with the intended BIN
    :param hash: (str) hash value
    :param last_numbers: (str) the last 4 digits of the number
    :param data_path: (str) the path to card data
    :return str: card number in the form of a string.
    """
    try:
        with mp.Pool(processes=mp.cpu_count()) as p:
            for result in p.starmap(check_hash, [(i, bins, hash, last_numbers) for i in range(0, 1000000)]):
                if result:
                    logging.info(f'Number of card: {result[0]}-{result[1]}-{result[2]}')
                    p.terminate()
                    write_json_file(data_path, {"card_number": f'{result[0]}{result[1]}{result[2]}'})
                    return f'{result[0]}{result[1]}{result[2]}'
    except Exception as ex:
        logging.error(f"The card data couldn't be found: {ex}\n")


def luhn_algorithm(card_numbers: str) -> bool:
    """Function that checks the card number using the Luhn algorithm
    :param card_numbers: (int) Card number
    :return bool: boolean value of match/non-match
    """
    try:
        result = int(card_numbers[-1])
        list_numbers = [int(i) for i in (card_numbers[::-1])]
        for i, num in enumerate(list_numbers):
            if i % 2 == 0:
                mul = num * 2
                if mul > 9:
                    mul -= 9
                list_numbers[i] = mul
        total_sum = sum(list_numbers)
        rem = total_sum % 10
        check_sum = 10 - rem if rem != 0 else 0

        if check_sum == result:
            logging.info("Card is existing by Luhn algorithm.")
            return True
        else:
            logging.info("Card is not existing by Luhn algorithm.")
            return False
    except Exception as ex:
        logging.error(f"An error occurred while executing the luhn algorithm: {ex}\n")


def time_measurement(bins: tuple, hash: str, last_numbers: str) -> None:
    """Function for measuring time and drawing a graph depending on the number of processes

    :param bins: (tuple) a tuple with the intended BIN
    :param hash: (str) hash value
    :param last_numbers: (str) the last 4 digits of the number
    :return:
    """
    try:
        times_list = []
        for i in tqdm(range(1, int(mp.cpu_count() * 1.5)), desc="Processes"):
            start = time.time()
            with mp.Pool(processes=i) as p:
                for result in p.starmap(check_hash, [(i, bins, hash, last_numbers) for i in range(0, 1000000)]):
                    if result:
                        end = time.time() - start
                        times_list.append(end)
                        p.terminate()
                        break
        fig = plt.figure(figsize=(15, 5))
        plt.plot(
            range(len(times_list)),
            times_list,
            linestyle=":",
            color="black",
            marker="x",
            markersize=10,
        )
        plt.bar(range(len(times_list)), times_list)
        plt.xlabel("Processes")
        plt.ylabel("Time in seconds")
        plt.title("The dependence of processes on time")
        plt.show()
    except Exception as ex:
        logging.error(f"An error occurred when measuring time and drawing a graph: {ex}\n")


if __name__ == "__main__":
    settings = read_json_file('default_settings.json')
    result = find_card_data(settings["bins"], settings["hash"], settings["last_numbers"], settings["card_number_path"])
    luhn_algorithm(result)
    time_measurement(settings["bins"], settings["hash"], settings["last_numbers"])
