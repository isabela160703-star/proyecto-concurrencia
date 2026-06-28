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
