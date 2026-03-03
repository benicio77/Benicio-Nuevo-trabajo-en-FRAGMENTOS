# partida.py

import random

class Partida:
    def __init__(self, nombre_partida: str, numero_jugadores: int):
        self.nombre_partida = nombre_partida
        self.numero_jugadores = numero_jugadores

        self.jugadores = []
        self.palabra_secreta = None
        self.roles_asignados = {}
        self.ronda_actual = 0
        self.tiempo_restante = 0

        # Diccionario para almacenar votos: {jugador: objetivo}
        self.votos = {}

    # ---------------------------------------------------------
    # Asignar roles (1 impostor, resto normales)
    # ---------------------------------------------------------
    def asignar_roles(self):
        if not self.jugadores:
            return

        impostor = random.choice(self.jugadores)

        for jugador in self.jugadores:
            self.roles_asignados[jugador] = (
                "impostor" if jugador == impostor else "normal"
            )

    # ---------------------------------------------------------
    # Elegir palabra secreta
    # ---------------------------------------------------------
    def generar_palabra_secreta(self, lista_palabras):
        if not lista_palabras:
            return

        self.palabra_secreta = random.choice(lista_palabras)

    # ---------------------------------------------------------
    # Avanzar ronda
    # ---------------------------------------------------------
    def avanzar_ronda(self):
        self.ronda_actual += 1
        self.tiempo_restante = 0

    # ---------------------------------------------------------
    # Registrar voto (solo guarda datos, no decide nada)
    # ---------------------------------------------------------
    def registrar_voto(self, jugador, objetivo):
        self.votos[jugador] = objetivo
