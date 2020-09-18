from bow import bow_colletcor

import threading
import yaml
import sys


def load_yaml(filename):

    with open(filename, encoding='utf_8_sig') as file:
        config = yaml.load(file, Loader=yaml.SafeLoader)

    return config


def main():

    config = load_yaml(sys.argv[1])

    thread_list = [
        threading.Thread(target=bow_colletcor,
                         args=([
                             store, config['keywords'], config['product_page'],
                             config['review_page']
                         ])) for store in config['stores']
    ]

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()


if __name__ == '__main__':
    main()
