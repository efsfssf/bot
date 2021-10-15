import sqlite3
import threading

class SQLighter_TELEGRAM:

    lock = threading.Lock()
    def __init__(self, database):
        # Define the lock globally
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect(database, check_same_thread=False)
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
            try:
                self.lock.acquire(True)
                return self.cursor.execute("SELECT gr FROM `group_student` WHERE `id_chat` = ?", (id_chat,)).fetchall()
            finally:
                self.lock.release()

    def chat_exists(self, id_chat):
        """Проверяем, есть ли уже беседа в базе"""
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `group_student` WHERE `id_chat` = ?', (id_chat,)).fetchall()
            return bool(len(result))

    def add_chat(self, id_chat, group, subscribe = True):
        """Добавляем новую беседу"""
        with self.connection:
            return self.cursor.execute("INSERT INTO `group_student` (`id_chat`, `gr`,`subscribe`) VALUES(?,?,?)", (id_chat, group, subscribe))