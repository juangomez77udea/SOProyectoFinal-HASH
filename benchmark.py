import multiprocessing
import os
import threading
import time

import matplotlib.pyplot as plt
import psutil

from database import Database

def measure_hash(algorithm_func, input_data):
    return algorithm_func(input_data)

def measure_time(algorithm_func, input_data):
    start_time = time.time()
    result = algorithm_func(input_data)
    return time.time() - start_time, result

def measure_memory():
    return psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)

def measure_cpu():
    return psutil.cpu_percent(interval=0.1)

def measure_disk():
    return psutil.disk_io_counters().read_bytes / (1024 * 1024)

def measure_wait_time():
    return sum(thread.native_id for thread in threading.enumerate()) / 1000000

class ResultThread(threading.Thread):
    def __init__(self, target, args=()):
        super().__init__(target=target, args=args)
        self.result = None

    def run(self):
        self.result = self._target(*self._args)
        print(f"Hilo: {self.name}, Identificador: {self.ident}, Función: {self._target.__name__}")

def benchmark(algorithm_func, input_data, algorithm_name, execution_type, input_type, input_size):
    result_thread = ResultThread(target=measure_hash, args=(algorithm_func, input_data))
    time_thread = ResultThread(target=measure_time, args=(algorithm_func, input_data))
    memory_thread = ResultThread(target=measure_memory)
    cpu_thread = ResultThread(target=measure_cpu)
    disk_thread = ResultThread(target=measure_disk)
    wait_thread = ResultThread(target=measure_wait_time)

    threads = [result_thread, time_thread, memory_thread, cpu_thread, disk_thread, wait_thread]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    execution_time, hash_result = time_thread.result

    metrics = {
        "result": hash_result,
        "time": execution_time,
        "memory": memory_thread.result,
        "cpu": cpu_thread.result,
        "disk": disk_thread.result,
        "wait_time": wait_thread.result
    }

    # Almacenar resultados en la base de datos
    db = Database()
    db.insert_result(algorithm_name, execution_type, metrics, input_type, input_size)
    db.close()

    return metrics

def visualize_parallel_execution(algorithm_func, input_data):
    num_cores = multiprocessing.cpu_count()

    def worker(core_id, result_queue):
        start_time = time.time()
        result = algorithm_func(input_data)
        end_time = time.time()
        result_queue.put((core_id, start_time, end_time))

    result_queue = multiprocessing.Queue()
    processes = []

    for i in range(num_cores):
        p = multiprocessing.Process(target=worker, args=(i, result_queue))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    results = []
    while not result_queue.empty():
        results.append(result_queue.get())

    # Visualización
    fig, ax = plt.subplots(figsize=(12, 6))

    for core_id, start_time, end_time in results:
        ax.barh(core_id, end_time - start_time, left=start_time, height=0.5, align='center')

    ax.set_yticks(range(num_cores))
    ax.set_yticklabels([f'Core {i}' for i in range(num_cores)])
    ax.set_xlabel('Tiempo (segundos)')
    ax.set_title('Ejecución Paralela por Núcleo')

    plt.tight_layout()
    plt.savefig('parallel_execution.png')
    plt.close()

    print(f"Gráfico de ejecución paralela guardado como 'parallel_execution.png'")

