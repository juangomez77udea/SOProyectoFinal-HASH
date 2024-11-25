from sha256_hash import sha256_parallel, sha256_concurrent
from md5_hash import md5_parallel, md5_concurrent
from blake_hash import blake_parallel, blake_concurrent
from benchmark import benchmark, visualize_parallel_execution
from utils import parse_input, generate_random_string
from script_generator_archive import select_file_size
from database import Database
import os

def run_benchmark(algorithm, input_type, input_data, num_executions):
    algorithms = {
        "sha256": {"parallel": sha256_parallel, "concurrent": sha256_concurrent},
        "md5": {"parallel": md5_parallel, "concurrent": md5_concurrent},
        "blake": {"parallel": blake_parallel, "concurrent": blake_concurrent}
    }

    selected_algorithm = algorithms.get(algorithm)
    if not selected_algorithm:
        print(f"Algoritmo {algorithm} no soportado.")
        return

    if input_type == "text":
        input_data = parse_input(input_data)
        input_size = len(input_data)
    else:
        input_size = os.path.getsize(input_data)

    for i in range(num_executions):
        print(f"\nEjecución {i + 1} de {num_executions}")

        print(f"\nEvaluando {algorithm} en modo paralelo...")
        parallel_metrics = benchmark(selected_algorithm["parallel"], input_data, algorithm, "parallel", input_type,
                                     input_size)
        print("Resultado (Paralelo):", parallel_metrics["result"])
        print(f"Tiempo (Paralelo): {parallel_metrics['time']} segundos")
        print(f"Uso de memoria (Paralelo): {parallel_metrics['memory']} MB")
        print(f"Uso de CPU (Paralelo): {parallel_metrics['cpu']}%")
        print(f"Uso de disco (Paralelo): {parallel_metrics['disk']} MB/s")
        print(f"Tiempo de espera entre procesos (Paralelo): {parallel_metrics['wait_time']} ms")

        print(f"\nVisualizando ejecución paralela...")
        visualize_parallel_execution(selected_algorithm["parallel"], input_data)

        print(f"\nEvaluando {algorithm} en modo concurrente...")
        concurrent_metrics = benchmark(selected_algorithm["concurrent"], input_data, algorithm, "concurrent",
                                       input_type, input_size)
        print("Resultado (Concurrente):", concurrent_metrics["result"])
        print(f"Tiempo (Concurrente): {concurrent_metrics['time']} segundos")
        print(f"Uso de memoria (Concurrente): {concurrent_metrics['memory']} MB")
        print(f"Uso de CPU (Concurrente): {concurrent_metrics['cpu']}%")
        print(f"Uso de disco (Concurrente): {concurrent_metrics['disk']} MB/s")
        print(f"Tiempo de espera entre procesos (Concurrente): {concurrent_metrics['wait_time']} ms")

def display_all_results():
    db = Database()
    results = db.get_all_results()
    db.close()

    print("\nResultados de ejecuciones paralelas:")
    for result in results["parallel"]:
        print(f"Algoritmo: {result['algorithm']}")
        print(f"Tiempo: {result['time']} segundos")
        print(f"Uso de Memoria: {result['memory']} MB")
        print(f"Uso de CPU: {result['cpu']}%")
        print(f"Uso de Disco: {result['disk']} MB/s")
        print(f"Tiempo de Espera: {result['wait_time']} ms")
        print(f"Resultado del hash: {result['result']}")
        print(f"Tipo de entrada: {result['input_type']}")
        print(
            f"Tamaño de entrada: {result['input_size']} {'bytes' if result['input_type'] == 'file' else 'caracteres'}")
        print("-" * 40)

    print("\nResultados de ejecuciones concurrentes:")
    for result in results["concurrent"]:
        print(f"Algoritmo: {result['algorithm']}")
        print(f"Tiempo: {result['time']} segundos")
        print(f"Uso de Memoria: {result['memory']} MB")
        print(f"Uso de CPU: {result['cpu']}%")
        print(f"Uso de Disco: {result['disk']} MB/s")
        print(f"Tiempo de Espera: {result['wait_time']} ms")
        print(f"Resultado del hash: {result['result']}")
        print(f"Tipo de entrada: {result['input_type']}")
        print(
            f"Tamaño de entrada: {result['input_size']} {'bytes' if result['input_type'] == 'file' else 'caracteres'}")
        print("-" * 40)

def main():
    while True:
        print("\nSelecciona una opción:")
        print("1 - Ejecutar benchmark")
        print("2 - Mostrar todos los resultados")
        print("3 - Salir")
        choice = int(input("Opción: "))

        if choice == 1:
            print("\nSelecciona el Algoritmo de Hash:")
            print("1 - SHA256\n2 - MD5\n3 - BLAKE")
            alg_choice = int(input("Opción: "))

            algorithms = {1: "sha256", 2: "md5", 3: "blake"}
            algorithm = algorithms.get(alg_choice)

            print("\nSelecciona el Tipo de Entrada:")
            print("1 - Archivo\n2 - Texto o Número")
            input_type = "file" if int(input("Opción: ")) == 1 else "text"

            if input_type == "file":
                print("\nSelecciona el Tamaño del Archivo a Generar:")
                print("1 - 1 MB\n2- 5 MB\n3 - 10 MB\n4 - 50 MB\n5 - 100 MB")
                file_option = input("Opción: ")
                input_data = select_file_size(file_option)
            else:
                print("\nSelecciona el Tamaño de la Cadena a Generar:")
                print("1 - 6 caracteres\n2 - 12 caracteres\n3 - 18 caracteres\n4 - 24 caracteres\n5 - 32 caracteres")
                string_option = int(input("Opción: "))
                string_sizes = {1: 6, 2: 12, 3: 18, 4: 24, 5: 32}
                input_data = generate_random_string(string_sizes.get(string_option, 6))
                print(f"Cadena generada: {input_data}")

            num_executions = int(input("Introduce el número de veces que deseas ejecutar el benchmark: "))
            run_benchmark(algorithm, input_type, input_data, num_executions)
        elif choice == 2:
            display_all_results()
        elif choice == 3:
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()

