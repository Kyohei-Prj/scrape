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


def product_info(store):

    # load settings
    config = load_yaml(store)

    # load keyword page url
    df_url = pd.read_csv(config['url_list'], index_col='keywords')

    for keyword in df_url.index:
        print('product_info keyword: ', keyword)
        product_name = []
        product_url = []
        for url in df_url.loc[keyword]:
            print(url)
            soup = load_scraper(url)
            product_name.append(
                [tag.text for tag in soup.select(config['css'])])
            product_url.append(
                [tag.get('href') for tag in soup.select(config['css'])])
            df_product_info = pd.DataFrame(
                list(zip(product_name, product_url)),
                columns=['product_name', 'product_url'])
            df_product_info.to_csv(config['save_path'] + keyword + '_' +
                                   config['product'],
                                   index=False,
                                   mode='a')
            time.sleep(20)


def backup():

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


def main():

    # load settings
    config = load_yaml(sys.argv[1])

    # load keyword page url
    df_url = pd.read_csv(config['url_list'])

    for keyword in df_url.index:
        print(keyword)


if __name__ == '__main__':
    main()
