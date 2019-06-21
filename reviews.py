import re
from typing import Optional
from requests import get
from logging import error


def get_lending_tree_reviews(url: str) -> Optional[dict]:
    resp = get(url)
    text = resp.text

    try:
        max_page_num = re.search('.*<ul class="lenderNav pagination"[\s\S]*>(\d+)<\/a>.*', text).group(1)
    except IndexError:
        error(f'unable to find max_page_num for {url}')
        return None


    # removing most of the useless html
    reviews_html = text.split('mainReviews')[1:]
    reviews_html[-1] = reviews_html[-1].split('Do you want to flag this review?')[0]
    # print(reviews_html[0])
    return None