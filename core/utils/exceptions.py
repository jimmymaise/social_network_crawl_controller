class ErrorLinkFormat(Exception):
    def __init__(self, message='ErrorLinkFormat'):
        self.message = message
        self.collection_service_error_name = 'error_link_format'

    def __str__(self):
        return self.message


class ErrorResponseFailed(Exception):
    def __init__(self, message='ErrorResponseFailed'):
        self.message = message
        self.collection_service_error_name = 'error_response_failed'

    def __str__(self):
        return self.message


class ErrorResponseFormat(Exception):
    def __init__(self, message='ErrorResponseFormat'):
        self.message = message
        self.collection_service_error_name = 'error_response_format'

    def __str__(self):
        return self.message


