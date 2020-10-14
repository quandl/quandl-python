import os


class ApiConfig:
    api_key = None
    api_protocol = 'https://'
    api_base = '{}www.quandl.com/api/v3'.format(api_protocol)
    api_version = None  # This is not used but keeping for backwards compatibility
    page_limit = 100

    use_retries = True
    number_of_retries = 5
    retry_backoff_factor = 0.5
    max_wait_between_retries = 8
    retry_status_codes = [429] + list(range(500, 512))
    verify_ssl = True


def save_key(apikey, filename=None):
    if filename is None:
        filename = os.path.join(os.path.expanduser('~'), '.quandl_apikey')

    fileptr = open(filename, 'w')
    fileptr.write(apikey)
    fileptr.close()
    ApiConfig.api_key = apikey


def read_key(filename=None):
    if filename is None:
        filename = os.path.join(os.path.expanduser('~'), '.quandl_apikey')

    with open(filename, 'r') as f:
        apikey = f.read()

    if not apikey:
        raise ValueError("File '{:s}' is empty.".format(filename))

    ApiConfig.api_key = apikey
