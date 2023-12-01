# README para la Aplicación de Trazador de Rutas para Robots

## Descripción General

La aplicación de Trazador de Rutas para Robots es una herramienta diseñada para simular y visualizar la planificación de rutas de robots autónomos en entornos definidos por el usuario. Compuesta por dos componentes principales, `inicio.py` y `creador_mapa.py`, permite a los usuarios crear mapas personalizados y simular el recorrido de un robot en estos entornos.

## Características

-   **Diseño de Mapas**: Crea mapas personalizados para simular diferentes entornos.
-   **Simulación de Rutas**: Visualiza cómo un robot navega a través del mapa evitando obstáculos.
-   **Interfaz Interactiva**: Manipula elementos como el robot y la meta en tiempo real.
-   **Guardado de Mapas**: Guarda y carga mapas en formato CSV para diferentes simulaciones.

## Requisitos Previos

Para utilizar la aplicación, necesitas:

-   Python 3.x
-   Librerías de Python: `tkinter`, `pygame`, y `PIL` (Python Imaging Library).

## Instalación y Configuración

1.  **Instalar Python 3.x**: Asegúrate de tener Python 3 instalado en tu sistema. Puedes descargarlo desde [python.org](https://www.python.org/downloads/).
2.  **Instalar Dependencias**: Instala las librerías requeridas utilizando pip. Abre una terminal y ejecuta:
    
    bashCopy code
    
    `pip install pygame pillow` 
    
3.  **Descargar los Archivos del Programa**: Descarga los archivos `inicio.py` y `creador_mapa.py` en tu directorio de trabajo.
>**Nota** Cambiar la direccion de ruta del archivo `creador_mapa.py`en el archivo `inicio.py` 

## Uso del Programa

### Crear un Mapa

1.  Ejecuta el script `creador_mapa.py`.
2.  Utiliza el mouse para dibujar obstáculos en la cuadrícula, representando el entorno.
3.  Guarda el mapa en formato CSV usando el botón "Guardar".

### Simular Rutas

1.  Ejecuta el script `inicio.py`.
2.  Carga un mapa previamente creado mediante el botón "Seleccionar mapa".
3.  Coloca el robot y la meta en el mapa arrastrándolos con el mouse.
4.  Inicia la simulación con el botón "Iniciar" y observa cómo el robot planea y sigue una ruta hacia la meta.

### Ejemplos de Uso

Se proporcionan varios mapas de ejemplo desde (`ejemplo1.csv` asta `ejemplo7.csv`). Estos archivos CSV representan diferentes disposiciones de obstáculos, donde `1` es un obstáculo y `0` un espacio libre.

#### Probar un Mapa de Ejemplo

-   Sigue los pasos en "Simular Rutas" para cargar y usar estos mapas.
-   Observa las diferencias en la planificación de rutas en diferentes configuraciones de obstáculos.

## Personalización y Expansión

-   **Personalización del Código**: Los scripts son completamente personalizables. Puedes modificar la lógica de planificación de rutas, el diseño de la interfaz, entre otros aspectos.
-   **Expansión de Funcionalidades**: Agrega nuevas características, como diferentes algoritmos de planificación de rutas o elementos interactivos adicionales.


## Licencia

Este proyecto está bajo la licencia MIT.

🐱‍💻

saludos especiales a NovaBryan(Bryan Paramo Paramo) y su mama Theriajta(Armando Jair Rivera Tinoco) que esta vez si trabajon xd
