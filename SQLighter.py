import sqlite3

class SQLighter:

    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS group_student(
        id INTEGER PRIMARY KEY,
        id_chat INTEGER,
	gr TEXT,
	subscribe bool
        );""")
        self.connection.commit()

    def get_chats(self, id_chat):
        """Получаем все группы студентов"""
        with self.connection:
            return self.cursor.execute("SELECT * FROM `group_student` WHERE `id_chat` = ?", (id_chat,)).fetchall()

    def get_group(self, id_chat):
        """Получаем все группы студентов"""
        with self.connection:
            return self.cursor.execute("SELECT gr FROM `group_student` WHERE `id_chat` = ?", (id_chat,)).fetchall()

    def chat_exists(self, id_chat):
        """Проверяем, есть ли уже беседа в базе"""
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `group_student` WHERE `id_chat` = ?', (id_chat,)).fetchall()
            return bool(len(result))

    def add_chat(self, id_chat, group, subscribe = True):
        """Добавляем новую беседу"""
        with self.connection:
            return self.cursor.execute("INSERT INTO `group_student` (`id_chat`, `gr`,`subscribe`) VALUES(?,?,?)", (id_chat, group, subscribe))