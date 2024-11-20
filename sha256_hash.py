import hashlib
import multiprocessing

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

def sha256_parallel(input_data):
    cores = multiprocessing.cpu_count()
    chunk_size = max(1, len(input_data) // cores)
    chunks = [input_data[i:i+chunk_size] for i in range(0, len(input_data), chunk_size)]

    with multiprocessing.Pool(cores) as pool:
        results = pool.map(sha256_hash, chunks)

    return ''.join(results)

def sha256_concurrent(input_data):
    return sha256_hash(input_data)