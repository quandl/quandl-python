class ApiConfig:
    api_key = None
    api_protocol = 'https://'
    api_base = '{}www.quandl.com/api/v3'.format(api_protocol)
    api_version = None
    page_limit = 100

    use_retries = True
    number_of_retries = 5
    retry_backoff_factor = 0.5
    max_wait_between_retries = 8
    retry_status_codes = [429] + list(range(500, 512))


def save_key(apikey, filename=None):
    if filename is None:
        import pathlib
        filename = str(pathlib.Path.home()) + "/.quandl_apikey"

    fileptr = open(filename, 'w')
    fileptr.write(apikey)
    fileptr.close()
    ApiConfig.api_key = apikey


def read_key(filename=None):
    if filename is None:
        import pathlib
        filename = str(pathlib.Path.home()) + "/.quandl_apikey"

    try:
        fileptr = open(filename, 'r')
        apikey = fileptr.read()
        fileptr.close()

        if apikey:
            ApiConfig.api_key = apikey
        else:
            raise Exception("File '{:s}' is empty.".format(filename))
    except ValueError:
        raise Exception("File '{:s}' not found.".format(filename))
