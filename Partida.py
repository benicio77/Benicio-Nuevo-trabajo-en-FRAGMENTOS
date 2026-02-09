Partida
import random
from collections import Counter

class Partida:
    def __init__(self, palabra_secreta, jugadores, num_impostores=1, rondas=3):
        self.palabra_secreta = palabra_secreta
        self.jugadores = jugadores[:]  # Copia para evitar modificar la lista original
        self.num_impostores = num_impostores
        self.rondas_totales = rondas
        self.ronda_actual = 1

        self.impostores = set()
        self.asignaciones = {}

        self._asignar_roles()

    def _asignar_roles(self):
        """Asigna impostores y palabras a cada jugador."""
        self.impostores = set(random.sample(self.jugadores, self.num_impostores))
        self.asignaciones = {
            jugador: (None if jugador in self.impostores else self.palabra_secreta)
            for jugador in self.jugadores
        }

    def obtener_palabra_jugador(self, jugador):
        """Devuelve la palabra del jugador o None si es impostor."""
        return self.asignaciones.get(jugador)

    def siguiente_ronda(self):
        """Avanza a la siguiente ronda si quedan."""
        if self.ronda_actual < self.rondas_totales:
            self.ronda_actual += 1
            return True
        return False

    def votar(self, votos):
        """
        Recibe un diccionario {jugador: voto} y devuelve:
        - expulsado (str)
        - era_impostor (bool)
        """
        conteo = Counter(votos.values())
        if not conteo:
            return None, False

        expulsado, _ = conteo.most_common(1)[0]
        era_impostor = expulsado in self.impostores

        return expulsado, era_impostor

    def eliminar_jugador(self, jugador):
        """Elimina al jugador de la partida completamente."""
        if jugador in self.jugadores:
            self.jugadores.remove(jugador)
        self.asignaciones.pop(jugador, None)
        self.impostores.discard(jugador)
