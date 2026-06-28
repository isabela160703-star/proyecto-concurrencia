import asyncio
from dataclasses import replace
from domain.models import GameState, Action, ActionType
from domain.actions import update

class GameManager:
    def __init__(self, repo):
        self._state = GameState()
        self._lock = asyncio.Lock()
        self._listeners = []
        self.repo = repo 

    def subscribe(self, listener):
        self._listeners.append(listener)
        return lambda: self._listeners.remove(listener)

    async def dispatch(self, accion: Action):
        async with self._lock:
            est_viejo = self._state
            est_nuevo = update(self._state, accion)
            nuevo_id = None

            if accion.tipo == ActionType.AGREGAR_JUGADOR:
                id_jug = accion.datos["id"]
                nom = accion.datos["nombre"]
                asyncio.create_task(self.repo.guardar_jugador(id_jug, nom))
                nuevo_id = id_jug  

            # 🚨 I/O NO BLOQUEANTE: La BD se actualiza en el fondo sin congelar el juego
            elif accion.tipo == ActionType.INICIAR_PARTIDA:
                async def iniciar_bd():
                    id_p = await self.repo.crear_partida()
                    async with self._lock:
                        self._state = replace(self._state, id_partida=id_p)
                asyncio.create_task(iniciar_bd())

            elif accion.tipo == ActionType.FINALIZAR and est_viejo.id_partida:
                dur = (est_nuevo.ronda - 1) * 20
                id_partida_local = est_viejo.id_partida
                jugadores_local = est_nuevo.jugadores
                
                async def finalizar_bd():
                    await self.repo.finalizar_partida(id_partida_local, dur)
                    max_pts = max([j.puntaje for j in jugadores_local]) if jugadores_local else 0
                    for jug in jugadores_local:
                        es_ganador = (jug.puntaje == max_pts and max_pts > 0)
                        
                        # 🚨 LA CORRECCIÓN: Ahora pasamos jug.nombre en lugar de jug.id
                        await self.repo.guardar_ranking(jug.nombre, jug.puntaje, es_ganador)
                        
                asyncio.create_task(finalizar_bd())

            if est_nuevo.id_partida and len(est_nuevo.historial) > len(est_viejo.historial):
                ult_ev = est_nuevo.historial[-1]
                asyncio.create_task(self.repo.guardar_evento(est_nuevo.id_partida, ult_ev.descripcion))

            self._state = est_nuevo

        # Notificamos de forma segura aislando errores de clientes desconectados
        for listener in list(self._listeners):
            try:
                listener(self._state)
            except Exception:
                pass

        return {"estado": self._state, "id": nuevo_id}

    async def get_state(self):
        async with self._lock:
            return self._state