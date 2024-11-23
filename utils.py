import random
import string

def read_file_in_blocks(file_path, block_size=65536):
    with open(file_path, 'rb') as f:
        while True:
            block = f.read(block_size)
            if not block:
                break
            yield block

def parse_input(input_string):
    # Split the input string by commas and strip whitespace
    inputs = [item.strip() for item in input_string.split(',')]

    # If there's only one input, return it as a string
    if len(inputs) == 1:
        return inputs[0]

    # If there are multiple inputs, return them as a list
    return inputs

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))