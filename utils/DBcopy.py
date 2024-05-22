import psycopg2

try:
    connection = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="@1Xygm352Z+chatboc",
        host="localhost",
        port="5432"
    )
    cursor = connection.cursor()
    cursor.execute("SELECT version();")
    db_version = cursor.fetchone()
    print(f"Conexión exitosa a la base de datos: {db_version}")
    cursor.close()
    connection.close()
except Exception as error:
    print(f"Error al conectar a la base de datos: {error}")
