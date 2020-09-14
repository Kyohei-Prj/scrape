# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from selenium import webdriver
import requests
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

    # load url to beautifulsoup
    soup_list = [load_scraper(url) for url in url_list]

    soup = soup_list[0]
    print(soup.find('.bcs-item'))


if __name__ == '__main__':
    main()
