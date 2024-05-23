from utils.DB import PostgresDB

class DB:
    
    def __init__(self, user_id):
        self.db = PostgresDB(host="localhost", database="postgres", user="postgres", password="276845Ru$")
        self.db.connect()
        self.user_id = user_id
    def saveAnswer(self, id_chat, user_id, content):
        return self.db.insert("security.chat_messages", ["chat_id", "user_id", "message"], [id_chat, user_id, content])
    def saveMetrics(self, id_line, done, done_reason, eval_count, eval_duration, load_duration, model, prompt_eval_count, prompt_eval_duration, total_duration):
        self.db.insert("metrics", ["id_line", "done", "done_reason", "eval_count", "eval_duration", "load_duration", "model", "prompt_eval_count", "prompt_eval_duration", "total_duration"], [id_line, done, done_reason, eval_count, eval_duration, load_duration, model, prompt_eval_count, prompt_eval_duration, total_duration])
    def getChatID(self, user_id):
        return self.db.execute_and_fetchall("SELECT id FROM security.chats WHERE user_id = %s", [user_id])
    def getMetrics(self, id_line):
        return self.db.execute_and_fetchall("SELECT * FROM metrics WHERE id_line = %s", [id_line])
    def getChatMetrics(self, id_chat):
        return self.db.execute_and_fetchall("SELECT * FROM metrics m INNER JOIN chat_lines c ON m.id_line = c.id_line WHERE c.id_chat = %s", [id_chat])
    def close(self):
        self.db.disconnect()
    def __del__(self):
        self.close()
    def saveChunks(self,id_chat,id_user,answer):
        # Save the answer in the database
        message = ""
        for chunk in answer:
            print(chunk)
            message += chunk["message"]["content"]
        print(message)
        print(id_chat)
        print(id_user)
        id_line = self.saveAnswer(id_chat, id_user, message)
        print("Id de linea insertada: ",id_line)
        result = self.db.execute_query("INSERT INTO security.chat_messages (chat_id, user_id, message) VALUES (%s, %s, %s)", [id_chat, id_user, message])
        #print(self.db.getLastID())
        print(result)
        #self.saveMetrics(id_line[0]['id_line'], answer[-1]['done'], answer[-1]['done_reason'], answer[-1]['eval_count'], answer[-1]['eval_duration'], answer[-1]['load_duration'], answer[-1]['model'], answer[-1]['prompt_eval_count'], answer[-1]['prompt_eval_duration'], answer[-1]['total_duration'])
        return result
    def getStream(self, stream, chat_id):
        message = ""
        for chunck in stream:
            print(chunck)
            message += chunck["message"]["content"]
            if chunck["done"]== True and chunck["done_reason"] == "stop":
                self.saveAnswer(chat_id, chunck['message']['role'],message)
    def getUserID(self):
        return self.user_id
    
# db = DB("2f86408f-e2f5-45f7-b9df-58c65f7ce252")
# print(db.getChatID(db.getUserID())[0]['id'])
    