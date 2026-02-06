Partida
import random
from collections import Counter

class Partida:
    def __init__(self, palabra_secreta, jugadores, num_impostores=1, rondas=3):
        self.palabra_secreta = palabra_secreta
        self.jugadores = jugadores
        self.num_impostores = num_impostores
        self.rondas_totales = rondas
        self.ronda_actual = 1

        self.impostores = set()
        self.asignaciones = {}

        self._asignar_roles()

    def _asignar_roles(self):
        self.impostores = set(random.sample(self.jugadores, self.num_impostores))
        self.asignaciones = {
            jugador: (None if jugador in self.impostores else self.palabra_secreta)
            for jugador in self.jugadores
        }

    def obtener_palabra_jugador(self, jugador):
        return self.asignaciones.get(jugador)

    def siguiente_ronda(self):
        if self.ronda_actual < self.rondas_totales:
            self.ronda_actual += 1
            return True
        return False

    def votar(self, votos):
        conteo = Counter(votos.values())
        if not conteo:
            return None, False

        expulsado, _ = conteo.most_common(1)[0]
        era_impostor = expulsado in self.impostores

        return expulsado, era_impostor
