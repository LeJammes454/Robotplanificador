import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps
import numpy

def open_map():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        # Cargar la imagen
        image = Image.open(file_path)

        # Convertir a escala de grises y luego binarizar
        gray_image = ImageOps.grayscale(image)
        binary_image = gray_image.point(lambda x: 0 if x < 128 else 255, '1')

        # Redimensionar y mostrar la imagen
        resized_image = binary_image.resize((right_frame.winfo_width(), right_frame.winfo_height()), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(resized_image)
        map_label = tk.Label(right_frame, image=photo)
        map_label.image = photo
        map_label.pack(fill="both", expand=True)

        # Convertir a matriz para el algoritmo de planificación
        map_matrix = numpy.array(binary_image)


# Crear la ventana principal
root = tk.Tk()
root.title("Ventana Principal")
root.geometry("1200x790")

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
select_map_button = tk.Button(middle_frame, text="Seleccionar mapa", command=open_map)
select_map_button.pack(pady=10)

# Marco inferior (fondo azul)
bottom_frame = tk.Frame(left_frame, bg="blue")
bottom_frame.pack(side="top", fill="both", expand=True)

# Marco derecho (fondo azul claro)
right_frame = tk.Frame(root, bg="lightblue")
right_frame.pack(side="right", fill="both", expand=True)



# Ejecutar la aplicación
root.mainloop()
