class DatalinkError(RuntimeError):
    GENERIC_ERROR_MESSAGE = 'Something went wrong. Please try again. \
If you continue to have problems, please contact us at connect@data.nasdaq.com.'

    def __init__(self, datalink_message=None, http_status=None, http_body=None, http_headers=None,
                 datalink_error_code=None, response_data=None):
        self.http_status = http_status
        self.http_body = http_body
        self.http_headers = http_headers if http_headers is not None else {}

        self.datalink_error_code = datalink_error_code
        self.datalink_message = datalink_message if datalink_message is not None \
            else self.GENERIC_ERROR_MESSAGE
        self.response_data = response_data

    def __str__(self):
        if self.http_status is None:
            status_string = ''
        else:
            status_string = "(Status %(http_status)s) " % {"http_status": self.http_status}
        if self.datalink_error_code is None:
            datalink_error_string = ''
        else:
            datalink_error_string = "(Nasdaq Data Link Error %(datalink_error_code)s) " % {
                "datalink_error_code": self.datalink_error_code}
        return "%(ss)s%(qes)s%(qm)s" % {
            "ss": status_string, "qes": datalink_error_string, "qm": self.datalink_message
        }


class AuthenticationError(DatalinkError):
    pass


class InvalidRequestError(DatalinkError):
    pass


class LimitExceededError(DatalinkError):
    pass


class NotFoundError(DatalinkError):
    pass


class ServiceUnavailableError(DatalinkError):
    pass


class InternalServerError(DatalinkError):
    pass


class ForbiddenError(DatalinkError):
    pass


class InvalidDataError(DatalinkError):
    pass


class ColumnNotFound(DatalinkError):
    pass
