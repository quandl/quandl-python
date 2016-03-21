import logging

# Disable the debug logging used by the factory boy plugin by default.
logger = logging.getLogger('factory')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)