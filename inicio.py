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

# Función para dibujar la cuadrícula
def dibujar_cuadricula(canvas, ancho, alto, celda_size):
    # Dibujar líneas verticales
    for x in range(0, ancho, celda_size):
        canvas.create_line(x, 0, x, alto, fill="#000000")

    # Dibujar líneas horizontales
    for y in range(0, alto, celda_size):
        canvas.create_line(0, y, ancho, y, fill="#000000")

def seleccionar_y_mostrar_mapa():
    ruta_archivo = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if ruta_archivo:
        with open(ruta_archivo, mode='r') as archivo_csv:
            lector_csv = csv.reader(archivo_csv, delimiter=',')
            for y, fila in enumerate(lector_csv):
                for x, valor in enumerate(fila):
                    color = "black" if valor == '1' else "white"
                    canvas.create_rectangle(x * tamaño_celda, y * tamaño_celda, (x + 1) * tamaño_celda, (y + 1) * tamaño_celda, fill=color, outline="")

        # Redibujar la cuadrícula después de colorear las celdas
        dibujar_cuadricula(canvas, right_frame_ancho, right_frame_alto, tamaño_celda)


def abrir_creador_mapa():
        subprocess.Popen(["python", "c:/Users/xboxj/OneDrive/Documentos/Planificador/Robotplanificador/creador_mapa.py"])



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

# Botón para seleccionar el mapa
edit_map_button = tk.Button(middle_frame, text="Editar mapa", command=0)
edit_map_button.pack(pady=10)

# Marco inferior (fondo azul)
bottom_frame = tk.Frame(left_frame, bg="blue")
bottom_frame.pack(side="top", fill="both", expand=True)

# Marco derecho (fondo azul claro)
right_frame = tk.Frame(root, bg="white", width=right_frame_ancho, height=right_frame_alto)
right_frame.pack(side="right", fill="none", expand=False)

# Crear un lienzo en el marco derecho
canvas = tk.Canvas(right_frame, bg="lightblue", width=right_frame_ancho, height=right_frame_alto)
canvas.pack()

# Dibujar la cuadrícula en el lienzo
dibujar_cuadricula(canvas, right_frame_ancho, right_frame_alto, tamaño_celda)

# Ejecutar la aplicación
root.mainloop()