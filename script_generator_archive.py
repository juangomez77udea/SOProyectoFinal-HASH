import os
import random
import string

# Ruta del proyecto para guardar los archivos de prueba
project_path = "/home/juan/Documentos/Sistemas/Semestre_11/Sistemas_Operativos/Laboratorio/proyectoFinal/proyectoFinalSisOperat"
test_files_path = os.path.join(project_path, "archivos_prueba")

# Crear la carpeta 'archivos_prueba' si no existe
if not os.path.exists(test_files_path):
    os.makedirs(test_files_path)

def generate_random_text_file(file_name, size_in_bytes):
    file_path = os.path.join(test_files_path, file_name)
    with open(file_path, "w") as f:
        while f.tell() < size_in_bytes:
            random_text = ''.join(random.choices(string.ascii_letters + string.digits, k=100)) + '\n'
            f.write(random_text)

    print(f"Archivo '{file_name}' creado con éxito en {test_files_path} con un tamaño aproximado de {size_in_bytes / (1024 * 1024):.2f} MB.")
    print(f"Ruta completa del archivo generado: {file_path}")
    return file_path  # Devolver la ruta para utilizar el archivo posteriormente

def select_file_size(option):
    file_sizes = {
        "1": 1 * 1024 * 1024,
        "2": 5 * 1024 * 1024,
        "3": 10 * 1024 * 1024,
        "4": 50 * 1024 * 1024,
        "5": 100 * 1024 * 1024
    }

    if option in file_sizes:
        size_in_bytes = file_sizes[option]
        file_name = f"archivo_prueba_{size_in_bytes // (1024 * 1024)}MB.txt"
        return generate_random_text_file(file_name, size_in_bytes)
    else:
        print("Opción no válida. Intente de nuevo.")
        return None

# Esta función ya no es necesaria, pero la mantenemos por compatibilidad
def select_file_size_interactive():
    print("Seleccione el tamaño del archivo a generar:")
    print("1 - 1 MB")
    print("2 - 5 MB")
    print("3 - 10 MB")
    print("4 - 50 MB")
    print("5 - 100 MB")

    option = input("Opción: ")
    return select_file_size(option)

# Si se ejecuta este script directamente, usamos la versión interactiva
if __name__ == "__main__":
    select_file_size_interactive()