import random
import string


def generate_random_string(n=10):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))
