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
    # Mostrar palabra secreta
    # ---------------------------------------------------------
    def mostrar_palabra(self, pantalla, palabra):
        pantalla.fill((0, 0, 0))

        fuente = pygame.font.SysFont(None, 80)
        texto = fuente.render(f"Palabra: {palabra}", True, (255, 255, 255))

        rect = texto.get_rect(center=(pantalla.get_width() // 2,
                                      pantalla.get_height() // 2))

        pantalla.blit(texto, rect)

    # ---------------------------------------------------------
    # Mostrar pantalla de votación
    # ---------------------------------------------------------
    def mostrar_votacion(self, pantalla, jugadores):
        pantalla.fill((30, 30, 30))
        fuente = pygame.font.SysFont(None, 50)

        ancho_boton = 300
        alto_boton = 60
        espacio = 20

        total_altura = len(jugadores) * (alto_boton + espacio)
        inicio_y = (pantalla.get_height() - total_altura) // 2

        for i, jugador in enumerate(jugadores):
            x = (pantalla.get_width() - ancho_boton) // 2
            y = inicio_y + i * (alto_boton + espacio)

            rect = pygame.Rect(x, y, ancho_boton, alto_boton)
            pygame.draw.rect(pantalla, (70, 70, 200), rect, border_radius=10)

            texto = fuente.render(jugador, True, (255, 255, 255))
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
    # Mostrar pantalla final
    # ---------------------------------------------------------
    def mostrar_fin(self, pantalla, ganador):
        pantalla.fill((0, 0, 0))

        fuente_titulo = pygame.font.SysFont(None, 90)
        fuente_ganador = pygame.font.SysFont(None, 70)

        titulo = fuente_titulo.render("Fin de la partida", True, (255, 255, 255))
        rect_titulo = titulo.get_rect(center=(pantalla.get_width() // 2, 150))
        pantalla.blit(titulo, rect_titulo)

        texto_ganador = fuente_ganador.render(f"Ganador: {ganador}", True, (255, 215, 0))
        rect_ganador = texto_ganador.get_rect(center=(pantalla.get_width() // 2,
                                                      pantalla.get_height() // 2))
        pantalla.blit(texto_ganador, rect_ganador)
