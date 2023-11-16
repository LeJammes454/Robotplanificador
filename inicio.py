
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import random
import math

class VentanaPrincipal:
    def __init__(self, master):
        self.master = master
        master.title("Planificación de Trayectorias")

        self.canvas = tk.Canvas(master, width=600, height=600)
        self.canvas.pack()

        self.label = tk.Label(master, text="¡Bienvenido al Planificador de Trayectorias!")
        self.label.pack()

        self.button_seleccionar_mapa = tk.Button(master, text="Seleccionar Mapa", command=self.seleccionar_mapa)
        self.button_seleccionar_mapa.pack()

        self.button_iniciar = tk.Button(master, text="Iniciar", command=self.iniciar_simulacion)
        self.button_iniciar.pack()

        self.button_linea_recta = tk.Button(master, text="Línea Recta", command=self.dibujar_linea_recta)
        self.button_linea_recta.pack()

        self.img_tk = None  # Variable para almacenar la representación de la imagen
        self.pixel_data = None  # Variable para almacenar la información de los píxeles
        self.robot_radio = 10  # Radio del robot (ajústalo según tus necesidades)
        self.robot_id = None  # ID del objeto del robot
        self.meta_id = None  # ID del objeto de la meta

    def seleccionar_mapa(self):
        file_path = filedialog.askopenfilename(title="Seleccionar Mapa", filetypes=[("Archivos de imagen", "*.jpg")])
        if file_path:
            print("Mapa seleccionado:", file_path)
            self.procesar_mapa(file_path)

    def procesar_mapa(self, file_path):
        # Eliminar objetos anteriores, si los hay
        self.canvas.delete("all")
        self.robot_id = None
        self.meta_id = None

        # Abrir la imagen
        img = Image.open(file_path)

        # Convertir la imagen a blanco y negro
        img = img.convert("L")

        # Redimensionar la imagen a 600x600
        img = img.resize((600, 600), resample=Image.BICUBIC)

        # Crear una representación de la imagen para mostrar en la interfaz gráfica
        self.img_tk = ImageTk.PhotoImage(img)

        # Mostrar la imagen en el Canvas
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img_tk)

        # Almacenar la información de los píxeles de la imagen
        self.pixel_data = list(img.getdata())

    def es_posicion_valida(self, x, y):
        # Comprobar si el píxel en la posición (x, y) es blanco (no obstáculo)
        pixel_index = y * 600 + x
        return self.pixel_data[pixel_index] > 128  # 128 es un umbral que puede ajustarse

    def obtener_posicion_valida(self):
        while True:
            x = random.randint(0, 599)
            y = random.randint(0, 599)
            if self.es_posicion_valida(x, y):
                return x, y

    def distancia_entre_puntos(self, punto1, punto2):
        x1, y1 = punto1
        x2, y2 = punto2
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def colisiona_con_obstaculo(self, x, y):
        # Comprobar si el círculo con radio self.robot_radio en la posición (x, y) colisiona con un obstáculo
        for i in range(-self.robot_radio, self.robot_radio + 1):
            for j in range(-self.robot_radio, self.robot_radio + 1):
                if 0 <= x + i < 600 and 0 <= y + j < 600:
                    if not self.es_posicion_valida(x + i, y + j):
                        return True
        return False

    def obtener_posicion_valida_con_radio(self):
        while True:
            x, y = self.obtener_posicion_valida()
            if not self.colisiona_con_obstaculo(x, y):
                return x, y

    def iniciar_simulacion(self):
        if self.img_tk:
            # Eliminar objetos anteriores, si los hay
            self.canvas.delete("robot")
            self.canvas.delete("meta")

            # Crear un robot azul (círculo) en una posición válida
            robot_x, robot_y = self.obtener_posicion_valida_con_radio()
            self.robot_id = self.canvas.create_oval(robot_x - self.robot_radio, robot_y - self.robot_radio,
                                                    robot_x + self.robot_radio, robot_y + self.robot_radio, fill="blue", tags="robot")

            # Crear un punto de meta verde (cubo) en una posición válida y alejada del robot
            max_intentos = 100  # Número máximo de intentos para encontrar una posición alejada
            for _ in range(max_intentos):
                meta_x, meta_y = self.obtener_posicion_valida_con_radio()
                distancia = self.distancia_entre_puntos((robot_x, robot_y), (meta_x, meta_y))
                if distancia > 2 * self.robot_radio:  # Ajusta este valor según tus necesidades
                    self.meta_id = self.canvas.create_rectangle(meta_x, meta_y, meta_x + 10, meta_y + 10, fill="green", tags="meta")
                    break

    def dibujar_linea_recta(self):
        if self.robot_id is not None and self.meta_id is not None:
            # Obtener las coordenadas del robot y la meta
            robot_coords = self.canvas.coords(self.robot_id)
            meta_coords = self.canvas.coords(self.meta_id)

            # Calcular el punto medio entre el robot y la meta
            punto_medio = ((robot_coords[0] + meta_coords[2]) / 2, (robot_coords[1] + meta_coords[3]) / 2)

            # Dibujar una línea recta dorada entre el robot y la meta
            self.canvas.create_line(robot_coords[0] + self.robot_radio, robot_coords[1] + self.robot_radio,
                                    meta_coords[0] + 5, meta_coords[1] + 5, fill="gold")

# Crear la ventana principal
root = tk.Tk()
app = VentanaPrincipal(root)

# Iniciar el bucle principal
root.mainloop()
