import json

from abc import abstractmethod
from logging import LoggerAdapter
from urllib.parse import urlencode, urlunparse


class ApiBase:

    def __init__(self, api_key: str, logger: LoggerAdapter, currency: str):
        self._api_key = api_key
        self._currency = currency
        self._logger = logger

    @abstractmethod
    def api_request(self, **kwargs):
        raise NotImplementedError(f'{self.__class__.__name__}.api_request method is not defined')

    @property
    def api_key(self):
        return self._api_key

    @staticmethod
    def _build_airbnb_url(path, query=None):
        if query is not None:
            query = urlencode(query)

        return urlunparse(['https', 'www.airbnb.com', path, None, query, None])

    @staticmethod
    def _put_json_param_strings(query: dict):
        """Property format JSON strings for 'variables' & 'extensions' params."""
        query['variables'] = json.dumps(query['variables'], separators=(',', ':'))
        query['extensions'] = json.dumps(query['extensions'], separators=(',', ':'))

    def read_data(self, response):
        """Read response data as json"""
        self._logger.debug(f"Parsing {response.url}")
        data = json.loads(response.body)

        return data

    def _get_search_headers(self):
        """Get headers for search requests."""
        required_headers = {
            'Content-Type':              'application/json',
            'X-Airbnb-API-Key':          self._api_key,
            'X-Airbnb-GraphQL-Platform': 'web',
        }

        return required_headers | {
            # configurable parameters:
            'Device-Memory':                    '8',
            'DPR':                              '1.25',
            'ect':                              '4g',
            'Referer':                          'https://www.airbnb.com/',
            'User-Agent':                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
            'Viewport-Width':                   '630',
            'X-Airbnb-GraphQL-Platform-Client': 'minimalist-niobe',
            'X-CSRF-Token':                     'V4$.airbnb.com$AaWRqg_KKT0$FpJwy7PSjJnlgMetxHfJfebN5lqMIICA1t_nn3I0JxM=',
            'X-CSRF-Without-Token':             '1',
        }
