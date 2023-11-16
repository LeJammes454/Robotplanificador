import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class VentanaPrincipal:
    def __init__(self, master):
        self.master = master
        master.title("Planificación de Trayectorias")

        self.label = tk.Label(master, text="¡Bienvenido al Planificador de Trayectorias!")
        self.label.pack()

        self.button_seleccionar_mapa = tk.Button(master, text="Seleccionar Mapa", command=self.seleccionar_mapa)
        self.button_seleccionar_mapa.pack()

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
        img = img.resize((600, 600), Image.ANTIALIAS)

        # Crear una representación de la imagen para mostrar en la interfaz gráfica
        img_tk = ImageTk.PhotoImage(img)

        # Mostrar la imagen en la interfaz gráfica
        self.label.config(image=img_tk)
        self.label.image = img_tk

# Crear la ventana principal
root = tk.Tk()
app = VentanaPrincipal(root)

# Iniciar el bucle principal
root.mainloop()
