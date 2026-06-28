import random
import asyncio
from reactpy import component, html, use_state, use_effect
from ui.components import Header, QuestionCard, PlayerList
from domain.models import Action, ActionType

@component
def GameBoard(game_manager):
    est, set_est = use_state(game_manager._state)
    session_id, set_session_id = use_state(None)
    nom, set_nom = use_state("")

    # ==========================================
    # LECTURA CONTINUA SEGURA (POLLING)
    # ==========================================
    @use_effect
    async def sync_loop():
        corriendo = True
        async def loop():
            while corriendo:
                nuevo_estado = await game_manager.get_state()
                set_est(nuevo_estado)
                await asyncio.sleep(0.5)
        
        tarea = asyncio.create_task(loop())
        
        def cleanup():
            nonlocal corriendo
            corriendo = False
            tarea.cancel()
        return cleanup

    async def btn_entrar(e):
        if not nom: return
        nuevo_id = random.randint(1000, 9999)
        resp = await game_manager.dispatch(Action(ActionType.AGREGAR_JUGADOR, {"id": nuevo_id, "nombre": nom}))
        set_session_id(resp["id"])

    async def btn_iniciar(e):
        await game_manager.dispatch(Action(ActionType.INICIAR_PARTIDA))

    async def on_resp(correcta):
        if not session_id: return
        await game_manager.dispatch(Action(ActionType.RESPONDER, {"id": session_id, "correcta": correcta, "mensaje": f"{nom} respondió."}))

    # ==========================================
    # RENDERIZADO DIRECTO (Sin contenedores extra)
    # ==========================================
    if est is None:
        return html.div("Cargando tablero...")

    soy_jugador = session_id is not None and any(j.id == session_id for j in est.jugadores)

    # 1. PANTALLA DE INGRESO
    if not soy_jugador:
        return html.div(
            {"style": {"textAlign": "center", "marginTop": "100px", "fontFamily": "sans-serif"}},
            html.h2("🎮 ¡Bienvenido a la Trivia!"),
            html.input({
                "type": "text", "placeholder": "Ingresa tu nombre",
                "on_change": lambda e: set_nom(e["target"]["value"]),
                "style": {"padding": "10px", "fontSize": "16px"}
            }),
            html.button({"on_click": btn_entrar, "style": {"padding": "10px 20px", "marginLeft": "10px", "cursor": "pointer"}}, "Entrar a la Sala")
        )

    # 2. PANTALLA DE SALA DE ESPERA
    if not est.juego_activo and est.ronda == 1:
        return html.div(
            {"style": {"textAlign": "center", "marginTop": "50px", "fontFamily": "sans-serif"}},
            html.h1(f"👋 Hola {nom}, estás en la sala de espera."),
            html.p("Esperando a que se unan más jugadores..."),
            html.button(
                {"on_click": btn_iniciar, "style": {"padding": "15px 30px", "fontSize": "18px", "backgroundColor": "#4CAF50", "color": "white", "border": "none", "borderRadius": "5px", "cursor": "pointer", "marginTop": "20px"}}, 
                "▶️ Comenzar Partida"
            ),
            html.div({"style": {"marginTop": "30px"}}, PlayerList(est.jugadores))
        )

    # 3. PANTALLA DE FIN DE PARTIDA
    if not est.juego_activo and est.ronda > 1:
        ganadores = sorted(est.jugadores, key=lambda x: x.puntaje, reverse=True)
        return html.div(
            {"style": {"textAlign": "center", "marginTop": "50px", "fontFamily": "sans-serif"}},
            html.h1("🏆 ¡Partida Finalizada!"),
            html.ul(
                {"style": {"listStyleType": "none", "padding": "0"}}, 
                # 🚨 LA CORRECCIÓN PURA: f"final-{j.id}"
                [html.li({"key": f"final-{j.id}", "style": {"fontSize": "20px", "margin": "10px"}}, f"🏅 {j.nombre}: {j.puntaje} pts") for j in ganadores]
            )
        )

    # 4. TABLERO PRINCIPAL DE JUEGO SIMULTÁNEO
    return html.div(
        {"style": {"maxWidth": "700px", "margin": "0 auto", "fontFamily": "sans-serif"}},
        Header(est.ronda, est.tiempo_restante),
        QuestionCard(est.pregunta_actual, on_resp),
        PlayerList(est.jugadores)
    )