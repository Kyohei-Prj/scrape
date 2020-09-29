from scraper.yaml_loader import load_yaml
from scraper.search_url import search_keywords
from scraper.product_scrape import product_info

import threading
import sys


def bow_colletcor(store, config):

    search_keywords(store, config)
    product_info(store)


def main():

    config = load_yaml(sys.argv[1])

    thread_list = [
        threading.Thread(target=bow_colletcor, args=([store, config]))
        for store in config['stores']
    ]

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()


if __name__ == '__main__':
    main()
