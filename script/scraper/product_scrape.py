# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from .yaml_loader import load_yaml
import pandas as pd
import requests
import sys
import time


def load_scraper(url):

    headers = {"User-Agent": "Mozilla/5.0"}
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, features='lxml')

    return soup


def get_product_name():

    pass


def get_product_url():

    pass


def get_product_description():

    pass


def get_product_reviews():

    pass


def main():

    # load settings
    config = load_yaml(sys.argv[1])

    # load keyword page url
    url_list = pd.read_csv(config['url_list'])

    # load url to beautifulsoup
    soup_list = [load_scraper(url) for url in url_list['url']]

    soup = soup_list[0]

    product_name = [tag.text for tag in soup.select(config['css'])]
    product_url = [tag.get('href') for tag in soup.select(config['css'])]

    df_url = pd.DataFrame(list(zip(product_name, product_url)),
                          columns=['product_name', 'product_url'])
    df_url.to_csv(config['product'], index=False)

    print('end product_scrape.py main')


if __name__ == '__main__':
    main()
