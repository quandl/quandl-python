import random
import string


def generate_random_string(n=10):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))


def generate_random_dictionary(n):
    random_dictionary = dict()
    for _ in range(n):
        random_dictionary[generate_random_string()] = generate_random_string()
    return random_dictionary
