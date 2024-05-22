import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor

class PostgresDB:
    def __init__(self, host, database, user, password, port=5432):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port
            )
            self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            print("Conexión exitosa a la base de datos")
        except psycopg2.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            self.connection = None

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("Conexión cerrada")

    def execute_query(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
        except psycopg2.Error as e:
            print(f"Error ejecutando la consulta: {e}")
            self.connection.rollback()

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def execute_and_fetchall(self, query, params=None):
        self.execute_query(query, params)
        return self.fetchall()

    def execute_and_fetchone(self, query, params=None):
        self.execute_query(query, params)
        return self.fetchone()

    def insert(self, table, columns, values):
        query = sql.SQL("INSERT INTO {table} ({columns}) VALUES ({values})").format(
            table=sql.Identifier(table),
            columns=sql.SQL(', ').join(map(sql.Identifier, columns)),
            values=sql.SQL(', ').join(sql.Placeholder() * len(values))
        )
        self.execute_query(query, values)

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
        self.execute_query(query, list(updates.values()))

    def delete(self, table, condition):
        query = sql.SQL("DELETE FROM {table} WHERE {condition}").format(
            table=sql.Identifier(table),
            condition=sql.SQL(condition)
        )
        self.execute_query(query)

# Uso de la clase
db = PostgresDB(host="localhost", database="postgres", user="postgres", password="@1Xygm352Z+chatboc")
db.connect()
db.execute_query("SELECT version();")
# Ejecutar una consulta
db.execute_query("CREATE TABLE IF NOT EXISTS ejemplo (id SERIAL PRIMARY KEY, nombre VARCHAR(100))")

# Insertar datos
db.insert("ejemplo", ["nombre"], ["Juan"])

# Obtener datos
result = db.execute_and_fetchall("SELECT * FROM ejemplo")
print(result)

# Actualizar datos
db.update("ejemplo", {"nombre": "Juan Actualizado"}, "id = 1")

# Borrar datos
db.delete("ejemplo", "id = 1")

# Cerrar la conexión
db.disconnect()
