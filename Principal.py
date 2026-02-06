Principal
# principal.py
from partida import Partida

def pedir_lista_jugadores():
    jugadores = input("Introduce la lista de jugadores (separados por coma): ")
    return [j.strip() for j in jugadores.split(",") if j.strip()]

def pedir_palabra():
    return input("Introduce la palabra secreta: ").strip()

def pedir_entero(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Por favor, introduce un número válido.")

def main():
    print("=== Configuración de la partida ===")

    palabra_secreta = pedir_palabra()
    jugadores = pedir_lista_jugadores()
    num_impostores = pedir_entero("Número de impostores: ")
    num_rondas = pedir_entero("Número de rondas: ")

    partida = Partida(palabra_secreta, jugadores, num_impostores, num_rondas)

    print("\n=== Información inicial (solo para pruebas) ===")
    for jugador in jugadores:
        conoce = "CONOCE la palabra" if partida.jugador_conoce_palabra(jugador) else "NO conoce la palabra"
        print(f"{jugador}: {conoce}")

    print("\n=== Comienza la partida ===")

    for ronda in range(1, num_rondas + 1):
        print(f"\n--- Ronda {ronda} ---")

        # Palabras relacionadas
        palabras_dichas = {}
        for jugador in jugadores:
            palabra = input(f"{jugador}, di una palabra relacionada: ")
            palabras_dichas[jugador] = palabra

        # Votaciones
        votos = {}
        print("\n--- Votación ---")
        for jugador in jugadores:
            while True:
                voto = input(f"{jugador}, vota a alguien: ").strip()
                if voto in jugadores:
                    votos[jugador] = voto
                    break
                else:
                    print("Jugador no válido. Intenta de nuevo.")

        expulsado = partida.votar(votos)
        print(f"\nJugador expulsado: {expulsado}")

        partida.siguiente_ronda()

    print("\n=== Fin de la partida ===")

if __name__ == "__main__":
    main()
