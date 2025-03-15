import pygame
import random
import sys
import tkinter as tk
from tkinter import messagebox

pygame.init()

MAPA_ANCHO = 20
MAPA_ALTO = 9
ANCHO, ALTO = 1200, 800
TAMANO_CELDA = min(ANCHO // MAPA_ANCHO, ALTO // MAPA_ALTO)
MAPA_ORIGINAL = [
        [ 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [ 1,3,3,3,3,1,3,3,3,1,3,3,3,3,1,3,3,3,3,1],
        [ 1,3,1,1,3,1,3,1,3,1,3,1,1,3,1,3,1,1,3,1],
        [ 1,3,1,1,3,1,3,1,3,1,3,3,3,3,3,3,3,3,3,1],
        [ 1,3,3,3,3,3,3,3,3,3,3,1,1,1,1,1,3,1,1,1],
        [ 1,3,1,1,3,1,1,3,1,1,3,1,3,3,3,3,3,3,3,1],
        [ 1,3,1,1,3,1,1,3,1,1,3,1,3,1,1,1,1,1,3,1],
        [ 1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,3,3,3,1],
        [ 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]
def reset_mapa():
    return [fila[:] for fila in MAPA_ORIGINAL]

mapa = reset_mapa()

NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)

pac_x, pac_y = 1, 1
fan_x, fan_y = 10, 5
puntos = 0
velocidad = 100

pantalla = pygame.display.set_mode((MAPA_ANCHO * TAMANO_CELDA, MAPA_ALTO * TAMANO_CELDA))
pygame.display.set_caption("Pac-Man")

def reiniciar_juego():
    global pac_x, pac_y, fan_x, fan_y, puntos, mapa
    pac_x, pac_y = 1, 1
    fan_x, fan_y = 10, 5
    puntos = 0
    mapa = reset_mapa() 

def mover_pacman(dx, dy):
    global pac_x, pac_y, puntos
    nueva_x = pac_x + dx
    nueva_y = pac_y + dy
    
    if 0 <= nueva_x < MAPA_ANCHO and 0 <= nueva_y < MAPA_ALTO and mapa[nueva_y][nueva_x] != 1:
        if mapa[nueva_y][nueva_x] == 3:
            puntos += 10 
            mapa[nueva_y][nueva_x] = 0 
        pac_x, pac_y = nueva_x, nueva_y

def mover_fantasma():
    global fan_x, fan_y
    direcciones = [(0, -1), (0, 1), (-1, 0), (1, 0)]  
    random.shuffle(direcciones)  

    for dx, dy in direcciones:
        nueva_x = fan_x + dx
        nueva_y = fan_y + dy

        if 0 <= nueva_x < MAPA_ANCHO and 0 <= nueva_y < MAPA_ALTO and mapa[nueva_y][nueva_x] != 1:
            fan_x, fan_y = nueva_x, nueva_y
            break  

def mostrar_game_over():
    root = tk.Tk()
    root.withdraw()  
    respuesta = messagebox.askyesno("GAME OVER", f"Puntaje: {puntos}\n¿Quieres continuar?")
    if respuesta:
        reiniciar_juego()
    else:
        pygame.quit()
        sys.exit()

def dibujar_mapa():
    pantalla.fill(NEGRO)
    for y in range(MAPA_ALTO):
        for x in range(MAPA_ANCHO):
            if mapa[y][x] == 1:  
                pygame.draw.rect(pantalla, AZUL, (x * TAMANO_CELDA, y * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA))
            elif mapa[y][x] == 3:  
                pygame.draw.circle(pantalla, BLANCO, (x * TAMANO_CELDA + TAMANO_CELDA // 2, y * TAMANO_CELDA + TAMANO_CELDA // 2), TAMANO_CELDA // 6)

    pygame.draw.circle(pantalla, AMARILLO, (pac_x * TAMANO_CELDA + TAMANO_CELDA // 2, pac_y * TAMANO_CELDA + TAMANO_CELDA // 2), TAMANO_CELDA // 2)

    pygame.draw.rect(pantalla, ROJO, (fan_x * TAMANO_CELDA + 5, fan_y * TAMANO_CELDA + 5, TAMANO_CELDA - 10, TAMANO_CELDA - 10))

    fuente = pygame.font.Font(None, 36)
    texto = fuente.render(f"Puntos: {puntos}", True, BLANCO)
    pantalla.blit(texto, (10, 10))


clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]: mover_pacman(0, -1)
    if keys[pygame.K_DOWN]: mover_pacman(0, 1)
    if keys[pygame.K_LEFT]: mover_pacman(-1, 0)
    if keys[pygame.K_RIGHT]: mover_pacman(1, 0)

    mover_fantasma()

    if (pac_x, pac_y) == (fan_x, fan_y):
        mostrar_game_over()

    dibujar_mapa()
    pygame.display.flip()
    clock.tick(10)
