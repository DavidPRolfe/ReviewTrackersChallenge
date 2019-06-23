from os import path
from typing import Optional
from unittest import TestCase

from reviews import _get_num_pages, _process_resp, _get_review


class TestReviews(TestCase):
    def setUp(self):
        self.resp = self._load(path.join('test_data', 'test_resp.html'))
        self.resp2 = self._load(path.join('test_data', 'test_resp2.html'))
        self.resp3 = self._load(path.join('test_data', 'test_resp3.html'))
        self.resp4 = self._load(path.join('test_data', 'test_resp4.html'))
        self.resp5 = self._load(path.join('test_data', 'test_resp5.html'))
        self.resp6 = self._load(path.join('test_data', 'test_resp6.html'))
        self.api_resp = self._load(path.join('test_data', 'test_api_resp.html'))
        self.review_text = self._load(path.join('test_data', 'test_review.txt'))

    def test_get_num_pages(self):
        test_cases = [
            (self.resp, 168),
            (self.resp2, 168),
            (self.resp3, 168),
            (self.resp4, 168),
            (self.resp5, 168),
            (self.resp6, 168),
            (self.api_resp, 1),
            ('this is not a valid resp', None),
            ('<ul class="lenderNav pagination" >Not a num</a>', None),
        ]
        for test, expected in test_cases:
            self.assertEqual(_get_num_pages(test), expected)

    def test_get_review(self):
        test_cases = [
            (self.review_text, {
                'stars': '5',
                'title': 'Great Experience',
                'review': '48 hours from request to funds. Very responsive and communicated via email and phone which was great when I wasn\'t available to take a call.',
                'author': 'Jay ',
                'location': 'GALENA, OH ',
                'date': 'June 2019',
                'loan_type': 'Personal Loan'
            }),
            ('', None),
        ]
        for test, expected in test_cases:
            self.assertEqual(_get_review(test), expected)

    def test_process_response(self):
        test_cases = [
            (self.resp, 10),
            (self.resp2, 10),
            (self.resp3, 10),
            (self.resp4, 10),
            (self.resp5, 10),
            (self.resp6, 10),
            ('nonsense class="recommended", more nonsense', None),
            ('', None),
        ]
        for i, (test, expected) in enumerate(test_cases):
            out = _process_resp(test)
            if out is None:
                num_reviews = None
            else:
                num_reviews = len(out)
            self.assertEqual(num_reviews, expected)

    def _load(self, filename: str) -> Optional[str]:
        with open(filename) as file:
            text = ''.join(file.readlines())
        return text

