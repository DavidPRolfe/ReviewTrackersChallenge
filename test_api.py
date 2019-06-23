from os import path
from unittest import TestCase

from mock import patch

from app import app


def mocked_get(url, *args, **kwargs):
    filepath = path.join('test_data', 'test_api_resp.html')
    with open(filepath) as file:
        mock_resp = ''.join(file.readlines())

    if url == 'https://www.lendingtree.com/reviews':
        return mock_resp
    return None


class TestAPI(TestCase):
    def test_root_exists(self):
        with app.test_client() as client:
            resp = client.get('/')
            self.assertEqual(resp.status_code, 200)

    @patch('reviews._make_request', side_effect=mocked_get)
    def test_lender(self, _):
        test_cases = [
            (None, 400),
            ('bad_url', 404),
            ('https://www.lendingtree.com/reviews', 200)
        ]

        for url_param, expected_status in test_cases:
            with app.test_client() as client:
                if url_param is None:
                    resp = client.get('/lender')
                    self.assertEqual(resp.status_code, expected_status)
                else:
                    resp = client.get(f'/lender?url={url_param}')
                    self.assertEqual(resp.status_code, expected_status)



