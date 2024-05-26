import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import OperationalError, sql

class ConnectionBD:
    
    def __init__(self):
        load_dotenv()
        self.hostname = os.getenv('DB_HOSTNAME')
        self.username = os.getenv('DB_USERNAME')
        self.password = os.getenv('DB_PASSWORD')
        self.database = os.getenv('DB_DATABASE')
        self.connection = None
        self.cursor = None
        self.connected = False
    
    def connect(self):
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
        if self.connection:
            self.connection.close()
            self.connected = False
            print('Desconexión exitosa de la base de datos')
            
    def is_connected(self):
        return self.connected
    
    def __execute_query(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
        except psycopg2.Error as e:
            print(f"Error ejecutando la consulta: {e}")
            self.connection.rollback()
            
    def __fetch_all(self):
        return self.cursor.fetchall()

    def __fetch_one(self):
        return self.cursor.fetchone()

    def __execute_and_fetch_all(self, query, params=None):
        self.__execute_query(query, params)
        return self.__fetch_all()

    def __execute_and_fetch_one(self, query, params=None):
        self.__execute_query(query, params)
        return self.__fetch_one()

    def select(self, table, columns, condition):
        query = sql.SQL("SELECT {columns} FROM {table} WHERE {condition}").format(
            columns=sql.SQL(', ').join(map(sql.Identifier, columns)),
            table=sql.Identifier(table),
            condition=sql.SQL(condition)
        )
        
        return self.__execute_and_fetch_one(query)

    def insert(self, table, columns, values):        
        query = sql.SQL("INSERT INTO {table} ({columns}) VALUES ({values})").format(
            table=sql.Identifier(table),
            columns=sql.SQL(', ').join(map(sql.Identifier, columns)),
            values=sql.SQL(', ').join(sql.Placeholder() * len(values))
        )
        
        return self.__execute_and_fetch_one(query, values)
    
    def insert_with_return(self, table, columns, values):
        query = sql.SQL("INSERT INTO {table} ({columns}) VALUES ({values}) RETURNING id").format(
            table=sql.Identifier(table),
            columns=sql.SQL(', ').join(map(sql.Identifier, columns)),
            values=sql.SQL(', ').join(sql.Placeholder() * len(values))
        )
        
        return self.__execute_and_fetch_one(query, values)
    
    def insert_with_no_result(self, table, columns, values):        
        query = sql.SQL("INSERT INTO {table} ({columns}) VALUES ({values})").format(
            table=sql.Identifier(table),
            columns=sql.SQL(', ').join(map(sql.Identifier, columns)),
            values=sql.SQL(', ').join(sql.Placeholder() * len(values))
        )
        
        self.__execute_query(query, values)

    def update(self, table, updates, condition):
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

    def delete(self, table, condition):
        query = sql.SQL("DELETE FROM {table} WHERE {condition}").format(
            table=sql.Identifier(table),
            condition=sql.SQL(condition)
        )
        return self.__execute_and_fetch_one(query)
    
    def set_query(self, query):
        return self.__execute_and_fetch_all(sql.SQL(query))
    
    def set_query_and_no_return(self, query):
        self.__execute_query(sql.SQL(query))