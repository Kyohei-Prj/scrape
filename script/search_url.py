# -*- coding: utf-8 -*-

from selenium import webdriver
import pandas as pd
import sys
import yaml
import time


def load_yaml(filename):

    with open(filename, encoding='utf_8_sig') as file:
        config = yaml.load(file, Loader=yaml.SafeLoader)

    return config


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


def main():

    # load settings
    config = load_yaml(sys.argv[1])

    # load main url page
    driver = load_search_page(config['url'])

    # input argument to search box and get list of urls
    url_list = [
        input_2_search_box(driver, config['id'], config['button'], keyword,
                           config['sleep']) for keyword in config['keyword']
    ]

    # close driver session
    driver.close
    driver.quit

    df_url = pd.DataFrame(list(zip(config['keyword'], url_list)),
                          columns=['keyword', 'url'])
    df_url.to_csv(config['url_list'], index=False)


if __name__ == '__main__':
    main()
