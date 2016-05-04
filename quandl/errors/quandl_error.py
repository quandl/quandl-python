class QuandlError(RuntimeError):
    GENERIC_ERROR_MESSAGE = 'Something went wrong. Please try again. \
If you continue to have problems, please contact us at connect@quandl.com.'

    def __init__(self, quandl_message=None, http_status=None, http_body=None, http_headers=None,
                 quandl_error_code=None, response_data=None):
        self.http_status = http_status
        self.http_body = http_body
        self.http_headers = http_headers if http_headers is not None else {}

        self.quandl_error_code = quandl_error_code
        self.quandl_message = quandl_message if quandl_message is not None \
            else self.GENERIC_ERROR_MESSAGE
        self.response_data = response_data

    def __str__(self):
        if self.http_status is None:
            status_string = ''
        else:
            status_string = "(Status %(http_status)s) " % {"http_status": self.http_status}
        if self.quandl_error_code is None:
            quandl_error_string = ''
        else:
            quandl_error_string = "(Quandl Error %(quandl_error_code)s) " % {
                "quandl_error_code": self.quandl_error_code}
        return "%(ss)s%(qes)s%(qm)s" % {
            "ss": status_string, "qes": quandl_error_string, "qm": self.quandl_message
        }


class AuthenticationError(QuandlError):
    pass


class InvalidRequestError(QuandlError):
    pass


class LimitExceededError(QuandlError):
    pass


class NotFoundError(QuandlError):
    pass


class ServiceUnavailableError(QuandlError):
    pass


class InternalServerError(QuandlError):
    pass


class ForbiddenError(QuandlError):
    pass


class InvalidDataError(QuandlError):
    pass


class ColumnNotFound(QuandlError):
    pass
