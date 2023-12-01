import csv
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import heapq
import subprocess


# Configuraciones iniciales
cuadricula_ancho = 40
cuadricula_alto = 30
tamaño_celda = 20
right_frame_ancho = cuadricula_ancho * tamaño_celda
right_frame_alto = cuadricula_alto * tamaño_celda

# Dimensiones del right_frame
right_frame_ancho = cuadricula_ancho * tamaño_celda
right_frame_alto = cuadricula_alto * tamaño_celda

# Matriz para almacenar los colores de las celdas
colores_celdas = [["white" for _ in range(cuadricula_ancho)] for _ in range(cuadricula_alto)]

# Función para dibujar la cuadrícula
def dibujar_cuadricula(canvas, ancho, alto, celda_size):
    # Dibujar líneas verticales
    for x in range(0, ancho, celda_size):
        canvas.create_line(x, 0, x, alto, fill="#000000")

    # Dibujar líneas horizontales
    for y in range(0, alto, celda_size):
        canvas.create_line(0, y, ancho, y, fill="#000000")

def seleccionar_y_mostrar_mapa():
    global colores_celdas
    ruta_archivo = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if ruta_archivo:
        with open(ruta_archivo, mode='r') as archivo_csv:
            lector_csv = csv.reader(archivo_csv, delimiter=',')
            for y, fila in enumerate(lector_csv):
                for x, valor in enumerate(fila):
                    color = "black" if valor == '1' else "white"
                    canvas.create_rectangle(x * tamaño_celda, y * tamaño_celda, (x + 1) * tamaño_celda, (y + 1) * tamaño_celda, fill=color, outline="")
                    colores_celdas[y][x] = color

        # Redibujar la cuadrícula después de colorear las celdas
        dibujar_cuadricula(canvas, right_frame_ancho, right_frame_alto, tamaño_celda)

    # Restablecer la posición del robot y la meta
    robot.place(x=robot._original_x, y=robot._original_y)
    meta.place(x=meta._original_x, y=meta._original_y)

def abrir_creador_mapa():
    subprocess.Popen(["python", "c:/Users/xboxj/OneDrive/Documentos/Planificador/Robotplanificador/creador_mapa.py"])

def on_canvas_click(event):
    columna = event.x // tamaño_celda
    fila = event.y // tamaño_celda
    color_celda = colores_celdas[fila][columna]
    print(f"Se hizo clic en la fila {fila}, columna {columna}, color: {color_celda}")

def iniciar_arrastre(event):
    widget = event.widget
    widget._drag_start_x = event.x
    widget._drag_start_y = event.y

def realizar_arrastre(event):
    widget = event.widget
    x = widget.winfo_x() - widget._drag_start_x + event.x
    y = widget.winfo_y() - widget._drag_start_y + event.y
    widget.place(x=x, y=y)

def reiniciarpos():
    global robot_en_cuadricula, meta_en_cuadricula

    # Borrar el camino y las posiciones del robot/meta en la cuadrícula
    for fila in range(cuadricula_alto):
        for columna in range(cuadricula_ancho):
            color_actual = colores_celdas[fila][columna]
            # Redibujar solo las celdas que no son parte del mapa original
            if color_actual != "black":
                canvas.create_rectangle(columna * tamaño_celda, fila * tamaño_celda, (columna + 1) * tamaño_celda, (fila + 1) * tamaño_celda, fill="white", outline="")
                colores_celdas[fila][columna] = "white"

    # Restablecer las posiciones del robot y la meta
    robot.place(x=robot._original_x, y=robot._original_y)
    meta.place(x=meta._original_x, y=meta._original_y)

    # Identificadores de posición en la cuadrícula
    robot_en_cuadricula = None
    meta_en_cuadricula = None

    # Redibujar la cuadrícula
    dibujar_cuadricula(canvas, right_frame_ancho, right_frame_alto, tamaño_celda)


def colocar_cuadro_en_cuadricula(fila, columna, color):
    return canvas.create_rectangle(columna * tamaño_celda, fila * tamaño_celda, (columna + 1) * tamaño_celda, (fila + 1) * tamaño_celda, fill=color, outline="")

