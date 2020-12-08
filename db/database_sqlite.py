import sqlite3

with sqlite3.connect('db/database.db')as db:
    cursor = db.cursor()


    def search_or_save_users(user_id, name, surname, age, score):
        query = """ CREATE TABLE IF NOT EXISTS users (user_id INTEGER, name TEXT,surname TEXT, age INT, score INT) """
        # query = """ INSERT INTO expenses (id,name) VALUES (1,'Коммуналка') """
        cursor.execute(query)
        query1 = """INSERT INTO users VALUES(user_id,name,surname,age,score) """
        cursor.execute(query1)
