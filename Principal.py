
# principal.py

import pygame
from graficos import Graficos
from partida import Partida


# ---------------------------------------------------------
# 1. manejar_click()
# ---------------------------------------------------------
def manejar_click(posicion, partida, pantalla_actual):
    x, y = posicion

    if pantalla_actual == "rol":
        return {"accion": "continuar"}

    if pantalla_actual == "palabra":
        return {"accion": "continuar"}

    if pantalla_actual == "votacion":
        ancho_boton = 300
        alto_boton = 60
        espacio = 20

        total_altura = len(partida.jugadores) * (alto_boton + espacio)
        inicio_y = (600 - total_altura) // 2
        inicio_x = (800 - ancho_boton) // 2

        for i, jugador in enumerate(partida.jugadores):
            bx = inicio_x
            by = inicio_y + i * (alto_boton + espacio)

            if bx <= x <= bx + ancho_boton and by <= y <= by + alto_boton:
                return {"accion": "votar", "objetivo": jugador}

        return {"accion": "ninguna"}

    if pantalla_actual == "resultados":
        return {"accion": "continuar"}

    if pantalla_actual == "fin":
        return {"accion": "salir"}

    return {"accion": "ninguna"}


# ---------------------------------------------------------
# 2. manejar_tecla()
# ---------------------------------------------------------
def manejar_tecla(tecla, partida, pantalla_actual):
    if pantalla_actual == "rol" and tecla == "ENTER":
        return {"accion": "continuar"}

    if pantalla_actual == "palabra" and tecla == "ENTER":
        return {"accion": "continuar"}

    if pantalla_actual == "votacion":
        if tecla == "ESC":
            return {"accion": "cancelar_votacion"}
        if tecla == "ENTER":
            return {"accion": "confirmar_voto"}

    if pantalla_actual == "resultados" and tecla == "ENTER":
        return {"accion": "continuar"}

    if pantalla_actual == "fin" and tecla == "ENTER":
        return {"accion": "salir"}

    if tecla == "R":
        return {"accion": "avanzar_ronda"}

    if tecla == "ESC":
        return {"accion": "salir"}

    return {"accion": "ninguna"}


# ---------------------------------------------------------
# 3. iniciar_partida()
# ---------------------------------------------------------
def iniciar_partida():
    nombre = input("Nombre de la partida: ")

    while True:
        try:
            num = int(input("Número de jugadores: "))
            if num > 0:
                break
        except ValueError:
            pass
        print("Introduce un número válido.")

    partida = Partida(nombre, num)

    print("\nIntroduce los nombres de los jugadores:")
    for i in range(num):
        nombre_jugador = input(f"Jugador {i+1}: ")
        partida.jugadores.append(nombre_jugador)

    partida.asignar_roles()

    print("\nIntroduce palabras posibles (separadas por comas):")
    lista = input("Palabras: ").split(",")
    lista = [p.strip() for p in lista if p.strip()]

    partida.generar_palabra_secreta(lista)

    return partida


# ---------------------------------------------------------
# 4. bucle_principal()
# ---------------------------------------------------------
def bucle_principal():
    pygame.init()

    pantalla = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Juego de Impostor")
    reloj = pygame.time.Clock()

    graficos = Graficos()
    partida = Partida("Partida 1", 4)
    partida.jugadores = ["Ana", "Luis", "Marta", "Pedro"]
    
    # Asignar roles y palabra secreta
    partida.asignar_roles()
    lista_palabras = ["gato", "perro", "casa", "sol", "luna"]
    partida.generar_palabra_secreta(lista_palabras)
    
    # Rastrear jugador actual y votos temporales
    jugador_actual = 0
    voto_actual = None

    pantalla_actual = "rol"
    ejecutando = True

    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                accion = manejar_click(pos, partida, pantalla_actual)

                if accion["accion"] == "votar":
                    voto_actual = accion["objetivo"]
                    pantalla_actual = "resultados"

                elif accion["accion"] == "continuar":
                    if pantalla_actual == "rol":
                        pantalla_actual = "palabra"
                    elif pantalla_actual == "palabra":
                        pantalla_actual = "votacion"
                    elif pantalla_actual == "resultados":
                        pantalla_actual = "fin"

                elif accion["accion"] == "salir":
                    ejecutando = False

            if evento.type == pygame.KEYDOWN:
                tecla = pygame.key.name(evento.key).upper()
                accion = manejar_tecla(tecla, partida, pantalla_actual)

                if accion["accion"] == "avanzar_ronda":
                    partida.avanzar_ronda()

                elif accion["accion"] == "continuar":
                    if pantalla_actual == "rol":
                        pantalla_actual = "palabra"
                    elif pantalla_actual == "palabra":
                        pantalla_actual = "votacion"
                    elif pantalla_actual == "resultados":
                        # Avanzar al siguiente jugador o terminar
                        if jugador_actual < len(partida.jugadores) - 1:
                            jugador_actual += 1
                            pantalla_actual = "rol"
                        else:
                            pantalla_actual = "fin"

                elif accion["accion"] == "salir":
                    ejecutando = False

        if pantalla_actual == "rol":
            rol = partida.roles_asignados.get(partida.jugadores[jugador_actual], "normal")
            graficos.mostrar_rol(pantalla, rol)

        elif pantalla_actual == "palabra":
            rol_actual = partida.roles_asignados.get(partida.jugadores[jugador_actual], "normal")
            if rol_actual == "impostor":
                graficos.mostrar_palabra(pantalla, "???")
            else:
                graficos.mostrar_palabra(pantalla, partida.palabra_secreta or "desconocida")

        elif pantalla_actual == "votacion":
            graficos.mostrar_votacion(pantalla, partida.jugadores)

        elif pantalla_actual == "resultados":
            if voto_actual:
                partida.registrar_voto(partida.jugadores[jugador_actual], voto_actual)
                voto_actual = None
            graficos.mostrar_resultados_votacion(pantalla, partida.votos)

        elif pantalla_actual == "fin":
            graficos.mostrar_fin(pantalla, "Jugadores")

        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()


# ---------------------------------------------------------
# Iniciar el juego
# ---------------------------------------------------------
if __name__ == "__main__":
    bucle_principal()
