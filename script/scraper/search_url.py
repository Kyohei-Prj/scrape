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


def input_2_search_box(driver, id, button, keyword, sleep):

    # search by keyword
    search_box = driver.find_element_by_id(id)
    search_box.send_keys(keyword)
    click_box = driver.find_element_by_class_name(button)
    click_box.click()

    time.sleep(sleep)

    # clear text in search box
    search_box = driver.find_element_by_id(id)
    search_box.clear()

    return driver.current_url


def search_keywords(store, config):

    # load settings
    store_name = load_yaml(store)

    # load main url page
    driver = load_search_page(store_name['url'])

    # input argument to search box and get list of urls
    url_list = [
        input_2_search_box(driver, store_name['id'], store_name['button'],
                           keyword, config['sleep'])
        for keyword in config['keywords']
    ]

    # close driver session
    driver.close
    driver.quit

    df_url = pd.DataFrame(list(zip(config['keywords'], url_list)),
                          columns=['keyword', 'url'])
    df_url.to_csv(store_name['url_list'], index=False)


def main():

    # load settings
    config = load_yaml(sys.argv[1])

    search_keywords(config['stores'][0], config['product_page'])


if __name__ == '__main__':
    main()
