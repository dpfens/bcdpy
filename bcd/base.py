import requests
from datetime import datetime
from collections import defaultdict
from . import exception


class Base(object):
    domain = 'https://api.better-call.dev'
    datetime_format = '%Y-%m-%dT%H:%M:%SZ'
    datetime_ms_format = '%Y-%m-%dT%H:%M:%S.%fZ'

    @classmethod
    def setdefaults(cls, parameters):
        parameters.setdefault('domain', cls.domain)
        parameters.setdefault('method', 'GET')
        return parameters

    @classmethod
    def validate_request_parameters(cls, parameters):
        valid_parameters = set(['domain', 'method', 'params', 'json', 'data'])
        included_parameters = set(parameters)
        invalid_parameters = included_parameters - valid_parameters
        if invalid_parameters:
            raise ValueError('The following parameters are invalid: %r' % (invalid_parameters, ))

    @classmethod
    def _request(cls, path, **kwargs):
        cls.validate_request_parameters(kwargs)
        kwargs = cls.setdefaults(kwargs)
        domain = kwargs.pop('domain')
        method = kwargs.pop('method')
        url = '%s/%s' % (domain, path)
        response = requests.request(method, url, **kwargs)
        return response

    @staticmethod
    def check_errors(data):
        if isinstance(data, dict):
            message = data.get('message')
            if message:
                raise exception.BCDException(message)

    @classmethod
    def to_datetime(cls, text):
        formats = [cls.to_datetime, cls.datetime_format]
        for format in formats:
            try:
                value = datetime.strptime(text, cls.datetime_format)
            except Exception:
                pass
            else:
                return value
        return None

    def from_api(data):
        output = defaultdict(lambda: None)
        output.update(data)
        return output
