# SOProyectoFinal-HASH
Proyecto final Sistemas Operativos

# Implementación
Para la implementación del proyecto usamos anaconda en la version 24.9.2. La codificación se utilzó python en la version 3.12.7.
Para el interprete de python se usó anaconda3, así:

![image](https://github.com/user-attachments/assets/ec927791-4a6d-4dd5-91a3-bdf96edaa8d0)

![image](https://github.com/user-attachments/assets/1dea2ec9-e9df-489f-8f1d-2ae018479add)

En caso de no tener ningun interprete previamente instalado, el IDE nos lo hara saber y nos brindara la opcion para configurar una:

![imagen ide](https://github.com/user-attachments/assets/1ef34a30-6d8b-41a0-8eb2-fd6fdcd371c1)

Para poder ejecutar el código debemos tener una base de datos de mongodb en nuestro entorno local, es importante que el nombre de la base de datos y el puerto que se expone coincidan con los datos que se encuentran en el archivo 'database.py'

![imagen db](https://github.com/user-attachments/assets/e42b07ae-6da2-4e3e-be22-898eb5bf312f)

![imagen dbc](https://github.com/user-attachments/assets/360fe10c-1d37-4953-9b30-de117cd67b8c)

# Ejecucion

Al ejecutar el codigo se mostrara el siguiente menu:

![menu](https://github.com/user-attachments/assets/07264520-f539-4bf9-b726-fb6b7e09c31a)

La opcion 1 nos permitira escoger un algoritmo:

![menu algoritmo](https://github.com/user-attachments/assets/791e2912-e9c9-461c-8a83-d8888cc67ada)

Luego se selecciona el metodo de input:

![metodo input](https://github.com/user-attachments/assets/d0ca8f37-5ee7-49dd-a8a8-1d094c131b90)

Seleccion de longitud de cadena aleatoria que sera generada:

![longitud cadena](https://github.com/user-attachments/assets/ebba9a4d-322f-45c5-95c1-bedbaff7a86e)

Se genera una cadena, luego se define cuanta veces se desea que se repita el algoritmo:

![repeticiones](https://github.com/user-attachments/assets/b6540d99-0cf2-4a18-b634-1a16ab7a7962)

Resultados:

![resultados](https://github.com/user-attachments/assets/58d66670-b9a3-4f00-8997-d56e1946665c)


# Librerias Usadas:

## [Multiprocessing](https://docs.python.org/es/3.9/library/multiprocessing.html):

Este es un paquete que nos permite crear procesos (spawning). El paquete ofrece concurrencia local y remota, haciendo que se esquive el [Global Interpreter Lock](https://docs.python.org/es/3.9/glossary.html#term-global-interpreter-lock), el cuál es el mecanismo encargado por el interprete CPython para asegurar que sólo un hilo ejecute el bytecode Python por vez. Este paquete permite al programador aprovechar el uso de multiples procesodores en una máquina, puede ser ejecutado en Unix y en Windows.
Para el presente trabajo usaremos el objeto Pool, el cuál nos ofrece un medio para paralelizar una función por medio de multiples valores de entrada por medio de paralelismo de datos.

## [Threading](https://docs.python.org/es/3.9/library/threading.html#module-threading):
Este módulo construye interfaces de hilado de alto nivel sobre el módulo de más bajo nivel _thread. La objetos tipo hilo de la clase thread, representa una actividad que recorre en un hilo de control separado. Es usada en nuestro proyecto en la medición del tiempo de espera.

Este módulo construye interfaces de hilado de alto nivel sobre el módulo de más bajo nivel _thread.
La objetos tipo hilo de la clase thread, representa una actividad que recorre en un hilo de control separado.

## [Psutil 6.1.0](https://pypi.org/project/psutil/):
Es una biblioteca que ayuda a recuperar información sobre los procesos en ejecución del sistema, por ejemplo (CPU, memoria, discos, entre otros..). En nuestro desarrollo lo usamos en el benchmark (punto de referencia) para las mediciones seleccionadas.

## [OS:](https://docs.python.org/es/3.10/library/os.html)
Esta módulo nos provee una manera de usar fucionalidades dependientes del sistema operativo tales como leer o escribir un archivo, manipular rutas, leer lineas de los archivos, crear archivos temporales, entre otros.

## [Time](https://docs.python.org/es/3.13/library/time.html): 
Este módulo proporciona funciones relacionadas con el tiempo. La mayoría de las funciones definidas de este módulo, invocan funciones C con el mismo nombre. En nuestro desarrollo las usamos para el control de las medidas seleccionadas, uso de memoria, cpu, tiempo de espera, ejecución del hash.

## [Concurrent.futures:](https://docs.python.org/es/3/library/concurrent.futures.html)
Este módulo provee una interfaz para ejecutar invocables de forma asíncrona por intermedio de hilos usando ThreadPoolExecutor o ProcessPoolExecutor. Esta librería la usamos en los diferentes algoritmos hash(sha256m, md5 y blake) para garantizar la ejecución de concurrente por medio de hilos.

## [matplotlib:](https://matplotlib.org/) 
Es una biblioteca que se usa para las visualizaciones de los resultados.

## [hashlib:](https://docs.python.org/es/3.10/library/hashlib.html) 
Este módulo implementa una interfaz común para diferentes algoritmos hash, con esta accedemos a los algoritmos que necesitamos sin necesidad de crear los códigos desde cero para cada uno de ellos.

## [pymongo:](https://pymongo.readthedocs.io/en/stable/)
PyMongo es una distribución de Python que contiene herramientas para trabajar con MongoDB y es la forma recomendada de trabajar con MongoDB desde Python.

## [random:](https://docs.python.org/es/3/library/random.html) 
Este módulo implementa generadores de números pseudoaleatorios para varias distribuciones.
