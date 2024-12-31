import sqlite3

class Database:
    def __init__(self):
        self.connection = sqlite3.connect('database.db', check_same_thread=False)
        self.cursor = self.connection.cursor()


    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `users` WHERE `user_id` = ?", (user_id, )).fetchall()
            return bool(len(result))

    def add_user(self, user_id, referer_id=None):
        with self.connection:
            if referer_id is not None:
                print("Не нон")
                return self.cursor.execute("INSERT INTO `users` (`user_id`, `referer_id`) VALUES (?,?)", (user_id, referer_id,))
            else :
                print("нон")
                return self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id, ))

    def count_referers(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT COUNT(`id`) as count FROM `users` WHERE `referer_id` = ?", (user_id, )).fetchone()[0]
