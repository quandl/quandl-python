from test.helpers.my_httpretty import MyHTTPretty
import httpretty.core
import httpretty

# Substitute in our version
HTTPretty = MyHTTPretty

httpretty.core.httpretty = MyHTTPretty

# May need to set other module-level attributes here, e.g. enable, reset etc,
# depending on your needs
httpretty.httpretty = MyHTTPretty
httpretty.enable = MyHTTPretty.enable
httpretty.disable = MyHTTPretty.disable
