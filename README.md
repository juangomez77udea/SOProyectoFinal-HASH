# SOProyectoFinal-HASH
Proyecto final Sistemas Operativos

# Implementación
Para la implementación del proyecto usamos anaconda en la version 24.9.2. La codificación se utilzó python en la version 3.12.7.
Para el interprete de python se usó anaconda3, así:

![img.png](img.png)

![img_2.png](img_2.png)


# Librerias Usadas:

## [Multiprocessing](https://docs.python.org/es/3.9/library/multiprocessing.html):

Este es un paquete que nos permite crear procesos (spawning). El paquete ofrece concurrencia local y remota, haciendo que se esquive el [Global Interpreter Lock](https://docs.python.org/es/3.9/glossary.html#term-global-interpreter-lock), el cuál es el mecanismo encargado por el interprete CPython para asegurar que sólo un hilo ejecute el bytecode Python por vez. Este paquete permite al programador aprovechar el uso de multiples procesodores en una máquina, puede ser ejecutado en Unix y en Windows.
Para el presente trabajo usaremos el objeto Pool, el cuál nos ofrece un medio para paralelizar una función por medio de multiples valores de entrada por medio de paralelismo de datos.

## [Threading](https://docs.python.org/es/3.9/library/threading.html#module-threading):

Este módulo construye interfaces de hilado de alto nivel sobre el módulo de más bajo nivel _thread.
La objetos tipo hilo de la clase thread, representa una actividad que recorre en un hilo de control separado.

## [psutil 6.1.0](https://pypi.org/project/psutil/):
Es una bilbioteca que nos sirve para recuperar información sobre procesos en ejecución y utilización del  sistema.

## [OS:](https://docs.python.org/es/3.10/library/os.html)
Esta módulo nos provee una manera de usar fucionalidades dependientes del sistema operativo tales como leer o escribir un archivo, manipular rutas, leer lineas de los archivos, crear archivos temporales, entre otros.

## [Time](https://docs.python.org/es/3.13/library/time.html): 
Esta módulo proporciona funciones
