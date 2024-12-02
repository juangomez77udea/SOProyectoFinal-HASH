import os
import matplotlib.pyplot as plt
import numpy as np

from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from sha256_hash import sha256_parallel, sha256_concurrent, sha256_file_parallel, sha256_file_concurrent
from md5_hash import md5_parallel, md5_concurrent, md5_file_parallel, md5_file_concurrent
from blake_hash import blake_parallel, blake_concurrent, blake_file_parallel, blake_file_concurrent
from benchmark import run_benchmark
from utils import generate_random_string
from script_generator_archive import generate_random_text_file
from database import Database

def main():
    version = input("Ingrese la versión de la base de datos (por ejemplo, v5): ")
    num_executions = int(input("Ingrese el número de ejecuciones para cada medición: "))

    db = Database(version)

    algorithms = ["sha256", "md5", "blake"]
    file_sizes = [1, 5, 10, 50, 100]
    string_lengths = [6, 12, 18, 24, 32]

    # Mediciones para archivos
    for size in file_sizes:
        file_name = f"test_file_{size}MB.bin"
        file_path = generate_random_text_file(file_name, size * 1024 * 1024)

        if file_path:
            for algorithm in algorithms:
                run_benchmark(db, algorithm, "file", file_path, f"{size}MB", num_executions)
            os.remove(file_path)
        else:
            print(f"No se pudo crear el archivo de prueba para {size}MB. Saltando esta medición.")

    # Mediciones para cadenas
    for length in string_lengths:
        input_data = generate_random_string(length)
        for algorithm in algorithms:
            run_benchmark(db, algorithm, "string", input_data, str(length), num_executions)

    # Guardar resultados en archivos JSON
    output_dir = f"dataset-{version}"
    db.save_to_json(output_dir)

    # Generar gráficos de velocidades
    generate_speed_graphs(db, algorithms, file_sizes, string_lengths, output_dir)

    db.close()

    print(f"\nTodos los resultados han sido guardados en la carpeta '{output_dir}'")
    print(f"Los gráficos de velocidades han sido guardados en la carpeta '{output_dir}'")

def generate_speed_graphs(db, algorithms, file_sizes, string_lengths, output_dir):
    # Gráficos para archivos
    generate_file_graphs(db, algorithms, file_sizes, output_dir)

    # Gráficos para cadenas
    generate_string_graphs(db, algorithms, string_lengths, output_dir)

def generate_file_graphs(db, algorithms, file_sizes, output_dir):
    plt.figure(figsize=(12, 8))
    all_speeds = []

    for algorithm in algorithms:
        parallel_speeds = []
        concurrent_speeds = []

        for size in file_sizes:
            collection_name = f"hash_benchmark-parallel_file_results-{size}MB"
            parallel_data = list(db.db[collection_name].find({"algorithm": algorithm}))
            parallel_speed = sum(d["time"] for d in parallel_data) / len(parallel_data)
            parallel_speeds.append(parallel_speed * 1e6)  # Convert to microseconds

            collection_name = f"hash_benchmark-concurrent_file_results-{size}MB"
            concurrent_data = list(db.db[collection_name].find({"algorithm": algorithm}))
            concurrent_speed = sum(d["time"] for d in concurrent_data) / len(concurrent_data)
            concurrent_speeds.append(concurrent_speed * 1e6)  # Convert to microseconds

        all_speeds.extend(parallel_speeds)
        all_speeds.extend(concurrent_speeds)

        plt.plot(file_sizes, parallel_speeds, label=f"{algorithm} (Paralelo)", marker='o')
        plt.plot(file_sizes, concurrent_speeds, label=f"{algorithm} (Concurrente)", marker='s')

    plt.xlabel("Tamaño del archivo (MB)")
    plt.ylabel("Tiempo de ejecución (microsegundos)")
    plt.title("Comparación de velocidades de algoritmos hash para archivos")
    plt.legend()
    plt.grid(True)

    # Configurar el eje x para mostrar los tamaños de archivo exactos
    plt.xticks(file_sizes)

    # Usar escala logarítmica para el eje Y
    plt.yscale('log')

    # Ajustar los límites del eje Y
    min_time = min(all_speeds)
    max_time = max(all_speeds)
    plt.ylim(bottom=min_time * 0.5, top=max_time * 2)

    # Función para formatear las etiquetas del eje Y en microsegundos
    def format_func(value, tick_number):
        return f"{value:.2f} µs"

    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(format_func))

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "file_speed_comparison.png"), dpi=300)
    plt.close()

def generate_string_graphs(db, algorithms, string_lengths, output_dir):
    fig, axs = plt.subplots(1, 3, figsize=(18, 6))

    for idx, algorithm in enumerate(algorithms):
        parallel_speeds = []
        concurrent_speeds = []

        for length in string_lengths:
            collection_name = f"hash_benchmark-parallel_string_results-{length}"
            parallel_data = list(db.db[collection_name].find({"algorithm": algorithm}))
            parallel_speed = sum(d["time"] for d in parallel_data) / len(parallel_data)
            parallel_speeds.append(parallel_speed * 1e6)  # Convert to microseconds

            collection_name = f"hash_benchmark-concurrent_string_results-{length}"
            concurrent_data = list(db.db[collection_name].find({"algorithm": algorithm}))
            concurrent_speed = sum(d["time"] for d in concurrent_data) / len(concurrent_data)
            concurrent_speeds.append(concurrent_speed * 1e6)  # Convert to microseconds

        x = np.arange(len(string_lengths))
        width = 0.35

        axs[idx].bar(x - width / 2, parallel_speeds, width, label='Paralelo')
        axs[idx].bar(x + width / 2, concurrent_speeds, width, label='Concurrente')

        axs[idx].set_xlabel("Longitud de la cadena")
        axs[idx].set_ylabel("Tiempo de ejecución (microsegundos)")
        axs[idx].set_title(f"{algorithm}")
        axs[idx].set_xticks(x)
        axs[idx].set_xticklabels(string_lengths)
        axs[idx].legend()

        # Formatear las etiquetas del eje y para mostrar más decimales
        axs[idx].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"{x:.2f} µs"))

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "string_speed_comparison.png"), dpi=300)
    plt.close()

if __name__ == "__main__":
    main()