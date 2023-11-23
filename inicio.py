import heapq
import time
import tkinter as tk
from tkinter import Canvas, filedialog, messagebox
from PIL import Image, ImageTk, ImageOps
import numpy

def open_map():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        image = Image.open(file_path)
        gray_image = ImageOps.grayscale(image)
        binary_image = gray_image.point(lambda x: 0 if x < 128 else 255, '1')

        canvas.update()
        resized_image = binary_image.resize((canvas.winfo_width(), canvas.winfo_height()), Image.Resampling.LANCZOS)
        global photo, binary_image_ref
        photo = ImageTk.PhotoImage(resized_image)
        canvas.create_image(0, 0, image=photo, anchor="nw")
        binary_image_ref = numpy.array(binary_image)

def a_star_search(start, goal, binary_image_ref):
    def heuristic(a, b):
        return abs(b[0] - a[0]) + abs(b[1] - a[1])

    neighbors = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j
            tentative_g_score = g_score[current] + 1

            if 0 <= neighbor[0] < binary_image_ref.shape[0] and 0 <= neighbor[1] < binary_image_ref.shape[1]:
                if binary_image_ref[neighbor[0], neighbor[1]] == 255:
                    if tentative_g_score < g_score.get(neighbor, float("inf")):
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return []

def calcular_y_dibujar_ruta():
    start_coords = canvas.coords(colocar_elementos.robot)[:2]
    goal_coords = canvas.coords(colocar_elementos.meta)[:2]

    # Convertir las coordenadas a índices de la matriz
    start = (int(start_coords[1] / 25), int(start_coords[0] / 25))
    goal = (int(goal_coords[1] / 25), int(goal_coords[0] / 25))

    print("Coordenadas del robot en el canvas:", start_coords, "-> En la matriz:", start)
    print("Coordenadas de la meta en el canvas:", goal_coords, "-> En la matriz:", goal)

    robot_en_obstaculo = verificar_obstaculo(colocar_elementos.robot)
    meta_en_obstaculo = verificar_obstaculo(colocar_elementos.meta)

    print("Robot en posición válida:", not robot_en_obstaculo)
    print("Meta en posición válida:", not meta_en_obstaculo)
    
    # Verificar si el robot o la meta están sobre un obstáculo
    if verificar_obstaculo(colocar_elementos.robot) or verificar_obstaculo(colocar_elementos.meta):
        messagebox.showinfo("Error", "El robot o la meta están sobre un obstáculo")
        return

    path = a_star_search(start, goal, binary_image_ref)

    # Dibujar la ruta en el canvas
    if path:
        for point in path:
            x, y = point[1] * 25, point[0] * 25
            canvas.create_rectangle(x, y, x + 25, y + 25, outline="yellow", fill="yellow")
        print("Ruta válida encontrada y dibujada en el mapa.")
    else:
        messagebox.showinfo("Sin Ruta", "No se encontró una ruta válida")

def verificar_obstaculo(item):
    x1, y1, x2, y2 = canvas.coords(item)
    cx, cy = int((x1 + x2) / 2), int((y1 + y2) / 2)

    return 0 <= cx < binary_image_ref.shape[1] and 0 <= cy < binary_image_ref.shape[0] and binary_image_ref[cy, cx] == 0

def colocar_elementos():
    coord_robot = [100, 100, 150, 150]
    coord_meta = [200, 200, 250, 250]

    if not hasattr(colocar_elementos, "robot"):
        colocar_elementos.robot = canvas.create_oval(*coord_robot, fill="blue", tags="robot")
        colocar_elementos.meta = canvas.create_rectangle(*coord_meta, fill="green", tags="meta")
    else:
        canvas.coords(colocar_elementos.robot, *coord_robot)
        canvas.coords(colocar_elementos.meta, *coord_meta)

    def iniciar_movimiento(event):
        item = canvas.find_closest(event.x, event.y)[0]
        if item in [colocar_elementos.robot, colocar_elementos.meta]:
            canvas.tag_raise(item)
            canvas.bind("<Motion>", mover_elemento, add='+')

    def mover_elemento(event):
        item = canvas.find_withtag("current")[0]
        x, y = event.x, event.y
        item_width = 25

        if item_width < x < (canvas.winfo_width() - item_width) and item_width < y < (canvas.winfo_height() - item_width):
            canvas.coords(item, x - item_width, y - item_width, x + item_width, y + item_width)

    canvas.bind("<ButtonPress-1>", iniciar_movimiento)
    canvas.bind("<ButtonRelease-1>", lambda event: canvas.unbind("<Motion>"))

root = tk.Tk()
root.title("Ventana Principal")
root.geometry("1200x790")

left_frame = tk.Frame(root, width=250, height=790, bg="gray")
left_frame.pack_propagate(False)
left_frame.pack(side="left", fill="y")

top_frame = tk.Frame(left_frame, height=90, bg="red")
top_frame.pack(side="top", fill="x")

middle_frame = tk.Frame(left_frame, height=500, bg="green")
middle_frame.pack(side="top", fill="x")

select_map_button = tk.Button(middle_frame, text="Seleccionar mapa", command=open_map)
select_map_button.pack(pady=10)

boton_colocar = tk.Button(middle_frame, text="Colocar", command=colocar_elementos)
boton_colocar.pack()

boton_calcular_ruta = tk.Button(middle_frame, text="Calcular Ruta", command=calcular_y_dibujar_ruta)
boton_calcular_ruta.pack()

bottom_frame = tk.Frame(left_frame, bg="blue")
bottom_frame.pack(side="top", fill="both", expand=True)

right_frame = tk.Frame(root, bg="lightblue")
right_frame.pack(side="right", fill="both", expand=True)

canvas = Canvas(right_frame, bg="lightblue")
canvas.pack(fill="both", expand=True)

root.mainloop()
