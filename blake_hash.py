import hashlib
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
import os

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

def chunk_reader(file_path, chunk_size):
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk

def blake_hash_chunk(chunk):
    hash_obj = hashlib.blake2b()
    hash_obj.update(chunk)
    return hash_obj.digest()

def blake_parallel(input_data, chunk_size=1024 * 1024):
    if isinstance(input_data, str):
        return blake_hash(input_data)

    file_size = os.path.getsize(input_data)
    chunks = max(1, file_size // chunk_size)
    cpu_count = multiprocessing.cpu_count()
    chunksize = max(1, chunks // cpu_count)

    with multiprocessing.Pool() as pool:
        results = pool.imap(blake_hash_chunk, chunk_reader(input_data, chunk_size), chunksize=chunksize)

        final_hash = hashlib.blake2b()
        for result in results:
            final_hash.update(result)

    return final_hash.hexdigest()

def blake_concurrent(input_data, min_chunk_size=1024 * 1024):
    if isinstance(input_data, str):
        return blake_hash(input_data)

    if len(input_data) < min_chunk_size * 2:
        return blake_hash(input_data)

    cores = multiprocessing.cpu_count()
    chunk_size = max(min_chunk_size, len(input_data) // cores)
    chunks = [input_data[i:i + chunk_size] for i in range(0, len(input_data), chunk_size)]

    with ThreadPoolExecutor(max_workers=cores) as executor:
        results = list(executor.map(blake_hash, chunks))

    combined_hash = hashlib.blake2b()
    for partial_hash in results:
        combined_hash.update(bytes.fromhex(partial_hash))

    return combined_hash.hexdigest()

def blake_file_parallel(file_path):
    return blake_parallel(file_path)

def blake_file_concurrent(file_path):
    with open(file_path, 'rb') as file:
        return blake_concurrent(file.read())