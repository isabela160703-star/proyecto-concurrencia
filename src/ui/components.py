from reactpy import component, html
from domain.models import Question

# ==========================================
# Encabezado (Ronda y Temporizador)
# ==========================================
@component
def Header(rnd: int, tmp: int):
    color_tmp = "red" if tmp <= 5 else "black"
    
    return html.div(
        {"style": {"display": "flex", "justifyContent": "space-between", "padding": "10px", "borderBottom": "2px solid #ccc"}},
        html.h2(f"Ronda: {rnd}"),
        html.h2({"style": {"color": color_tmp}}, f"⏳ {tmp}s")
    )

# ==========================================
# Tarjeta de Pregunta y Opciones
# ==========================================
@component
def QuestionCard(preg: Question | None, on_resp):
    if not preg:
        return html.div(
            {"style": {"textAlign": "center", "padding": "20px"}},
            html.h3("⏳ Preparando siguiente pregunta...")
        )

    def btn_opcion(letra: str, texto: str):
        es_correcta = (letra == preg.respuesta_correcta)
        
        async def al_hacer_click(event):
            await on_resp(es_correcta)

        return html.button(
            {
                "key": f"opcion-{letra}", # 🚨 LLAVE ÚNICA DE TEXTO
                "on_click": al_hacer_click,
                "style": {
                    "margin": "10px", "padding": "15px", "fontSize": "16px", 
                    "cursor": "pointer", "width": "45%"
                }
            },
            f"{letra}) {texto}"
        )

    return html.div(
        {"style": {"textAlign": "center", "margin": "20px 0"}},
        html.h2(preg.enunciado),
        html.div(
            {"style": {"display": "flex", "flexWrap": "wrap", "justifyContent": "center"}},
            btn_opcion("A", preg.opcion_a),
            btn_opcion("B", preg.opcion_b),
            btn_opcion("C", preg.opcion_c),
            btn_opcion("D", preg.opcion_d)
        )
    )

# ==========================================
# Lista de Jugadores (Ranking en vivo)
# ==========================================
@component
def PlayerList(jugadores):
    def render_jug(jug):
        if jug.respondio:
            estado_resp = "✅ ¡Correcto!" if jug.ok else "❌ Falló"
        else:
            estado_resp = "⌛ Pensando..."

        return html.li(
            # 🚨 LLAVE ESTRICTA DE TEXTO PARA QUE REACTPY NO COLAPSE
            {"key": f"jugador-{jug.id}", "style": {"padding": "5px", "fontSize": "18px"}},
            html.strong(jug.nombre), 
            f" - Puntos: {jug.puntaje} - [{estado_resp}]"
        )

    return html.div(
        {"style": {"border": "1px solid #ccc", "padding": "15px", "borderRadius": "8px"}},
        html.h3("👥 Jugadores en Sala"),
        html.ul([render_jug(j) for j in jugadores])
    )