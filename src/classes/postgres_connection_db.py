from dotenv import load_dotenv
from psycopg2 import sql
import os
import psycopg2

class PostgresConnectionBD:
    
    def __init__(self):
        """
        Inicializa la conexión a la base de datos PostgreSQL.
        """
        load_dotenv()
        self.hostname = os.getenv('DB_HOSTNAME')
        self.username = os.getenv('DB_USERNAME')
        self.password = os.getenv('DB_PASSWORD')
        self.database = os.getenv('DB_DATABASE')
        self.connection = None
        self.cursor = None
        self.connected = False
    
    def connect(self):
        """
        Establece una conexión a la base de datos PostgreSQL.
        """
        try:
            self.connection = psycopg2.connect(
                host=self.hostname,
                user=self.username,
                password=self.password,
                database=self.database
            )
            self.cursor = self.connection.cursor()
            print('Conexión exitosa a la base de datos')
            self.connected = True
        except psycopg2.Error as error:
            print('Error al conectarse a la base de datos: {}'.format(error))
            
    def disconnect(self):
        """
        Cierra la conexión actual a la base de datos PostgreSQL.
        """
        if self.connection:
            self.connection.close()
            self.connected = False
            print('Desconexión exitosa de la base de datos')
            
    def is_connected(self):
        """
        Verifica si hay una conexión activa a la base de datos PostgreSQL.

        Returns:
            bool: True si está conectado, False de lo contrario.
        """
        return self.connected
    
    def __execute_query(self, query, params=None):
        """
        Ejecuta una consulta SQL en la base de datos PostgreSQL.

        Args:
            query (str): Consulta SQL a ejecutar.
            params (tuple, opcional): Parámetros para la consulta SQL. Por defecto es None.
        """
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
        except psycopg2.Error as e:
            print(f"Error ejecutando la consulta: {e}")
            self.connection.rollback()
            
    def __fetch_all(self):
        """
        Obtiene todas las filas resultantes de la última consulta.

        Returns:
            list: Lista de tuplas representando las filas.
        """
        return self.cursor.fetchall()

    def __fetch_one(self):
        """
        Obtiene la primera fila resultante de la última consulta.

        Returns:
            tuple: Tupla representando la fila.
        """
        return self.cursor.fetchone()

    def __execute_and_fetch_all(self, query, params=None):
        """
        Ejecuta una consulta SQL y obtiene todas las filas resultantes.

        Args:
            query (str): Consulta SQL a ejecutar.
            params (tuple, opcional): Parámetros para la consulta SQL. Por defecto es None.

        Returns:
            list: Lista de tuplas representando las filas.
        """
        self.__execute_query(query, params)
        return self.__fetch_all()

    def __execute_and_fetch_one(self, query, params=None):
        """
        Ejecuta una consulta SQL y obtiene la primera fila resultante.

        Args:
            query (str): Consulta SQL a ejecutar.
            params (tuple, opcional): Parámetros para la consulta SQL. Por defecto es None.

        Returns:
            tuple: Tupla representando la fila.
        """
        self.__execute_query(query, params)
        return self.__fetch_one()

    def select(self, table, columns, condition):
        """
        Ejecuta una consulta SELECT en la base de datos.

        Args:
            table (str): Nombre de la tabla.
            columns (list): Lista de nombres de columnas a seleccionar.
            condition (str): Condición de la consulta.

        Returns:
            list: Lista de tuplas representando las filas seleccionadas.
        """
        query = sql.SQL("SELECT {columns} FROM {table} WHERE {condition}").format(
            columns=sql.SQL(', ').join(map(sql.Identifier, columns)),
            table=sql.Identifier(table),
            condition=sql.SQL(condition)
        )
        
        return self.__execute_and_fetch_all(query)

    def insert(self, table, columns, values):        
        """
        Ejecuta una consulta INSERT en la base de datos.

        Args:
            table (str): Nombre de la tabla.
            columns (list): Lista de nombres de columnas.
            values (list): Lista de valores a insertar.

        Returns:
            tuple: Tupla representando la fila insertada.
        """
        query = sql.SQL("INSERT INTO {table} ({columns}) VALUES ({values})").format(
            table=sql.Identifier(table),
            columns=sql.SQL(', ').join(map(sql.Identifier, columns)),
            values=sql.SQL(', ').join(sql.Placeholder() * len(values))
        )
        
        return self.__execute_and_fetch_one(query, values)
    
    def insert_with_return(self, table, columns, values):
        """
        Ejecuta una consulta INSERT en la base de datos y devuelve el ID de la fila insertada.

        Args:
            table (str): Nombre de la tabla.
            columns (list): Lista de nombres de columnas.
            values (list): Lista de valores a insertar.

        Returns:
            tuple: Tupla representando el ID de la fila insertada.
        """
        query = sql.SQL("INSERT INTO {table} ({columns}) VALUES ({values}) RETURNING id").format(
            table=sql.Identifier(table),
            columns=sql.SQL(', ').join(map(sql.Identifier, columns)),
            values=sql.SQL(', ').join(sql.Placeholder() * len(values))
        )
        
        return self.__execute_and_fetch_one(query, values)
    
    def insert_with_no_result(self, table, columns, values):        
        """
        Ejecuta una consulta INSERT en la base de datos sin devolver resultados.

        Args:
            table (str): Nombre de la tabla.
            columns (list): Lista de nombres de columnas.
            values (list): Lista de valores a insertar.
        """
        query = sql.SQL("INSERT INTO {table} ({columns}) VALUES ({values})").format(
            table=sql.Identifier(table),
            columns=sql.SQL(', ').join(map(sql.Identifier, columns)),
            values=sql.SQL(', ').join(sql.Placeholder() * len(values))
        )
        
        self.__execute_query(query, values)

    def update(self, table, updates, condition):
        """
        Ejecuta una consulta UPDATE en la base de datos.

        Args:
            table (str): Nombre de la tabla.
            updates (dict): Diccionario de columnas a actualizar y sus nuevos valores.
            condition (str): Condición de la consulta.

        Returns:
            tuple: Tupla representando la fila actualizada.
        """
        set_clause = sql.SQL(', ').join(
            sql.SQL("{} = {}").format(sql.Identifier(k), sql.Placeholder())
            for k in updates.keys()
        )
        query = sql.SQL("UPDATE {table} SET {set_clause} WHERE {condition}").format(
            table=sql.Identifier(table),
            set_clause=set_clause,
            condition=sql.SQL(condition)
        )
        return self.__execute_and_fetch_one(query, list(updates.values()))