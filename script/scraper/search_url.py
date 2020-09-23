# -*- coding: utf-8 -*-

from selenium import webdriver
from .yaml_loader import load_yaml
import pandas as pd
import sys
import time


def load_search_page(url):

    driver = webdriver.Chrome('../driver/chromedriver')
    driver.get(url)

    return driver


def input_2_search_box(driver, store_name, keyword, config):

    # search by keyword
    search_box = driver.find_element_by_id(store_name['id'])
    search_box.send_keys(keyword)
    click_box = driver.find_element_by_class_name(store_name['button'])
    click_box.click()

    time.sleep(config['sleep'])

    # clear text in search box
    search_box = driver.find_element_by_id(store_name['id'])
    search_box.clear()

    url_list = [driver.current_url]
    for page in range(2, config['product_page'] + 1):
        url_list.append(
            driver.current_url.split('&')[0] + store_name['page'] + str(page))

    return url_list


def search_keywords(store, config):

    # load settings
    store_name = load_yaml(store)

    # load main url page
    driver = load_search_page(store_name['url'])

    # input argument to search box and get list of urls
    url_list = [
        input_2_search_box(driver, store_name, keyword, config)
        for keyword in config['keywords']
    ]

    # close driver session
    driver.close
    driver.quit

    columns = ['url_1']
    for i in range(2, len(url_list[0]) + 1):
        columns.append('url_' + str(i))

    df_url = pd.DataFrame(url_list, index=config['keywords'], columns=columns)
    df_url.index.name = 'keywords'

    df_url.to_csv(store_name['url_list'])


def main():

    # load settings
    config = load_yaml(sys.argv[1])

    search_keywords(config['stores'][0], config)


if __name__ == '__main__':
    main()
