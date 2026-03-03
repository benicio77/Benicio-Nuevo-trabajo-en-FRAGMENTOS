# juego.py

import json


def guardar_partida(partida, nombre_archivo=None):
    """Escribe los datos básicos de la partida a un archivo JSON.

    No modifica el estado de la partida en memoria, por lo que no afecta el
    flujo del juego. Se utiliza como un "elemento aleatorio" para que el usuario
    pueda generar un guardado sin que nada cambie durante la ejecución.

    Retorna la ruta del archivo creado si tuvo éxito, o ``None`` si ocurrió un
    error al escribir.
    """

    if nombre_archivo is None:
        nombre_archivo = f"{partida.nombre_partida}_guardado.json"

    datos = {
        "nombre_partida": partida.nombre_partida,
        "numero_jugadores": partida.numero_jugadores,
        "jugadores": partida.jugadores,
        "roles_asignados": partida.roles_asignados,
        "palabra_secreta": partida.palabra_secreta,
        "votos": partida.votos,
        "ronda_actual": partida.ronda_actual,
    }

    try:
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
        return nombre_archivo
    except Exception:
        return None
