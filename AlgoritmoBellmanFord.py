
import pygame
import math
import time

# Configuración de pantalla y colores
ANCHO, ALTO = 800, 600
RADIO_NODO = 20
DISTANCIA_MINIMA = 30
COLOR_FONDO = (0, 0, 0)          # Negro
COLOR_NODO = (0, 0, 255)         # Azul
COLOR_INICIAL = (0, 255, 0)      # Verde
COLOR_FINAL = (255, 0, 0)        # Rojo
COLOR_LINEA = (255, 255, 255)    # Blanco (peso positivo)
COLOR_LINEA_NEGATIVA = (255, 0, 0)  # Rojo (peso negativo)
COLOR_CAMINO = (255, 255, 0)     # Amarillo
COLOR_TEXTO = (255, 255, 255)

pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Visualización del Algoritmo de Bellman-Ford")
fuente = pygame.font.SysFont(None, 24)

# Estructuras de datos
nodos = []
conexiones = {}
letras_nodos = {}
nodo_inicio = None
nodo_fin = None
camino = []

# Funciones auxiliares


def distancia(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def reiniciar():
    """Reinicia todos los datos al presionar ESC."""
    global nodos, conexiones, letras_nodos, camino, nodo_inicio, nodo_fin
    nodos.clear()
    conexiones.clear()
    letras_nodos.clear()
    nodo_inicio = None
    nodo_fin = None
    camino = []


def agregar_nodo(pos):
    for nodo in nodos:
        if distancia(nodo, pos) < DISTANCIA_MINIMA:
            mostrar_alerta("Nodo muy cerca de otro nodo existente.")
            return
    nodo_id = len(nodos) + 1
    nodos.append(pos)
    letras_nodos[pos] = str(nodo_id)
    conexiones[pos] = []


def pedir_peso():
    """Pide el peso de la conexión entre los nodos seleccionados."""
    texto = fuente.render(
        "Introduce el peso de la conexión: ", True, COLOR_TEXTO)
    pantalla.blit(texto, (10, 10))
    pygame.display.update()

    input_text = ""
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return None
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    try:
                        peso = float(input_text)
                        return peso
                    except ValueError:
                        mostrar_alerta(
                            "Por favor, introduce un número válido.")
                        input_text = ""
                elif evento.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += evento.unicode

                # Mostrar el texto de entrada en pantalla
                pantalla.fill(COLOR_FONDO)
                pantalla.blit(texto, (10, 10))
                texto_input = fuente.render(input_text, True, COLOR_TEXTO)
                pantalla.blit(texto_input, (10, 40))
                pygame.display.update()


def agregar_conexion(n1, n2):
    """Agrega una conexión entre dos nodos con un peso proporcionado por el usuario."""
    peso = pedir_peso()
    if peso is None:
        return  # Salir si no se introduce un peso válido

    color_linea = COLOR_LINEA_NEGATIVA if peso < 0 else COLOR_LINEA
    conexiones[n1].append((n2, peso))
    dibujar()


def bellman_ford_animado(nodo_inicio, nodo_fin):
    distancias = {nodo: float('inf') for nodo in nodos}
    distancias[nodo_inicio] = 0
    predecesores = {nodo: None for nodo in nodos}

    for i in range(len(nodos) - 1):
        hubo_actualizacion = False
        for u in conexiones:
            for v, peso in conexiones[u]:
                if distancias[u] != float('inf') and distancias[u] + peso < distancias[v]:
                    distancias[v] = distancias[u] + peso
                    predecesores[v] = u
                    hubo_actualizacion = True

        # Animación del proceso
        dibujar()
        pygame.display.update()

        if not hubo_actualizacion:
            break  # Si no hubo cambios, terminamos antes

    # Comprobación de ciclos negativos
    for u in conexiones:
        for v, peso in conexiones[u]:
            if distancias[u] != float('inf') and distancias[u] + peso < distancias[v]:
                mostrar_alerta(
                    "¡Ciclo negativo detectado! No se puede calcular el camino.")
                return None

    # Reconstrucción del camino más corto
    camino = []
    nodo_actual = nodo_fin
    while nodo_actual is not None:
        camino.insert(0, nodo_actual)
        nodo_actual = predecesores[nodo_actual]

    # Verificar si el nodo inicial no está conectado al nodo final
    if camino[0] != nodo_inicio:
        mostrar_alerta(
            "No hay camino entre el nodo de inicio y el nodo final.")
        return None

    return camino


def dibujar():
    pantalla.fill(COLOR_FONDO)

    # Dibujamos las conexiones y mostramos los pesos
    for n1 in conexiones:
        for n2, peso in conexiones[n1]:
            color_linea = COLOR_LINEA if peso > 0 else COLOR_LINEA_NEGATIVA
            pygame.draw.line(pantalla, color_linea, n1, n2, 2)

            # Mostrar el peso de la conexión
            medio = ((n1[0] + n2[0]) // 2, (n1[1] + n2[1]) // 2)
            texto_peso = fuente.render(f'{peso:.1f}', True, COLOR_TEXTO)
            pantalla.blit(
                texto_peso, (medio[0] - texto_peso.get_width() // 2, medio[1] - texto_peso.get_height() // 2))

    for nodo in nodos:
        color = COLOR_NODO
        if nodo == nodo_inicio:
            color = COLOR_INICIAL
        elif nodo == nodo_fin:
            color = COLOR_FINAL
        pygame.draw.circle(pantalla, color, nodo, RADIO_NODO)

        letra = letras_nodos[nodo]
        texto = fuente.render(letra, True, COLOR_TEXTO)
        pantalla.blit(
            texto, (nodo[0] - texto.get_width() // 2, nodo[1] - texto.get_height() // 2))

    if camino:
        for i in range(len(camino) - 1):
            pygame.draw.line(pantalla, COLOR_CAMINO,
                             camino[i], camino[i + 1], 3)

    pygame.display.flip()


def mostrar_alerta(texto):
    pantalla.fill(COLOR_FONDO)
    alerta_texto = fuente.render(texto, True, COLOR_TEXTO)
    pantalla.blit(alerta_texto, (10, ALTO - 30))
    pygame.display.update()
    time.sleep(2)


# Ejecución inicial
reiniciar()

nodo_seleccionado = None
ejecutando = True

while ejecutando:
    dibujar()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            pos = evento.pos
            if evento.button == 1:
                agregar_nodo(pos)
            elif evento.button == 3:
                for nodo in nodos:
                    if distancia(nodo, pos) < RADIO_NODO + 5:
                        if nodo_seleccionado is None:
                            nodo_seleccionado = nodo
                        else:
                            agregar_conexion(nodo_seleccionado, nodo)
                            nodo_seleccionado = None
                        break
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                reiniciar()
            elif evento.key == pygame.K_s:  # Seleccionar nodo inicial
                for nodo in nodos:
                    if distancia(nodo, pygame.mouse.get_pos()) < RADIO_NODO + 5:
                        nodo_inicio = nodo
                        break
            elif evento.key == pygame.K_f:  # Seleccionar nodo final
                for nodo in nodos:
                    if distancia(nodo, pygame.mouse.get_pos()) < RADIO_NODO + 5:
                        nodo_fin = nodo
                        break
            elif evento.key == pygame.K_SPACE and nodo_inicio and nodo_fin:
                camino = bellman_ford_animado(nodo_inicio, nodo_fin)

pygame.quit()
