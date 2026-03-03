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
    # Asignar roles (múltiples impostores, resto normales)
    # ---------------------------------------------------------
    def asignar_roles(self, num_impostores=1):
        if not self.jugadores or num_impostores <= 0:
            return

        num_impostores = min(num_impostores, len(self.jugadores) - 1)
        impostores = random.sample(self.jugadores, num_impostores)

        for jugador in self.jugadores:
            self.roles_asignados[jugador] = (
                "impostor" if jugador in impostores else "normal"
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

    # ---------------------------------------------------------
    # Determinar ganador basado en votos
    # ---------------------------------------------------------
    def determinar_ganador(self):
        """
        Retorna:
        - "impostores" si los impostores ganaron (un inocente fue eliminado)
        - "inocentes" si los inocentes ganaron (un impostor fue eliminado)
        """
        if not self.votos:
            return None

        # Contar votos
        conteo = {}
        for votante, objetivo in self.votos.items():
            conteo[objetivo] = conteo.get(objetivo, 0) + 1

        # Obtener el jugador eliminado (el con más votos)
        eliminado = max(conteo, key=conteo.get)

        # Verificar si es impostor
        if self.roles_asignados.get(eliminado) == "impostor":
            return "inocentes"
        else:
            return "impostores"
