from dataclasses import dataclass, field
from typing import Tuple

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