def soltar_cuadro_en_cuadricula(event):
    global robot_en_cuadricula, meta_en_cuadricula
    widget = event.widget
    x = root.winfo_pointerx() - root.winfo_rootx()
    y = root.winfo_pointery() - root.winfo_rooty()

    # Determinar si el cuadro se soltó dentro de la cuadrícula
    if right_frame.winfo_x() <= x <= right_frame.winfo_x() + right_frame_ancho and right_frame.winfo_y() <= y <= right_frame.winfo_y() + right_frame_alto:
        columna = (x - right_frame.winfo_x()) // tamaño_celda
        fila = (y - right_frame.winfo_y()) // tamaño_celda

        # Verificar si la celda es negra
        if colores_celdas[fila][columna] == "black":
            # Devolver el cuadro a su posición original si la celda es negra
            widget.place(x=widget._original_x, y=widget._original_y)
        else:
            # Colocar el cuadro en la celda correspondiente si no es negra
            canvas.create_rectangle(columna * tamaño_celda, fila * tamaño_celda, (columna + 1) * tamaño_celda, (fila + 1) * tamaño_celda, fill=widget['bg'], outline="")
    else:
        # Devolver el cuadro a su posición original si se suelta fuera de la cuadrícula
        widget.place(x=widget._original_x, y=widget._original_y)

        # Actualizar la ubicación del robot/meta en la cuadrícula
    if widget == robot:
        robot_en_cuadricula = (fila, columna)
    elif widget == meta:
        meta_en_cuadricula = (fila, columna)


def arrastrar_cuadro_en_cuadricula(event, cuadro_id):
    columna = event.x // tamaño_celda
    fila = event.y // tamaño_celda
    canvas.coords(cuadro_id, columna * tamaño_celda, fila * tamaño_celda, (columna + 1) * tamaño_celda, (fila + 1) * tamaño_celda)

def calcular_heuristica(p1, p2):
    # Calcular la distancia de Manhattan entre p1 y p2
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def buscar_camino(inicio, fin):
    # Lista de nodos abiertos y cerrados
    abiertos = []
    cerrados = set()
    heapq.heappush(abiertos, (0, inicio))

    # Diccionario para rastrear el camino
    camino = {}
    costos_g = {inicio: 0}

    while abiertos:
        _, actual = heapq.heappop(abiertos)
        if actual == fin:
            # Reconstruir el camino
            recorrido = []
            while actual in camino:
                recorrido.append(actual)
                actual = camino[actual]
            return recorrido[::-1]  # Invertir el camino

        cerrados.add(actual)
        for vecino in obtener_vecinos(actual):
            if vecino in cerrados:
                continue

            nuevo_costo_g = costos_g[actual] + 1  # Suponemos un costo de 1 por movimiento
            if vecino not in costos_g or nuevo_costo_g < costos_g[vecino]:
                costos_g[vecino] = nuevo_costo_g
                f = nuevo_costo_g + calcular_heuristica(fin, vecino)
                heapq.heappush(abiertos, (f, vecino))
                camino[vecino] = actual

    return None

def obtener_vecinos(nodo):
    # Devuelve los vecinos navegables (no negros) de un nodo en la cuadrícula
    vecinos = []
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Direcciones: arriba, abajo, izquierda, derecha
        x, y = nodo[0] + dx, nodo[1] + dy
        if 0 <= x < cuadricula_ancho and 0 <= y < cuadricula_alto and colores_celdas[y][x] != "black":
            vecinos.append((x, y))
    return vecinos

def animar_camino(camino, indice=0):
    if indice < len(camino):
        columna, fila = camino[indice]
        # Colorear la celda del camino
        canvas.create_rectangle(columna * tamaño_celda, fila * tamaño_celda, (columna + 1) * tamaño_celda, (fila + 1) * tamaño_celda, fill="purple", outline="")
        # Llamar a esta misma función después de un breve retraso para la siguiente celda
        root.after(100, animar_camino, camino, indice + 1)

def iniciar_simulacion():
    if robot_en_cuadricula and meta_en_cuadricula:
        fila_robot, columna_robot = robot_en_cuadricula
        fila_meta, columna_meta = meta_en_cuadricula
        # Obtener el camino
        camino = buscar_camino((columna_robot, fila_robot), (columna_meta, fila_meta))
        if camino:
            animar_camino(camino)

