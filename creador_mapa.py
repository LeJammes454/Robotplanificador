import pygame
import sys
import csv
import tkinter as tk
from tkinter import filedialog


# Inicializar Pygame
pygame.init()

# Tamaño de la ventana principal
ventana_ancho = 950
ventana_alto = 790

# Tamaño de la cuadrícula y de cada celda
cuadricula_ancho = 40
cuadricula_alto = 30
celda_ancho = ventana_ancho // cuadricula_ancho
celda_alto = ventana_alto // cuadricula_alto

# Tamaño de la ventana de selección de color
ventana_color_ancho = 100
ventana_color_alto = ventana_alto

# Inicializar la ventana principal
ventana = pygame.display.set_mode((ventana_ancho + ventana_color_ancho, ventana_alto))
pygame.display.set_caption("Dibuja el mapa")

# Inicializar la ventana de selección de color
ventana_color = pygame.Surface((ventana_color_ancho, ventana_color_alto))
ventana_color.fill((200, 200, 200))

# Colores
blanco = (255, 255, 255)
negro = (0, 0, 0)
gris_claro = (220, 220, 220)

# Crear la matriz de la cuadrícula
cuadricula = [[blanco for _ in range(cuadricula_ancho)] for _ in range(cuadricula_alto)]

# Función para dibujar la cuadrícula
def dibujar_cuadricula():
    for fila in range(cuadricula_alto):
        for columna in range(cuadricula_ancho):
            pygame.draw.rect(ventana, cuadricula[fila][columna], (columna * celda_ancho, fila * celda_alto, celda_ancho, celda_alto))
            pygame.draw.rect(ventana, gris_claro, (columna * celda_ancho, fila * celda_alto, celda_ancho, celda_alto), 1)

# Función para dibujar la ventana de selección de color
def dibujar_ventana_color():
    ventana_color.fill((200, 200, 200))
    pygame.draw.rect(ventana_color, blanco, (20, 20, 40, 40))
    pygame.draw.rect(ventana_color, negro, (20, 80, 40, 40))


# Función para guardar en formato CSV
def guardar_en_csv(cuadricula, ruta_archivo):
    with open(ruta_archivo, mode='w', newline='') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv, delimiter=',')
        for fila in cuadricula:
            fila_csv = [1 if celda == negro else 0 for celda in fila]
            escritor_csv.writerow(fila_csv)
    print("Diseño guardado en formato CSV")


def guardar_archivo_dialogo(cuadricula):
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal de Tkinter
    ruta_archivo = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if ruta_archivo:
        guardar_en_csv(cuadricula, ruta_archivo)
    root.destroy()


# Función para dibujar el botón de guardar
def dibujar_boton_guardar():
    fuente = pygame.font.Font(None, 24)
    texto = fuente.render("Guardar", True, (255, 255, 255))
    boton_guardar = pygame.Rect(ventana_ancho + 10, 150, 80, 30)
    pygame.draw.rect(ventana, (100, 100, 100), boton_guardar)
    ventana.blit(texto, (boton_guardar.x + 10, boton_guardar.y + 5))
    return boton_guardar

# Color de pintura seleccionado inicialmente
color_seleccionado = blanco

# Bucle principal
mouse_pulsado = False
while True:
    boton_guardar = dibujar_boton_guardar()
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            mouse_pulsado = True
            if boton_guardar.collidepoint(evento.pos):
                guardar_archivo_dialogo(cuadricula)
            elif ventana_ancho <= evento.pos[0] <= ventana_ancho + ventana_color_ancho:
                if 20 <= evento.pos[1] <= 60:
                    color_seleccionado = blanco
                elif 80 <= evento.pos[1] <= 120:
                    color_seleccionado = negro
            else:
                x, y = evento.pos
                fila = y // celda_alto
                columna = x // celda_ancho
                if 0 <= fila < cuadricula_alto and 0 <= columna < cuadricula_ancho:
                    cuadricula[fila][columna] = color_seleccionado
        elif evento.type == pygame.MOUSEBUTTONUP:
            mouse_pulsado = False
        elif evento.type == pygame.MOUSEMOTION:
            if mouse_pulsado:
                x, y = evento.pos
                fila = y // celda_alto
                columna = x // celda_ancho
                if 0 <= fila < cuadricula_alto and 0 <= columna < cuadricula_ancho:
                    cuadricula[fila][columna] = color_seleccionado

    # Dibujar la cuadrícula en la pantalla principal
    ventana.fill((200, 200, 200))
    dibujar_cuadricula()

    # Dibujar la ventana de selección de color
    dibujar_ventana_color()
    ventana.blit(ventana_color, (ventana_ancho, 0))

    # Dibujar el botón de guardar
    dibujar_boton_guardar()

    # Actualizar la pantalla
    pygame.display.update()
