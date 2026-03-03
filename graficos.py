# graficos.py

import pygame

class Graficos:
    def __init__(self):
        pass

    # ---------------------------------------------------------
    # Mostrar rol del jugador
    # ---------------------------------------------------------
    def mostrar_rol(self, pantalla, rol):
        pantalla.fill((0, 0, 0))

        fuente = pygame.font.SysFont(None, 80)
        texto = fuente.render(f"Tu rol: {rol}", True, (255, 255, 255))

        rect = texto.get_rect(center=(pantalla.get_width() // 2,
                                      pantalla.get_height() // 2))

        pantalla.blit(texto, rect)

    # ---------------------------------------------------------
    # Mostrar palabra secreta con instrucción
    # ---------------------------------------------------------
    def mostrar_palabra(self, pantalla, palabra, jugador_num=None):
        # Si es impostor, mostrar en rojo con fondo rojo
        if palabra == "impostor":
            pantalla.fill((139, 0, 0))  # Fondo rojo oscuro
            
            fuente_palabra = pygame.font.SysFont(None, 150)
            texto = fuente_palabra.render("IMPOSTOR", True, (255, 0, 0))  # Texto rojo brillante
            rect = texto.get_rect(center=(pantalla.get_width() // 2, pantalla.get_height() // 2 - 50))
            pantalla.blit(texto, rect)
        else:
            # Para palabras normales
            pantalla.fill((0, 0, 0))

            fuente_nombre = pygame.font.SysFont(None, 60)
            fuente_palabra = pygame.font.SysFont(None, 80)

            if jugador_num:
                nombre_texto = fuente_nombre.render(f"Jugador {jugador_num}", True, (255, 255, 255))
                rect_nombre = nombre_texto.get_rect(center=(pantalla.get_width() // 2, 80))
                pantalla.blit(nombre_texto, rect_nombre)

            palabra_texto = fuente_palabra.render(f"Palabra: {palabra}", True, (255, 255, 255))
            rect_palabra = palabra_texto.get_rect(center=(pantalla.get_width() // 2,
                                                          pantalla.get_height() // 2 - 50))
            pantalla.blit(palabra_texto, rect_palabra)

        fuente_instruccion = pygame.font.SysFont(None, 40)
        instruccion = fuente_instruccion.render("Presiona ENTER para continuar", True, (100, 100, 100))
        rect_instruccion = instruccion.get_rect(center=(pantalla.get_width() // 2,
                                                        pantalla.get_height() - 100))
        pantalla.blit(instruccion, rect_instruccion)

    # ---------------------------------------------------------
    # Mostrar pantalla de transición entre jugadores
    # ---------------------------------------------------------
    def mostrar_transicion(self, pantalla, jugador_siguiente):
        pantalla.fill((0, 0, 0))

        fuente = pygame.font.SysFont(None, 50)
        fuente_instruccion = pygame.font.SysFont(None, 40)

        texto = fuente.render(f"Turno del Jugador {jugador_siguiente}", True, (255, 255, 255))
        rect = texto.get_rect(center=(pantalla.get_width() // 2, pantalla.get_height() // 2 - 100))
        pantalla.blit(texto, rect)

        instruccion = fuente_instruccion.render("Presiona ENTER para comenzar", True, (100, 100, 100))
        rect_instruccion = instruccion.get_rect(center=(pantalla.get_width() // 2,
                                                        pantalla.get_height() // 2 + 50))
        pantalla.blit(instruccion, rect_instruccion)

    # ---------------------------------------------------------
    # Mostrar votación individual (preguntando a qué jugador votar)
    # ---------------------------------------------------------
    def mostrar_votacion_individual(self, pantalla, numero_jugador_actual, numero_total_jugadores):
        pantalla.fill((30, 30, 30))
        fuente_pregunta = pygame.font.SysFont(None, 50)
        fuente_boton = pygame.font.SysFont(None, 40)

        pregunta = fuente_pregunta.render(f"¿Jugador {numero_jugador_actual} a quién votas?", True, (255, 255, 255))
        rect_pregunta = pregunta.get_rect(center=(pantalla.get_width() // 2, 60))
        pantalla.blit(pregunta, rect_pregunta)

        ancho_boton = 300
        alto_boton = 50
        espacio = 15

        # Crear lista de otros jugadores (números)
        otros_jugadores_numeros = [i for i in range(1, numero_total_jugadores + 1) if i != numero_jugador_actual]

        total_altura = len(otros_jugadores_numeros) * (alto_boton + espacio)
        inicio_y = (pantalla.get_height() - total_altura) // 2

        for i, numero_jugador in enumerate(otros_jugadores_numeros):
            x = (pantalla.get_width() - ancho_boton) // 2
            y = inicio_y + i * (alto_boton + espacio)

            rect = pygame.Rect(x, y, ancho_boton, alto_boton)
            pygame.draw.rect(pantalla, (70, 70, 200), rect, border_radius=10)

            texto = fuente_boton.render(f"Jugador {numero_jugador}", True, (255, 255, 255))
            texto_rect = texto.get_rect(center=rect.center)

            pantalla.blit(texto, texto_rect)

    # ---------------------------------------------------------
    # Mostrar resultados de la votación
    # ---------------------------------------------------------
    def mostrar_resultados_votacion(self, pantalla, votos):
        pantalla.fill((0, 0, 0))

        fuente_titulo = pygame.font.SysFont(None, 70)
        fuente_lista = pygame.font.SysFont(None, 50)

        titulo = fuente_titulo.render("Resultados de la votación", True, (255, 255, 255))
        rect_titulo = titulo.get_rect(center=(pantalla.get_width() // 2, 80))
        pantalla.blit(titulo, rect_titulo)

        conteo = {}
        for votante, objetivo in votos.items():
            conteo[objetivo] = conteo.get(objetivo, 0) + 1

        resultados = sorted(conteo.items(), key=lambda x: x[1], reverse=True)

        inicio_y = 180
        espacio = 50

        for i, (jugador, cantidad) in enumerate(resultados):
            texto = fuente_lista.render(f"{jugador}: {cantidad} voto(s)", True, (255, 255, 255))
            rect = texto.get_rect(center=(pantalla.get_width() // 2,
                                          inicio_y + i * espacio))
            pantalla.blit(texto, rect)

    # ---------------------------------------------------------
    # Mostrar pantalla final con ganador
    # ---------------------------------------------------------
    def mostrar_fin(self, pantalla, ganador):
        pantalla.fill((0, 0, 0))

        fuente_titulo = pygame.font.SysFont(None, 90)
        fuente_ganador = pygame.font.SysFont(None, 70)

        titulo = fuente_titulo.render("Fin de la partida", True, (255, 255, 255))
        rect_titulo = titulo.get_rect(center=(pantalla.get_width() // 2, 150))
        pantalla.blit(titulo, rect_titulo)

        # Mostrar ganador en verde
        color_verde = (0, 255, 0)
        if "inocentes" in ganador.lower():
            texto_ganador = fuente_ganador.render(f"¡{ganador} ganan!", True, color_verde)
        elif "impostor" in ganador.lower():
            texto_ganador = fuente_ganador.render(f"¡{ganador} gana!", True, color_verde)
        else:
            texto_ganador = fuente_ganador.render(f"{ganador}", True, color_verde)

        rect_ganador = texto_ganador.get_rect(center=(pantalla.get_width() // 2,
                                                      pantalla.get_height() // 2))
        pantalla.blit(texto_ganador, rect_ganador)

    # ---------------------------------------------------------
    # Mostrar mensaje de guardado
    # ---------------------------------------------------------
    def mostrar_guardado(self, pantalla, archivo_guardado):
        pantalla.fill((0, 0, 0))

        fuente = pygame.font.SysFont(None, 60)
        texto = fuente.render(f"Guardado: {archivo_guardado}", True, (255, 255, 0))
        rect = texto.get_rect(center=(pantalla.get_width() // 2,
                                      pantalla.get_height() // 2))
        pantalla.blit(texto, rect)

        fuente_inst = pygame.font.SysFont(None, 40)
        instruccion = fuente_inst.render("Presiona ENTER para continuar", True, (100, 100, 100))
        rect_inst = instruccion.get_rect(center=(pantalla.get_width() // 2,
                                                   pantalla.get_height() - 100))
        pantalla.blit(instruccion, rect_inst)
