import hashlib
import multiprocessing
from functools import partial


def blake_hash(input_data):
    if isinstance(input_data, str):
        data = input_data.encode('utf-8')
    elif isinstance(input_data, bytes):
        data = input_data
    else:
        raise ValueError("Input must be a string or bytes")

    hash_obj = hashlib.blake2b()
    hash_obj.update(data)
    return hash_obj.hexdigest()


def blake_parallel(input_data, min_chunk_size=1024 * 1024):  # 1MB minimum chunk size
    if len(input_data) < min_chunk_size * 2:  # If input is too small, use sequential
        return blake_hash(input_data)

    cores = multiprocessing.cpu_count()
    chunk_size = max(min_chunk_size, len(input_data) // cores)
    chunks = [input_data[i:i + chunk_size] for i in range(0, len(input_data), chunk_size)]

    with multiprocessing.Pool() as pool:
        results = pool.map(blake_hash, chunks)

    # Combine partial hashes
    combined_hash = hashlib.blake2b()
    for partial_hash in results:
        combined_hash.update(bytes.fromhex(partial_hash))

    return combined_hash.hexdigest()


def blake_concurrent(input_data):
    return blake_hash(input_data)


def blake_file_parallel(file_path):
    with open(file_path, 'rb') as file:
        return blake_parallel(file.read())


def blake_file_concurrent(file_path):
    with open(file_path, 'rb') as file:
        return blake_concurrent(file.read())

