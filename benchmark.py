import time
import psutil
import threading
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from sha256_hash import sha256_parallel, sha256_concurrent, sha256_file_parallel, sha256_file_concurrent
from md5_hash import md5_parallel, md5_concurrent, md5_file_parallel, md5_file_concurrent
from blake_hash import blake_parallel, blake_concurrent, blake_file_parallel, blake_file_concurrent


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


def run_benchmark(db, algorithm, input_type, input_data, input_size, num_executions):
    algorithms = {
        "sha256": {"parallel": sha256_parallel, "concurrent": sha256_concurrent, "file_parallel": sha256_file_parallel,
                   "file_concurrent": sha256_file_concurrent},
        "md5": {"parallel": md5_parallel, "concurrent": md5_concurrent, "file_parallel": md5_file_parallel,
                "file_concurrent": md5_file_concurrent},
        "blake": {"parallel": blake_parallel, "concurrent": blake_concurrent, "file_parallel": blake_file_parallel,
                  "file_concurrent": blake_file_concurrent}
    }

    selected_algorithm = algorithms.get(algorithm)
    if not selected_algorithm:
        print(f"Algoritmo {algorithm} no soportado.")
        return

    for execution_type in ["parallel", "concurrent"]:
        print(f"\nEvaluando {algorithm} en modo {execution_type}...")

        for _ in range(num_executions):
            if input_type == "file":
                func = selected_algorithm[f"file_{execution_type}"]
            else:
                func = selected_algorithm[execution_type]

            if execution_type == "parallel":
                with ProcessPoolExecutor() as executor:
                    future = executor.submit(measure_time, func, input_data)
                    time_taken, result = future.result()
            else:
                with ThreadPoolExecutor() as executor:
                    future = executor.submit(measure_time, func, input_data)
                    time_taken, result = future.result()

            memory_usage = measure_memory()
            cpu_usage = measure_cpu()
            wait_time = measure_wait_time()

            metrics = {
                "algorithm": algorithm,
                "execution_type": execution_type,
                "input_type": input_type,
                "input_size": input_size,
                "time": time_taken,
                "memory": memory_usage,
                "cpu": cpu_usage,
                "wait_time": wait_time,
                "result": result
            }

            db.insert_result(algorithm, execution_type, input_type, input_size, metrics)

            print(
                f"Tiempo: {time_taken:.4f}s, Memoria: {memory_usage:.2f}MB, CPU: {cpu_usage:.2f}%, Tiempo de espera: {wait_time:.4f}ms")