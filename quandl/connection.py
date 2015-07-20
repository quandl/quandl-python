import re

import requests

from .util import Util
from .api_config import ApiConfig
from quandl.errors.quandl_error import (
    QuandlError, LimitExceededError, InternalServerError,
    AuthenticationError, ForbiddenError, InvalidRequestError,
    NotFoundError, ServiceUnavailableError)


class Connection:
    @classmethod
    def request(cls, http_verb, url, **options):
        if 'headers' in options:
            headers = options['headers']
        else:
            headers = {}

        accept_value = 'application/json'
        if ApiConfig.api_version:
            accept_value += ", application/vnd.quandl+json;version=%s" % ApiConfig.api_version

        headers = Util.merge_to_dicts({'accept': accept_value}, headers)
        if ApiConfig.api_key:
            headers = Util.merge_to_dicts({'x-api-token': ApiConfig.api_key}, headers)

        options['headers'] = headers

        abs_url = '%s/%s' % (ApiConfig.api_base, url)

        return cls.execute_request(http_verb, abs_url, **options)

    @classmethod
    def execute_request(cls, http_verb, url, **options):
        try:
            func = getattr(requests, http_verb)
            response = func(url, **options)
            if response.status_code < 200 or response.status_code >= 300:
                cls.handle_api_error(response)
            else:
                return response
        except requests.exceptions.RequestException as e:
            if e.response:
                cls.handle_api_error(e.response)
            raise e

    @classmethod
    def parse(cls, response):
        try:
            return response.json()
        except ValueError as e:
            raise QuandlError(str(e), response.status_code, response.text)

    @classmethod
    def handle_api_error(cls, resp):
        error_body = cls.parse(resp)
        code = error_body['quandl_error']['code']
        message = error_body['quandl_error']['message']
        prog = re.compile('^QE([a-zA-Z])x')
        if prog.match(code):
            code_letter = prog.match(code).group(1)

        if code_letter == 'L':
            klass = LimitExceededError
        elif code_letter == 'M':
            klass = InternalServerError
        elif code_letter == 'A':
            klass = AuthenticationError
        elif code_letter == 'P':
            klass = ForbiddenError
        elif code_letter == 'S':
            klass = InvalidRequestError
        elif code_letter == 'C':
            klass = NotFoundError
        elif code_letter == 'X':
            klass = ServiceUnavailableError
        else:
            klass = QuandlError

        raise klass(message, resp.status_code, resp.text, resp.headers, code)
