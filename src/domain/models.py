from dataclasses import dataclass, field
from typing import Tuple
from datetime import datetime
from enum import Enum

class ActionType(str, Enum):
    AGREGAR_JUGADOR = "AGREGAR_JUGADOR"
    INICIAR_PARTIDA = "INICIAR_PARTIDA"
    RESTAR_TIEMPO = "RESTAR_TIEMPO"
    CAMBIAR_PREGUNTA = "CAMBIAR_PREGUNTA"
    RESPONDER = "RESPONDER"
    FINALIZAR = "FINALIZAR"

@dataclass(frozen=True)
class Player:
    id: int
    nombre: str
    puntaje: int = 0
    respondio: bool = False
    ok: bool | None = None


@dataclass(frozen=True)
class Question:
    id: int
    enunciado: str
    opcion_a: str
    opcion_b: str
    opcion_c: str
    opcion_d: str
    respuesta_correcta: str

@dataclass(frozen=True)
class Event:
    fecha_hora: datetime
    descripcion: str


@dataclass(frozen=True)
class Action:
    tipo: ActionType
    datos: dict = field(default_factory=dict)

@dataclass(frozen=True)
class GameState:
    id_partida: int | None = None
    jugadores: Tuple[Player, ...] = field(default_factory=tuple)
    pregunta_actual: Question | None = None
    ronda: int = 1
    tiempo_restante: int = 20
    juego_activo: bool = False
    historial: Tuple[Event, ...] = field(default_factory=tuple)
