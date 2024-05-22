from DB import PostgresDB

db = PostgresDB(host="localhost", database="postgres", user="postgres", password="@1Xygm352Z+chatboc")
db.connect()
# Crear tabla de autenticación de usuarios
result = db.execute_query("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, username VARCHAR(255) NOT NULL, password VARCHAR(255) NOT NULL)")
print(result)

# Crear tabla de chats
result = db.execute_query("CREATE TABLE IF NOT EXISTS chats (id SERIAL PRIMARY KEY, id_user INTEGER NOT NULL, name VARCHAR(255) NOT NULL, created_at TIMESTAMP NOT NULL, last_update TIMESTAMP NOT NULL)")
print(result)

# Crear tabla de líneas de chat
result = db.execute_query("CREATE TABLE IF NOT EXISTS chat_lines (id SERIAL PRIMARY KEY, id_chat INTEGER NOT NULL, role VARCHAR(255) NOT NULL, content TEXT NOT NULL)")
print(result)
# Crear tabla de métricas
result = db.execute_query("CREATE TABLE IF NOT EXISTS metrics (id SERIAL PRIMARY KEY, id_line INTEGER NOT NULL, created_at TIMESTAMP NOT NULL, done BOOLEAN NOT NULL, done_reason VARCHAR(255) NOT NULL, eval_count INTEGER NOT NULL, eval_duration INTEGER NOT NULL, load_duration INTEGER NOT NULL, model VARCHAR(255) NOT NULL, prompt_eval_count INTEGER NOT NULL, prompt_eval_duration INTEGER NOT NULL, total_duration INTEGER NOT NULL)")
print(result)

# insertar datos
db.insert("users", ["username", "password"], ["admin", "admin"])
# Obtener datos
result = db.execute_and_fetchall("SELECT * FROM users")
print(result)