import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import random

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

        self.img_tk = None  # Variable para almacenar la representación de la imagen

    def seleccionar_mapa(self):
        file_path = filedialog.askopenfilename(title="Seleccionar Mapa", filetypes=[("Archivos de imagen", "*.jpg")])
        if file_path:
            print("Mapa seleccionado:", file_path)
            self.procesar_mapa(file_path)

    def procesar_mapa(self, file_path):
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

    def iniciar_simulacion(self):
        if self.img_tk:
            # Crear un punto de meta verde (cubo) de manera aleatoria
            meta_x = random.randint(0, 599)
            meta_y = random.randint(0, 599)
            self.canvas.create_rectangle(meta_x, meta_y, meta_x + 10, meta_y + 10, fill="green")

            # Crear un robot azul (círculo) de manera aleatoria
            robot_x = random.randint(0, 599)
            robot_y = random.randint(0, 599)
            self.canvas.create_oval(robot_x, robot_y, robot_x + 20, robot_y + 20, fill="blue")

# Crear la ventana principal
root = tk.Tk()
app = VentanaPrincipal(root)

# Iniciar el bucle principal
root.mainloop()
