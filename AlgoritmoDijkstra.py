
import pygame
import math
import heapq
import time

# Configuración de pantalla y colores
ANCHO, ALTO = 800, 600
RADIO_NODO = 20
DISTANCIA_MINIMA = 30
COLOR_FONDO = (0, 0, 0)          # Negro
COLOR_NODO = (0, 0, 255)         # Azul
COLOR_INICIAL = (0, 255, 0)      # Verde
COLOR_FINAL = (255, 0, 0)        # Rojo
COLOR_LINEA = (255, 255, 255)    # Blanco
COLOR_CAMINO = (255, 255, 0)     # Amarillo
COLOR_TEXTO = (255, 255, 255)

pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Visualización del Algoritmo de Dijkstra")
fuente = pygame.font.SysFont(None, 24)

# Estructuras de datos
nodos = []
conexiones = {}
letras_nodos = {}
nodo_inicio = None
nodo_fin = None
camino = []
nodo_seleccionado = None

# Funciones auxiliares


def distancia(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def agregar_nodo(pos):
    for nodo in nodos:
        if distancia(nodo, pos) < DISTANCIA_MINIMA:
            mostrar_alerta("Nodo muy cerca de otro nodo existente.")
            return
    # Generamos un ID para el nodo (puedes usar letras si prefieres)
    nodo_id = len(nodos) + 1
    nodos.append(pos)
    letras_nodos[pos] = str(nodo_id)  # Asignamos un número o letra al nodo
    conexiones[pos] = []


def agregar_conexion(n1, n2):
    costo = distancia(n1, n2)
    conexiones[n1].append((n2, costo))
    conexiones[n2].append((n1, costo))

# Algoritmo de Dijkstra con animación


def dijkstra_animado(inicio, fin):
    distancias = {nodo: float('inf') for nodo in nodos}
    distancias[inicio] = 0
    cola_prioridad = [(0, inicio)]
    nodos_previos = {nodo: None for nodo in nodos}

    while cola_prioridad:
        distancia_actual, nodo_actual = heapq.heappop(cola_prioridad)

        if distancia_actual > distancias[nodo_actual]:
            continue

        if nodo_actual == fin:
            break

        # Efecto animado: mostrar el nodo actual mientras se explora
        pygame.draw.circle(pantalla, COLOR_CAMINO, nodo_actual, RADIO_NODO)
        pygame.display.update()
        time.sleep(0.05)

        for vecino, peso in conexiones[nodo_actual]:
            distancia = distancia_actual + peso

            if distancia < distancias[vecino]:
                distancias[vecino] = distancia
                nodos_previos[vecino] = nodo_actual
                heapq.heappush(cola_prioridad, (distancia, vecino))

    # Si no se encontró un camino, mostrar mensaje y retornar
    if distancias[fin] == float('inf'):
        mostrar_alerta("No se encontró un camino entre inicio y fin.")
        return []

    # Reconstrucción del camino
    camino = []
    while fin:
        camino.append(fin)
        fin = nodos_previos[fin]
    camino.reverse()
    return camino

# Función de dibujo


def dibujar():
    pantalla.fill(COLOR_FONDO)
    # Dibujar conexiones
    for n1 in conexiones:
        for n2, _ in conexiones[n1]:
            pygame.draw.line(pantalla, COLOR_LINEA, n1, n2, 2)

    # Dibujar nodos
    for nodo in nodos:
        color = COLOR_NODO
        if nodo == nodo_inicio:
            color = COLOR_INICIAL
        elif nodo == nodo_fin:
            color = COLOR_FINAL
        pygame.draw.circle(pantalla, color, nodo, RADIO_NODO)

        # Dibujar la letra o número dentro del nodo
        letra = letras_nodos[nodo]
        texto = fuente.render(letra, True, COLOR_TEXTO)
        pantalla.blit(
            texto, (nodo[0] - texto.get_width() // 2, nodo[1] - texto.get_height() // 2))

    # Dibujar el camino resaltado en amarillo
    if camino:
        for i in range(len(camino) - 1):
            pygame.draw.line(pantalla, COLOR_CAMINO,
                             camino[i], camino[i + 1], 3)

    pygame.display.flip()

# Función para mostrar alertas en pantalla


def mostrar_alerta(texto):
    pantalla.fill(COLOR_FONDO)  # Limpia la pantalla para mostrar la alerta
    alerta_texto = fuente.render(texto, True, COLOR_TEXTO)
    pantalla.blit(alerta_texto, (10, ALTO - 30))
    pygame.display.update()
    time.sleep(2)  # Pausa para que el usuario vea la alerta

# Función para limpiar el estado


def limpiar():
    global nodos, conexiones, letras_nodos, nodo_inicio, nodo_fin, camino
    nodos = []
    conexiones = {}
    letras_nodos = {}
    nodo_inicio = (RADIO_NODO + 10, RADIO_NODO + 10)
    nodo_fin = (ANCHO - RADIO_NODO - 10, ALTO - RADIO_NODO - 10)
    nodos.extend([nodo_inicio, nodo_fin])
    letras_nodos[nodo_inicio] = 'I'  # Letra 'I' para el nodo de inicio
    letras_nodos[nodo_fin] = 'F'  # Letra 'F' para el nodo final
    conexiones[nodo_inicio] = []
    conexiones[nodo_fin] = []
    camino = []


# Modo principal
ejecutando = True
nodo_inicio = (RADIO_NODO + 10, RADIO_NODO + 10)
nodo_fin = (ANCHO - RADIO_NODO - 10, ALTO - RADIO_NODO - 10)
nodos.extend([nodo_inicio, nodo_fin])
letras_nodos[nodo_inicio] = 'I'  # Letra 'I' para el nodo de inicio
letras_nodos[nodo_fin] = 'F'  # Letra 'F' para el nodo final
conexiones[nodo_inicio] = []
conexiones[nodo_fin] = []
camino = []
nodo_seleccionado = None

while ejecutando:
    dibujar()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            pos = evento.pos
            if evento.button == 1:  # Click izquierdo para agregar nodos
                agregar_nodo(pos)
            elif evento.button == 3:  # Click derecho para seleccionar nodos y crear conexiones
                for nodo in nodos:
                    if distancia(nodo, pos) < RADIO_NODO + 5:
                        if nodo_seleccionado is None:
                            nodo_seleccionado = nodo
                        else:
                            agregar_conexion(nodo_seleccionado, nodo)
                            nodo_seleccionado = None
                        break
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE and nodo_inicio and nodo_fin:
                # Ejecutar Dijkstra con animación y calcular el camino más corto
                camino = dijkstra_animado(nodo_inicio, nodo_fin)
            elif evento.key == pygame.K_ESCAPE:
                # Limpiar el estado al presionar ESC
                limpiar()

    pygame.display.update()

pygame.quit()
