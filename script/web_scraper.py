from scraper.yaml_loader import load_yaml
from scraper.scrape_tools import PageStore

import threading
import sys


def collect_data(store):

    driver = store.load_search_page()
    url_dict = store.get_keyword_url(driver)

    driver.close
    driver.quit

    product_dict = store.get_product_info(
        url_dict, [store.get_tag_text, store.get_tag_url], ['name', 'url'],
        store.product_css)
    store.save_to_csv(product_dict, 'product_name')

    if store.review_css != 'no':
        review_dict = store.get_product_review(product_dict,
                                               [store.get_tag_text],
                                               ['review'], store.review_css)
        store.save_to_csv(review_dict, 'product_review')


def get_store_list(stores_yaml, Store_Object):

    store_list = []
    for store_yaml in stores_yaml:
        store_info = load_yaml(store_yaml)
        store = Store_Object(store_info['name'], store_info['main_url'],
                             store_info['keywords'], store_info['button_id'],
                             store_info['button_press'], store_info['sleep'],
                             store_info['product_css'],
                             store_info['flip_size'], store_info['url_head'],
                             store_info['review_css'],
                             store_info['flip_method'])
        store_list.append(store)

    return store_list


def make_thread_list(store_list):

    thread_list = [
        threading.Thread(target=collect_data, args=([store]))
        for store in store_list
    ]

    return thread_list


def start_scraping(stores_yaml, Store_Object):

    store_list = get_store_list(stores_yaml, Store_Object)
    thread_list = make_thread_list(store_list)

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()


def main():

    stores_yaml = load_yaml(sys.argv[1])
    start_scraping(stores_yaml['paging'], PageStore)


if __name__ == '__main__':
    main()
