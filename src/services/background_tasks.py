import asyncio
from domain.models import Action, ActionType

async def temporizador(game):
    while True:
        estado = await game.get_state()
        if estado.juego_activo:
            await asyncio.sleep(1)
            await game.dispatch(Action(ActionType.RESTAR_TIEMPO))
        else:
            await asyncio.sleep(1)

async def cambio_pregunta(game, preguntas):
    indice = 0
    while True:
        estado = await game.get_state()
        # Si la partida no ha empezado, no hagas nada y espera
        if not estado.juego_activo:
            await asyncio.sleep(1)
            continue
            
        # Si ya empezó, carga la pregunta si está vacía o si se acabó el tiempo
        if estado.pregunta_actual is None or estado.tiempo_restante == 0:
            if indice >= len(preguntas):
                await game.dispatch(Action(ActionType.FINALIZAR))
                break
            preg = preguntas[indice]
            indice += 1
            await game.dispatch(Action(ActionType.CAMBIAR_PREGUNTA, {"pregunta": preg}))
        await asyncio.sleep(1)

async def anunciador_tiempo(game):
    while True:
        estado = await game.get_state()
        if estado.juego_activo and estado.tiempo_restante == 10:
            await game.dispatch(Action(ActionType.RESPONDER, {"id": 0, "correcta": False, "mensaje": "¡Quedan 10 segundos!"}))
        await asyncio.sleep(1)

async def iniciar_corrutinas(game, preguntas):
    await asyncio.gather(
        temporizador(game),
        cambio_pregunta(game, preguntas),
        anunciador_tiempo(game)
    )