# Crear la ventana principal
root = tk.Tk()
root.title("Robot Trazador de Ruta")
root.geometry(f"{250 + right_frame_ancho}x{max(400, right_frame_alto)}")

# Estilos para los botones y etiquetas
estilo_boton = {'bg': '#4CAF50', 'fg': 'white', 'padx': 10, 'pady': 5}
estilo_titulo = {'font': ('Helvetica', 16, 'bold')}

# Marco izquierdo (fondo azul)
left_frame = tk.Frame(root, width=250, height=790, bg="gray")
left_frame.pack_propagate(False)
left_frame.pack(side="left", fill="y")

# Marco superior
top_frame = tk.Frame(left_frame, bg="#D3D3D3")
top_frame.pack(side="top", fill="x")

# Título e integrantes
titulo_label = tk.Label(top_frame, text="Robot Trazador de Ruta", **estilo_titulo)
titulo_label.pack(pady=10)
integrantes_label = tk.Label(top_frame, text="Integrantes:\nJaime León Ángeles\nBryan Paramo Paramo\nArmando Jair Rivera Tinoco", bg="#D3D3D3")
integrantes_label.pack()

# Marco para los botones
buttons_frame = tk.Frame(left_frame, bg="#D3D3D3")
buttons_frame.pack(fill="x")

# Botones
create_map_button = tk.Button(buttons_frame, text="Crear mapa", command=abrir_creador_mapa, **estilo_boton)
create_map_button.pack(fill="x", pady=5)

select_map_button = tk.Button(buttons_frame, text="Seleccionar mapa", command=seleccionar_y_mostrar_mapa, **estilo_boton)
select_map_button.pack(fill="x", pady=5)

ini_button = tk.Button(buttons_frame, text="Reiniciar", command=reiniciarpos, **estilo_boton)
ini_button.pack(fill="x", pady=5)

start_button = tk.Button(buttons_frame, text="Iniciar", command=iniciar_simulacion, **estilo_boton)
start_button.pack(fill="x", pady=5)

# Crear cuadros para el robot y la meta
robot = tk.Label(root, bg="green", width=4, height=2)
robot._original_x = 10
robot._original_y = 350
robot.place(x=robot._original_x, y=robot._original_y)
robot.bind("<Button-1>", iniciar_arrastre)
robot.bind("<B1-Motion>", realizar_arrastre)
robot.bind("<ButtonRelease-1>", soltar_cuadro_en_cuadricula)

meta = tk.Label(root, bg="red", width=4, height=2)
meta._original_x = 60
meta._original_y = 350
meta.place(x=meta._original_x, y=meta._original_y)
meta.bind("<Button-1>", iniciar_arrastre)
meta.bind("<B1-Motion>", realizar_arrastre)
meta.bind("<ButtonRelease-1>", soltar_cuadro_en_cuadricula)

# Marco medio (ahora gris) para los robots y la meta
middle_frame = tk.Frame(left_frame, height=500, bg="#A9A9A9")
middle_frame.pack(side="top", fill="x")

# Marco inferior (fondo gris)
bottom_frame = tk.Frame(left_frame, bg="light grey")
bottom_frame.pack(side="top", fill="both", expand=True)

# Variables para almacenar las posiciones de robots y meta
robots_en_cuadricula = []  # Ahora es una lista
meta_en_cuadricula = None



# Marco derecho (fondo azul claro)
right_frame = tk.Frame(root, bg="lightblue", width=right_frame_ancho, height=right_frame_alto)
right_frame.pack(side="right", fill="none", expand=False)

# Crear un lienzo en el marco derecho
canvas = tk.Canvas(right_frame, bg="lightblue", width=right_frame_ancho, height=right_frame_alto)
canvas.pack()

# Vincular el evento de clic del ratón al lienzo
canvas.bind("<Button-1>", on_canvas_click)

# Dibujar la cuadrícula en el lienzo
dibujar_cuadricula(canvas, right_frame_ancho, right_frame_alto, tamaño_celda)

# Ejecutar la aplicación
root.mainloop()