import logging
import re
from typing import Optional, List, Dict, Union

from requests import get, RequestException


def get_lending_tree_reviews(url: str) -> Optional[Dict[str, Union[str, List[Dict[str, str]]]]]:
    """ Gets all the lender reviews for the given lending tree url formats them into a response dict

    :param url:
    :return: None if an error occurs, otherwise returns the response dict
    """
    text = _make_request(url, 1)
    if text is None:
        return None

    pages = _get_num_pages(text)
    reviews = _process_resp(text)
    if reviews is None:
        return None

    response = {
        'url': url,
        'reviews': reviews
    }

    for page in range(2, pages + 1):
        text = _make_request(url, page)
        if text is None:
            return None

        reviews = _process_resp(text)
        if reviews is None:
            logging.error(f'failed to process following text for {url} on page {page}')
            return None

        response['reviews'] += reviews

    return response


def _make_request(url: str, page: 1) -> Optional[str]:
    """ Makes a http get and handles any errors

    :param url: url we are sending the request to
    :param page: the reviews page number
    :return:
    """
    try:
        resp = get(url, params={'pid': page})
    except RequestException as e:
        logging.error(f'an error occured while getting reviews, url: {url}, error{e}')
        return None
    if resp.status_code != 200:
        logging.error(f'recieved a bad response from {url}, status: {resp.status_code}, text: {resp.text}')
        return None

    return resp.text


def _get_num_pages(text: str) -> Optional[int]:
    """Pareses the html body to find the number of review pages.

    :param text: body of the html response
    :return: number of pages found or None if there was no match
    """
    match = re.search(r'.*<ul class="lenderNav pagination"[\s\S]*>(\d+)</a>.*', text)
    if match:
        max_page_num = match.group(1)
    else:
        return None
    return int(max_page_num)


def _process_resp(text: str) -> Optional[List[Dict[str, str]]]:
    """Takes the html response, splits it into reviews and builds the response dict

    :param text: body of the html response
    :return: None if there was a failure matching the text
    """
    collected_reviews = []

    reviews = text.split('class="recommended"')[1:]
    if len(reviews) < 1:
        return None
    for review_text in reviews:
        review = _get_review(review_text)
        if review is None:
            return None
        collected_reviews.append(review)

    return collected_reviews


def _get_review(review: str) -> Optional[Dict[str, str]]:
    """Searchs the input for all the review information and build a dict with the review info.

    :param review: the review html
    :return: returns either a review dict or None if there was no match
    """
    stars_match = re.search(r'numRec\">\((\d) of \d\)', review)
    title_match = re.search(r'reviewTitle\">((?:(?!</p>)[\s\S])+)</p>', review)
    review_match = re.search(r'reviewText\">((?:(?!</p>)[\s\S])+)</p>', review)
    author_match = re.search(r'consumerName\">((?:(?!</span>)[\s\S])+)<span>from ((?:(?!</span>)[\s\S])+)</span>', review)
    date_match = re.search(r'consumerReviewDate\">Reviewed in ([\s\w]+)</p>', review)
    # loan type can be an empty string
    loan_type_match = re.search(r'Loan Type:</p> *<div class=\"loanType\">((?:(?!</div>)[\s\S])*)</div>', review)

    if not all((stars_match, title_match, review_match, author_match, date_match, loan_type_match)):
        return None

    return {
        'stars': stars_match.group(1),
        'title': title_match.group(1),
        'review': review_match.group(1),
        'author': author_match.group(1),
        'location': author_match.group(2),
        'date': date_match.group(1),
        'loan_type': loan_type_match.group(1)
    }
