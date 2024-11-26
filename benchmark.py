import time
import psutil
import threading
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import matplotlib.pyplot as plt

def measure_time(func, *args):
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    return end_time - start_time, result

def measure_memory():
    return psutil.Process().memory_info().rss / (1024 * 1024)  # Convertir a MB

def measure_cpu():
    return psutil.cpu_percent(interval=0.1)

def measure_wait_time():
    return sum(thread.native_id or 0 for thread in threading.enumerate()) / 1000000

def parallel_benchmark(hash_func, input_data, algorithm, input_type, input_size):
    with ProcessPoolExecutor() as executor:
        future_time = executor.submit(measure_time, hash_func, input_data)
        future_memory = executor.submit(measure_memory)
        future_cpu = executor.submit(measure_cpu)
        future_wait_time = executor.submit(measure_wait_time)

        time_taken, result = future_time.result()
        memory_usage = future_memory.result()
        cpu_usage = future_cpu.result()
        wait_time = future_wait_time.result()

    metrics = {
        "time": time_taken,
        "memory": memory_usage,
        "cpu": cpu_usage,
        "wait_time": wait_time,
        "result": result
    }

    # Guardar en la base de datos
    from database import Database
    db = Database()
    db.insert_result(algorithm, "parallel", metrics, input_type, input_size)
    db.close()

    return metrics

def concurrent_benchmark(hash_func, input_data, algorithm, input_type, input_size):
    with ThreadPoolExecutor() as executor:
        future_time = executor.submit(measure_time, hash_func, input_data)
        future_memory = executor.submit(measure_memory)
        future_cpu = executor.submit(measure_cpu)
        future_wait_time = executor.submit(measure_wait_time)

        time_taken, result = future_time.result()
        memory_usage = future_memory.result()
        cpu_usage = future_cpu.result()
        wait_time = future_wait_time.result()

    metrics = {
        "time": time_taken,
        "memory": memory_usage,
        "cpu": cpu_usage,
        "wait_time": wait_time,
        "result": result
    }

    # Guardar en la base de datos
    from database import Database
    db = Database()
    db.insert_result(algorithm, "concurrent", metrics, input_type, input_size)
    db.close()

    return metrics

def visualize_parallel_execution(hash_func, input_data):
    start_time = time.time()
    result = hash_func(input_data)
    end_time = time.time()

    execution_time = end_time - start_time
    num_cores = psutil.cpu_count(logical=False)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(range(num_cores), [execution_time] * num_cores)
    ax.set_xlabel('Núcleo de CPU')
    ax.set_ylabel('Tiempo de ejecución (segundos)')
    ax.set_title('Ejecución paralela a través de los núcleos de CPU')
    plt.savefig('parallel_execution.png')
    plt.close()

def visualize_comparison(parallel_metrics, concurrent_metrics):
    metrics = ['time', 'memory', 'cpu', 'wait_time']
    parallel_values = [parallel_metrics[m] for m in metrics]
    concurrent_values = [concurrent_metrics[m] for m in metrics]

    x = range(len(metrics))
    width = 0.35

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar([i - width/2 for i in x], parallel_values, width, label='Paralelo')
    ax.bar([i + width/2 for i in x], concurrent_values, width, label='Concurrente')

    ax.set_ylabel('Valores')
    ax.set_title('Comparación de ejecución paralela vs concurrente')
    ax.set_xticks(x)
    ax.set_xticklabels(metrics)
    ax.legend()

    plt.savefig('comparison.png')
    plt.close()