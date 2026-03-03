
# principal.py

import pygame
from graficos import Graficos
from partida import Partida
from juego import guardar_partida  # módulo nuevo que simplemente escribe un guardado sin alterar la partida


# ---------------------------------------------------------
# 1. manejar_click()
# ---------------------------------------------------------
def manejar_click(posicion, partida, pantalla_actual, jugador_actual=None):
    x, y = posicion

    if pantalla_actual == "palabra":
        return {"accion": "continuar"}

    if pantalla_actual == "votacion":
        ancho_boton = 300
        alto_boton = 50
        espacio = 15

        # Crear lista de índices de otros jugadores
        otros_jugadores_indices = [i for i in range(len(partida.jugadores)) if i != jugador_actual]

        total_altura = len(otros_jugadores_indices) * (alto_boton + espacio)
        inicio_y = (600 - total_altura) // 2
        inicio_x = (800 - ancho_boton) // 2

        for i, indice_jugador in enumerate(otros_jugadores_indices):
            bx = inicio_x
            by = inicio_y + i * (alto_boton + espacio)

            if bx <= x <= bx + ancho_boton and by <= y <= by + alto_boton:
                # Retornar el nombre del jugador votado
                return {"accion": "votar", "objetivo": partida.jugadores[indice_jugador]}

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
    # Cualquier RETURN continúa (excepto en fin)
    if tecla == "RETURN":
        if pantalla_actual == "fin":
            return {"accion": "salir"}
        else:
            return {"accion": "continuar"}

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

    while True:
        try:
            num_impostores = int(input(f"Número de impostores (máximo {num - 1}): "))
            if 0 < num_impostores < num:
                break
        except ValueError:
            pass
        print("Introduce un número válido.")

    partida = Partida(nombre, num)

    print("\nIntroduce los nombres de los jugadores:")
    for i in range(num):
        nombre_jugador = input(f"Jugador {i+1}: ")
        partida.jugadores.append(nombre_jugador)

    partida.asignar_roles(num_impostores)

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
    
    # Crear partida o usar la interactiva
    partida = Partida("Partida 1", 4)
    partida.jugadores = ["Ana", "Luis", "Marta", "Pedro"]
    partida.asignar_roles(1)  # 1 impostor
    lista_palabras = ["gato", "perro", "casa", "sol", "luna"]
    partida.generar_palabra_secreta(lista_palabras)
    
    # Estados del juego
    FASE_TRANSICION = 0  # Pantalla de transición entre jugadores
    FASE_PALABRA = 1  # Mostrar palabra a cada jugador
    FASE_VOTACION = 2  # Votación
    FASE_RESULTADOS = 3  # Resultados
    FASE_FIN = 4  # Fin del juego
    
    fase_actual = FASE_TRANSICION
    jugador_actual = 0
    voto_actual = None
    en_fase_palabras = True  # Rastrear si aún estamos en la fase de ver palabras

    # Variables para el guardado "random"
    guardado_activo = False
    guardado_archivo = None
    
    ejecutando = True

    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                accion = manejar_click(pos, partida, 
                                      "votacion" if fase_actual == FASE_VOTACION else "palabra",
                                      jugador_actual)

                if accion["accion"] == "votar":
                    voto_actual = accion["objetivo"]
                    # Registrar voto
                    partida.registrar_voto(partida.jugadores[jugador_actual], voto_actual)
                    
                    # Avanzar al siguiente jugador o a resultados
                    jugador_actual += 1
                    voto_actual = None
                    
                    if jugador_actual >= len(partida.jugadores):
                        # Todos votaron
                        fase_actual = FASE_RESULTADOS
                        jugador_actual = 0
                    else:
                        # Mostrar transición al siguiente jugador de votación
                        fase_actual = FASE_TRANSICION

                elif accion["accion"] == "continuar":
                    if fase_actual == FASE_PALABRA:
                        jugador_actual += 1
                        if jugador_actual >= len(partida.jugadores):
                            # Todos vieron su palabra, ir a transición de votación
                            fase_actual = FASE_TRANSICION
                        else:
                            # Mostrar transición al siguiente jugador
                            fase_actual = FASE_TRANSICION

                elif accion["accion"] == "salir":
                    ejecutando = False

            if evento.type == pygame.KEYDOWN:
                tecla = pygame.key.name(evento.key).upper()

                # si estamos mostrando el mensaje de guardado, sólo ENTER lo cierra
                if guardado_activo:
                    if tecla == "RETURN":
                        guardado_activo = False
                    continue

                pantalla_para_tecla = "fin" if fase_actual == FASE_FIN else "resultados" if fase_actual == FASE_RESULTADOS else "votacion" if fase_actual == FASE_VOTACION else "palabra"
                accion = manejar_tecla(tecla, partida, pantalla_para_tecla)

                # tecla G: crear guardado sin afectar el juego
                if tecla == "G":
                    ruta = guardar_partida(partida)
                    guardado_archivo = ruta or "error_guardado"
                    guardado_activo = True
                    continue

                if accion["accion"] == "continuar":
                    if fase_actual == FASE_TRANSICION:
                        if en_fase_palabras:
                            # Estamos en fase de ver palabras
                            if jugador_actual < len(partida.jugadores):
                                # Mostrar palabra del jugador actual
                                fase_actual = FASE_PALABRA
                            else:
                                # Esto no debería pasar
                                pass
                        else:
                            # Estamos en fase de votación, mostrar votación
                            if jugador_actual < len(partida.jugadores):
                                fase_actual = FASE_VOTACION
                            else:
                                # Todos votaron
                                fase_actual = FASE_RESULTADOS
                    
                    elif fase_actual == FASE_PALABRA:
                        # Pasar al siguiente jugador
                        jugador_actual += 1
                        if jugador_actual >= len(partida.jugadores):
                            # Todos vieron palabra, cambiar a votación
                            en_fase_palabras = False
                            jugador_actual = 0
                        fase_actual = FASE_TRANSICION

                    elif fase_actual == FASE_VOTACION:
                        # Pasar al siguiente votante
                        jugador_actual += 1
                        if jugador_actual >= len(partida.jugadores):
                            # Todos votaron
                            fase_actual = FASE_RESULTADOS
                        else:
                            # Ir a transición del siguiente votante
                            fase_actual = FASE_TRANSICION

                    elif fase_actual == FASE_RESULTADOS:
                        fase_actual = FASE_FIN

                elif accion["accion"] == "salir":
                    ejecutando = False

        # Si estamos mostrando el guardado, no se procesa ninguna otra fase
        if guardado_activo:
            graficos.mostrar_guardado(pantalla, guardado_archivo)
        else:
            # Renderizar según fase actual
            if fase_actual == FASE_TRANSICION:
                if en_fase_palabras:
                    # Transición entre palabras
                    if jugador_actual < len(partida.jugadores):
                        graficos.mostrar_transicion(pantalla, jugador_actual + 1)
                else:
                    # Transición de votación
                    if jugador_actual < len(partida.jugadores):
                        graficos.mostrar_transicion(pantalla, f"Votación - Jugador {jugador_actual + 1}")

            elif fase_actual == FASE_PALABRA:
                rol_actual = partida.roles_asignados.get(partida.jugadores[jugador_actual], "normal")
                if rol_actual == "impostor":
                    graficos.mostrar_palabra(pantalla, "impostor", jugador_actual + 1)
                else:
                    graficos.mostrar_palabra(pantalla, partida.palabra_secreta or "desconocida", jugador_actual + 1)

            elif fase_actual == FASE_VOTACION:
                graficos.mostrar_votacion_individual(pantalla, jugador_actual + 1, len(partida.jugadores))

            elif fase_actual == FASE_RESULTADOS:
                graficos.mostrar_resultados_votacion(pantalla, partida.votos)

            elif fase_actual == FASE_FIN:
                ganador = partida.determinar_ganador()
                if ganador:
                    graficos.mostrar_fin(pantalla, ganador.capitalize())
                else:
                    graficos.mostrar_fin(pantalla, "Empate")

        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()


# ---------------------------------------------------------
# Iniciar el juego
# ---------------------------------------------------------
if __name__ == "__main__":
    bucle_principal()
