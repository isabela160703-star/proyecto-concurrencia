from dataclasses import replace
from datetime import datetime
from domain.models import *

def update(estado: GameState, accion: Action) -> GameState:

    if accion.tipo == ActionType.AGREGAR_JUGADOR:
        nuevo = Player(id=accion.datos["id"], nombre=accion.datos["nombre"])
        jugadores = estado.jugadores + (nuevo,)
        evento = Event(datetime.now(), f"{nuevo.nombre} ingresó a la partida.")
        return replace(estado, jugadores=jugadores, historial=estado.historial + (evento,))
    
    if accion.tipo == ActionType.INICIAR_PARTIDA:
        preg = accion.datos.get("pregunta")
        evento = Event(datetime.now(), "La partida comenzó.")
        return replace(estado, juego_activo=True, tiempo_restante=20, ronda=1, pregunta_actual=preg, historial=estado.historial + (evento,))

    if accion.tipo == ActionType.RESTAR_TIEMPO:
        return replace(estado, tiempo_restante=max(0, estado.tiempo_restante - 1))

    if accion.tipo == ActionType.CAMBIAR_PREGUNTA:
        preg = accion.datos["pregunta"]
        jugadores = []
        for jug in estado.jugadores:
            if jug.respondio:
                jugadores.append(replace(jug, respondio=False, ok=None))
            else:
                jugadores.append(replace(jug, puntaje=max(0, jug.puntaje - 5), respondio=False, ok=None))
        evento = Event(datetime.now(), "Nueva pregunta.")
        return replace(estado, pregunta_actual=preg, tiempo_restante=20, ronda=estado.ronda + 1, jugadores=tuple(jugadores), historial=estado.historial + (evento,))
    return estado