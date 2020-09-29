from bs4 import BeautifulSoup
from .yaml_loader import load_yaml
import pandas as pd
import requests
import sys
import time
import os


def load_scraper(url):

    headers = {
        'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
    }
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, features='lxml')

    return soup


def get_tag(url_list, css, func, url_head=None):

    tag_list = []
    for url in url_list:
        print('url: ', url)
        soup = load_scraper(url)
        tag_list.append(func(tag, url_head) for tag in soup.select(css))
        time.sleep(15)

    return tag_list


def get_tag_text(tag, url_head):

    return tag.text


def get_tag_url(tag, url_head):

    return url_head + tag.get('href').replace('dp', 'review')


def list_to_stack(list):

    df = pd.DataFrame(list)
    df = df.stack()

    return df


def save_to_csv(df, path, encoding):

    if (os.path.exists(path)):
        df.to_csv(path,
                  index=False,
                  header=False,
                  mode='a',
                  encoding=encoding,
                  errors='ignore')
    else:
        df.to_csv(path, index=False, encoding=encoding, errors='ignore')


def product_info(store):

    # load settings
    config = load_yaml(store)

    # load keyword page url
    df_url = pd.read_csv(config['url_list'], index_col='keywords')

    for keyword in df_url.index:
        save_product_name = config['save_path'] + keyword + '_' + config[
            'product_name']
        print('product_info keyword: ', keyword)

        product_name = get_tag(df_url.loc[keyword], config['css_product'],
                               get_tag_text)
        product_url = get_tag(df_url.loc[keyword], config['css_product'],
                              get_tag_url, config['url_head'])

        df_product_name = list_to_stack(product_name)
        df_product_url = list_to_stack(product_url)

        save_to_csv(df_product_name, save_product_name, config['encoding'])

        '''
        save_product_review = config['save_path'] + keyword + '_' + config[
            'product_review']
        review_list = get_tag(df_product_url, config['css_review'],
                              get_tag_text)
        df_product_review = list_to_stack(review_list)
        save_to_csv(df_product_review, save_product_review, config['encoding'])
        '''


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
