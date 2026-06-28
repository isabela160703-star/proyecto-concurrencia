import asyncio
import pyodbc

class Database:
    def __init__(self):
        self.cadena_conexion = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=localhost;"
            "DATABASE=proyecto2DB;"
            "Trusted_Connection=yes;"
        )
        
    async def ejecutar(self, sql, parametros=()):
        await asyncio.sleep(0.1)
        def consulta():
            try:
                conexion = pyodbc.connect(self.cadena_conexion)
                cursor = conexion.cursor()
                cursor.execute(sql, parametros)
                conexion.commit()
                cursor.close()
                conexion.close()
            except Exception as e:
                # 🚨 EL DETECTIVE: Esto imprimirá letras rojas en la terminal si SQL falla
                print(f"❌ Error SQL silencioso detectado: {e}")
        await asyncio.to_thread(consulta)
        
    async def consultar(self, sql, parametros=()):
        await asyncio.sleep(1)
        def consulta():
            conexion = pyodbc.connect(self.cadena_conexion)
            cursor = conexion.cursor()
            cursor.execute(sql, parametros)
            datos = cursor.fetchall()
            conexion.commit() # 🚨 El commit que salva los datos
            cursor.close()
            conexion.close()
            return datos
        return await asyncio.to_thread(consulta)
        
