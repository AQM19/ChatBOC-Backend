def escape_sql(value) -> str:
    return value.replace("'", "''").replace("\\", "\\\\")

# Chats
INSERT_CHAT = lambda user_id, chat_name: f"INSERT INTO chats (user_id, name) VALUES ( '{str(user_id)}' , '{str(escape_sql(chat_name))}') RETURNING id"
DELETE_CHAT = lambda chat_id: f"DELETE FROM chats WHERE id = '{str(chat_id)}'"

# Chat_messages
GET_CHAT_MESSAGES = lambda chat_id, user_id : f"SELECT * FROM chat_messages WHERE chat_id = '{str(chat_id)}' AND user_id = '{str(user_id)}' ORDER BY created_at DESC"
INSERT_QUESTION = lambda chat_id, user_id, question: f"INSERT INTO chat_messages (chat_id, user_id, message, is_response) values ('{str(chat_id)}', '{str(user_id)}', '{str(question)}', False)"
INSERT_RESPONSE = lambda chat_id, user_id, response: f"INSERT INTO chat_messages (chat_id, user_id, message, is_response) values ('{str(chat_id)}', '{str(user_id)}', '{str(escape_sql(response))}', True)"