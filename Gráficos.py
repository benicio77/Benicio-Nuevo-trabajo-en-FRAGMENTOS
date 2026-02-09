import pygame
import sys

class Graficos:
    def __init__(self, ancho=800, alto=600):
        pygame.init()
        self.ventana = pygame.display.set_mode((ancho, alto))
        pygame.display.set_caption("Juego")
        self.fondo = None

    def cargar_fondo(self, ruta):
        try:
            self.fondo = pygame.image.load(ruta).convert()
        except pygame.error:
            print(f"Error: no se pudo cargar la imagen '{ruta}'")
            self.fondo = None

    def dibujar_fondo(self):
        if self.fondo:
            self.ventana.blit(self.fondo, (0, 0))
        else:
            self.ventana.fill((0, 0, 0))  # Fondo negro si no hay imagen

    def actualizar(self):
        pygame.display.update()

    def cerrar_si_solicitado(self):
        """Permite cerrar la ventana correctamente."""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
