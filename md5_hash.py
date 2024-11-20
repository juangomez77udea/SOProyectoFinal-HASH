import hashlib
import multiprocessing

def md5_hash(input_data):
    if isinstance(input_data, str):
        data = input_data.encode('utf-8')
    elif isinstance(input_data, bytes):
        data = input_data
    else:
        raise ValueError("Input must be a string or bytes")

    hash_obj = hashlib.md5()
    hash_obj.update(data)
    return hash_obj.hexdigest()

def md5_parallel(input_data):
    cores = multiprocessing.cpu_count()
    if isinstance(input_data, str):
        input_data = input_data.encode('utf-8')
    chunk_size = max(1, len(input_data) // cores)
    chunks = [input_data[i:i+chunk_size] for i in range(0, len(input_data), chunk_size)]

    with multiprocessing.Pool(cores) as pool:
        results = pool.map(md5_hash, chunks)

    return ''.join(results)

def md5_concurrent(input_data):
    return md5_hash(input_data)

def md5_file_parallel(file_path):
    with open(file_path, 'rb') as file:
        return md5_parallel(file.read())

def md5_file_concurrent(file_path):
    with open(file_path, 'rb') as file:
        return md5_concurrent(file.read())