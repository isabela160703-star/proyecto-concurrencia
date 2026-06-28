import asyncio
from reactpy import component, run, use_effect
from services.game_manager import GameManager
from services.background_tasks import iniciar_corrutinas
from infrastructure.repository import Repository
from ui.views import GameBoard

repo = Repository()
gestor = GameManager(repo)
motor_iniciado = False

@component
def App():
    @use_effect
    async def arrancar_motor():
        global motor_iniciado
        if not motor_iniciado:
            motor_iniciado = True
            print("⏳ Conectando a BD para extraer preguntas...")
            preg_db = await repo.obtener_preguntas()
            print(f"✅ ¡{len(preg_db)} preguntas cargadas!")

            # Iniciamos las tareas de fondo, pero estarán en reposo hasta que presionen "Comenzar"
            asyncio.create_task(iniciar_corrutinas(gestor, preg_db))

    return GameBoard(gestor)

if __name__ == "__main__":
    print("🚀 Levantando servidor ReactPy...")
    run(App)