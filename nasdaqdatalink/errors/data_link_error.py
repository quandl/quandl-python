class DataLinkError(RuntimeError):
    GENERIC_ERROR_MESSAGE = 'Something went wrong. Please try again. \
If you continue to have problems, please contact us at connect@data.nasdaq.com.'

    def __init__(self, data_link_message=None, http_status=None, http_body=None, http_headers=None,
                 data_link_error_code=None, response_data=None):
        self.http_status = http_status
        self.http_body = http_body
        self.http_headers = http_headers if http_headers is not None else {}

        self.data_link_error_code = data_link_error_code
        self.data_link_message = data_link_message if data_link_message is not None \
            else self.GENERIC_ERROR_MESSAGE
        self.response_data = response_data

    def __str__(self):
        if self.http_status is None:
            status_string = ''
        else:
            status_string = "(Status %(http_status)s) " % {"http_status": self.http_status}
        if self.data_link_error_code is None:
            data_link_error_string = ''
        else:
            data_link_error_string = "(Nasdaq Data Link Error %(data_link_error_code)s) " % {
                "data_link_error_code": self.data_link_error_code}
        return "%(ss)s%(qes)s%(qm)s" % {
            "ss": status_string, "qes": data_link_error_string, "qm": self.data_link_message
        }


class AuthenticationError(DataLinkError):
    pass


class InvalidRequestError(DataLinkError):
    pass


class LimitExceededError(DataLinkError):
    pass


class NotFoundError(DataLinkError):
    pass


class ServiceUnavailableError(DataLinkError):
    pass


class InternalServerError(DataLinkError):
    pass


class ForbiddenError(DataLinkError):
    pass


class InvalidDataError(DataLinkError):
    pass


class ColumnNotFound(DataLinkError):
    pass
