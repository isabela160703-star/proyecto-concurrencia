from infrastructure.database import Database
from domain.models import Question

class Repository:
    def __init__(self):
        self.db = Database()

    async def obtener_preguntas(self):
        sql = "SELECT id_pregunta, pregunta, opcion_a, opcion_b, opcion_c, opcion_d, respuesta_correcta FROM Preguntas"
        filas = await self.db.consultar(sql)
        preguntas = []
        for fila in filas:
            preguntas.append(Question(
                id=fila[0], enunciado=fila[1], opcion_a=fila[2], 
                opcion_b=fila[3], opcion_c=fila[4], opcion_d=fila[5], 
                respuesta_correcta=fila[6].strip()
            ))
        return preguntas
        
     async def guardar_jugador(self, id_jug, nom):
        sql = """
        IF NOT EXISTS (SELECT * FROM Jugadores WHERE nombre = ?)
        BEGIN
            SET IDENTITY_INSERT Jugadores ON;
            INSERT INTO Jugadores (id_jugador, nombre) VALUES (?, ?);
            SET IDENTITY_INSERT Jugadores OFF;
        END
        """
        await self.db.ejecutar(sql, (nom, id_jug, nom))

async def crear_partida(self):
        sql = "INSERT INTO Partidas (fecha_inicio, estado) OUTPUT INSERTED.id_partida VALUES (GETDATE(), 'ACTIVA')"
        datos = await self.db.consultar(sql)
        return datos[0][0]


async def finalizar_partida(self, id_partida, duracion_segundos):
        sql = "UPDATE Partidas SET fecha_fin = GETDATE(), duracion_segundos = ?, estado = 'FINALIZADA' WHERE id_partida = ?"
        await self.db.ejecutar(sql, (duracion_segundos, id_partida))


async def guardar_respuesta(self, id_partida, id_jugador, id_pregunta, correcta):
        sql = "INSERT INTO Respuestas (id_partida, id_jugador, id_pregunta, correcta) VALUES (?, ?, ?, ?)"
        await self.db.ejecutar(sql, (id_partida, id_jugador, id_pregunta, correcta))


async def guardar_evento(self, id_partida, descripcion):
        sql = "INSERT INTO HistorialEventos (id_partida, descripcion) VALUES (?, ?)"
        await self.db.ejecutar(sql, (id_partida, descripcion))


