import random
import string

def generate_key_value_pairs(num_pairs=1000):
    data = {}
    for i in range(num_pairs):
        key = f'k{i}'
        value = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
        data[key] = value
    return data