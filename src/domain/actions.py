from dataclasses import replace
from datetime import datetime
from domain.models import *

def update(estado: GameState, accion: Action) -> GameState:

    if accion.tipo == ActionType.AGREGAR_JUGADOR:
        nuevo = Player(id=accion.datos["id"], nombre=accion.datos["nombre"])
        jugadores = estado.jugadores + (nuevo,)
        evento = Event(datetime.now(), f"{nuevo.nombre} ingresó a la partida.")
        return replace(estado, jugadores=jugadores, historial=estado.historial + (evento,))

    return estado