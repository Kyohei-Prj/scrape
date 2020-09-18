from . import search_url

def bow_colletcor(store, keywords, product_page, review_page):

    print(store)
    print(keywords)
    print(product_page)
    print(review_page)

    search_url.search_keywords(store, product_page)


def main():

    print('main')


if __name__ == '__main__':
    main()
