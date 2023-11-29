import csv
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import subprocess

# Calcular las dimensiones de la cuadrícula
cuadricula_ancho = 40
cuadricula_alto = 30
tamaño_celda = 20  # Tamaño de cada celda de la cuadrícula en píxeles

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

    def borrar_de_cuadricula(fila, columna):
        # Redibujar la celda completa con el color de fondo
        canvas.create_rectangle(columna * tamaño_celda, fila * tamaño_celda, (columna + 1) * tamaño_celda, (fila + 1) * tamaño_celda, fill="white", outline="")

        # Redibujar las líneas de la cuadrícula para esta celda
        canvas.create_line(columna * tamaño_celda, fila * tamaño_celda, columna * tamaño_celda, (fila + 1) * tamaño_celda, fill="#000000")
        canvas.create_line(columna * tamaño_celda, fila * tamaño_celda, (columna + 1) * tamaño_celda, fila * tamaño_celda, fill="#000000")

    # Borrar el robot/meta de la cuadrícula si están presentes
    if robot_en_cuadricula:
        fila, columna = robot_en_cuadricula
        borrar_de_cuadricula(fila, columna)
        robot_en_cuadricula = None
    if meta_en_cuadricula:
        fila, columna = meta_en_cuadricula
        borrar_de_cuadricula(fila, columna)
        meta_en_cuadricula = None

    # Restablecer la posición del robot y la meta
    robot.place(x=robot._original_x, y=robot._original_y)
    meta.place(x=meta._original_x, y=meta._original_y)

# Identificadores para los cuadros en la cuadrícula
robot_en_cuadricula = None
meta_en_cuadricula = None

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

def mover_cuadro_en_cuadricula(event):
    # Identificar el cuadro sobre el que se ha hecho clic
    cuadro_id = canvas.find_closest(event.x, event.y)[0]
    if cuadro_id in [id_robot, id_meta]:
        # Guardar la posición original por si se necesita mover de vuelta
        cuadro_id._original_coords = canvas.coords(cuadro_id)
        canvas.bind("<B1-Motion>", lambda e: arrastrar_cuadro_en_cuadricula(e, cuadro_id))

def arrastrar_cuadro_en_cuadricula(event, cuadro_id):
    columna = event.x // tamaño_celda
    fila = event.y // tamaño_celda
    canvas.coords(cuadro_id, columna * tamaño_celda, fila * tamaño_celda, (columna + 1) * tamaño_celda, (fila + 1) * tamaño_celda)


# Crear la ventana principal
root = tk.Tk()
root.title("Ventana Principal")
root.geometry(f"{250 + right_frame_ancho}x{max(400, right_frame_alto)}")

# Marco izquierdo (fondo gris)
left_frame = tk.Frame(root, width=250, height=790, bg="gray")
left_frame.pack_propagate(False)
left_frame.pack(side="left", fill="y")

# Marco superior (fondo rojo)
top_frame = tk.Frame(left_frame, height=90, bg="red")
top_frame.pack(side="top", fill="x")

# Marco medio (fondo verde)
middle_frame = tk.Frame(left_frame, height=500, bg="green")
middle_frame.pack(side="top", fill="x")

# Botón para seleccionar el mapa
create_map_button = tk.Button(middle_frame, text="Crear mapa", command=abrir_creador_mapa)

create_map_button.pack(pady=10)
# Botón para seleccionar el mapa
select_map_button = tk.Button(middle_frame, text="Seleccionar mapa", command=seleccionar_y_mostrar_mapa)
select_map_button.pack(pady=10)

# Marco inferior (fondo azul)
bottom_frame = tk.Frame(left_frame, bg="blue")
bottom_frame.pack(side="top", fill="both", expand=True)

# Crear cuadros para el robot y la meta
robot = tk.Label(bottom_frame, bg="green", width=4, height=2)
robot.place(x=10, y=10)
robot._original_x = 10
robot._original_y = 10
robot.bind("<Button-1>", iniciar_arrastre)
robot.bind("<B1-Motion>", realizar_arrastre)
robot.bind("<ButtonRelease-1>", soltar_cuadro_en_cuadricula)

meta = tk.Label(bottom_frame, bg="orange", width=4, height=2)
meta.place(x=60, y=10)
meta._original_x = 60
meta._original_y = 10
meta.bind("<Button-1>", iniciar_arrastre)
meta.bind("<B1-Motion>", realizar_arrastre)
meta.bind("<ButtonRelease-1>", soltar_cuadro_en_cuadricula)

# Botón para seleccionar el mapa
ini_button = tk.Button(bottom_frame, text="Reiniciar", command=reiniciarpos)
ini_button.pack(pady=10)

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