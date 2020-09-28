from bs4 import BeautifulSoup
from .yaml_loader import load_yaml
import pandas as pd
import requests
import sys
import time
import os


def load_scraper(url):

    headers = {"User-Agent": "Mozilla/5.0"}
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


def product_info(store):

    # load settings
    config = load_yaml(store)

    # load keyword page url
    df_url = pd.read_csv(config['url_list'], index_col='keywords')

    for keyword in df_url.index:
        save_path = config['save_path'] + keyword + '_' + config['product']
        print('product_info keyword: ', keyword)
        '''
        product_name = []
        product_url = []
        '''
        product_name = get_tag(df_url.loc[keyword], config['css'], get_tag_text)
        product_url = get_tag(df_url.loc[keyword], config['css'], get_tag_url, config['url_head'])
        '''
        for url in df_url.loc[keyword]:
            print('url: ', url)
            soup = load_scraper(url)
            product_name.append(
                [tag.text for tag in soup.select(config['css'])])
            product_url.append([
                (config['url_head'] + tag.get('href')).replace('dp', 'review')
                for tag in soup.select(config['css'])
            ])
            time.sleep(15)
        '''
        columns = []
        for i in range(len(product_name)):
            columns.append('url_' + str(i))

        df_product_name = pd.DataFrame(product_name)
        df_product_name = df_product_name.stack()

        df_product_url = pd.DataFrame(product_url)
        df_product_url = df_product_url.stack()

        review_list = get_tag(df_product_url, config['css_review'], get_tag_text)

        '''
        review_list = []
        for url in df_product_url:
            print('product url: ', url)
            soup = load_scraper(url)
            review_list.append(
                [tag.text for tag in soup.select(config['css_review'])])
            time.sleep(15)
        '''

        for review in review_list:
            print(review)

        df_product_review = pd.DataFrame(review_list)
        df_product_review = df_product_review.stack()

        if (os.path.exists(save_path)):
            df_product_review.to_csv(save_path,
                                     index=False,
                                     header=False,
                                     mode='a',
                                     encoding=config['encoding'],
                                     errors='ignore')
        else:
            df_product_review.to_csv(save_path,
                                     index=False,
                                     encoding=config['encoding'],
                                     errors='ignore')


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
