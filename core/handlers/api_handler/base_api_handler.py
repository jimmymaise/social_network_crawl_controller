from abc import ABCMeta, abstractmethod

import requests

from core.handlers.api_handler.api_specs.base_api_specs import BaseAPISpecs
from core.logger.logger_handler import Logger
from core.utils import retry
from core.utils.exceptions import ErrorRequestFormat, ErrorAPIServerConnection


class BaseApiRequestHandler(object, metaclass=ABCMeta):
    def __init__(self, base_url):
        self.base_url = base_url
        self.logger = Logger.get_logger()

    @abstractmethod
    def _handle_failed_request(self, response, request_data=None):
        pass

    @abstractmethod
    def _handle_success_request(self, response, request_data=None):
        pass

    @staticmethod
    def _is_request_success(response):
        # Can extend more this method
        return response.ok

    @staticmethod
    def _validate_schema(data, schema):
        error = {}
        try:
            schema().load(data)
        except Exception as e:
            error = e
        return data, error

    def _process_request(self, request_data: BaseAPISpecs):
        self.logger.info(f'{self.base_url}/{request_data.path}')
        self.logger.info(request_data.body)
        try:
            response = getattr(requests, request_data.method)(url=f'{self.base_url}/{request_data.path}',
                                                              headers=request_data.headers,
                                                              json=request_data.body)
        except Exception as e:
            raise ErrorAPIServerConnection(f'Error {str(e)}')
        return response

    def _validate_response_schema(self, response_body, response_schema):

        _, errors = self._validate_schema(response_body, response_schema)
        return response_body, errors

    def call_api(self, request_data: BaseAPISpecs, max_attempts: int = 1, retry_time_sleep: int = 3):
        _, request_schema_errors = self._validate_schema(request_data.body, request_data.request_schema)
        success = True
        if request_schema_errors:
            raise ErrorRequestFormat(f'Request Schema Error: {request_schema_errors}')
        retryer = retry.Retrying(stop=retry.stop_after_attempt(max_attempts),
                                 retry=(retry.retry_if_exception_type(Exception) | retry.retry_if_not_result(
                                     self._is_request_success)),
                                 wait=retry.wait_fixed(retry_time_sleep),
                                 before_sleep=retry.warning_when_retry,
                                 reraise=False,
                                 retry_error_callback=retry.return_last_value)
        response_schema_errors = {}
        response = retryer(self._process_request, request_data)
        if not self._is_request_success(response):
            success = False
            self._handle_failed_request(response, request_data)
            return response, success, response_schema_errors

        self._handle_success_request(response)
        response_body = response.json()
        data, response_schema_errors = self._validate_response_schema(response_body=response_body,
                                                                      response_schema=request_data.response_schema,
                                                                      )
        return response, success, response_schema_errors
