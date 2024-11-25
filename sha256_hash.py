import hashlib
import multiprocessing
from functools import partial


def sha256_hash(input_data):
    if isinstance(input_data, str):
        data = input_data.encode('utf-8')
    elif isinstance(input_data, bytes):
        data = input_data
    else:
        raise ValueError("Input must be a string or bytes")

    hash_obj = hashlib.sha256()
    hash_obj.update(data)
    return hash_obj.hexdigest()


def sha256_parallel(input_data, min_chunk_size=1024 * 1024):  # 1MB minimum chunk size
    if len(input_data) < min_chunk_size * 2:  # If input is too small, use sequential
        return sha256_hash(input_data)

    cores = multiprocessing.cpu_count()
    chunk_size = max(min_chunk_size, len(input_data) // cores)
    chunks = [input_data[i:i + chunk_size] for i in range(0, len(input_data), chunk_size)]

    with multiprocessing.Pool() as pool:
        results = pool.map(sha256_hash, chunks)

    # Combine partial hashes
    combined_hash = hashlib.sha256()
    for partial_hash in results:
        combined_hash.update(bytes.fromhex(partial_hash))

    return combined_hash.hexdigest()


def sha256_concurrent(input_data):
    return sha256_hash(input_data)

