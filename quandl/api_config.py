class ApiConfig:
    api_key = None
    api_base = 'https://www.quandl.com/api/v3'
    api_version = None
    page_limit = 100


def save_key(apikey, filename=None):
    """Store the Quandl Token in $HOME/.quandl_apikey 

    Parameters:
    -----------
    apikey : str
        The API Key from the Quandl Website. 

    filename : str
        Absolute path to the text where the 
        Quandl API Key is stored (Optional)
    
    """
    #set default path
    if filename is None:
        import pathlib 
        filename = str(pathlib.Path.home()) + "/.quandl_apikey";

    #write string to file
    fileptr = open(filename, 'w');
    fileptr.write(apikey);
    fileptr.close();

    #set key
    ApiConfig.api_key = apikey;


def read_key(filename=None):
    """ Returns the locally store QUandl API key from $HOME/.quandl_apikey 

    Parameters:
    -----------
    filename : str
        Absolute path to the text where the 
        Quandl API Key is stored (Optional)

    """
    #set default path
    if filename is None:
        import pathlib 
        filename = str(pathlib.Path.home()) + "/.quandl_apikey";

    #try to read
    try:
        fileptr = open(filename, 'r');
        apikey = fileptr.read();
        fileptr.close();

        if apikey:
            ApiConfig.api_key = apikey;
        else:
            raise Exception("File '{:s}' is empty. Please your 'quandl.save_key' before.".format(filename));
    except: 
        raise Exception("File '{:s}' not found. Please your 'quandl.save_key' before.".format(filename));