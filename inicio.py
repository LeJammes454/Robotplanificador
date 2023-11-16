import tkinter as tk
from tkinter import filedialog

class VentanaPrincipal:
    def __init__(self, master):
        self.master = master
        master.title("Planificación de Trayectorias")

        self.label = tk.Label(master, text="¡Bienvenido al Planificador de Trayectorias!")
        self.label.pack()

        self.button_seleccionar_mapa = tk.Button(master, text="Seleccionar Mapa", command=self.seleccionar_mapa)
        self.button_seleccionar_mapa.pack()

    def seleccionar_mapa(self):
        file_path = filedialog.askopenfilename(title="Seleccionar Mapa", filetypes=[("Archivos de texto", "*.txt")])
        if file_path:
            print("Mapa seleccionado:", file_path)
            # Aquí puedes realizar la lógica para cargar y procesar el mapa.

# Crear la ventana principal
root = tk.Tk()
app = VentanaPrincipal(root)

# Iniciar el bucle principal
root.mainloop()
