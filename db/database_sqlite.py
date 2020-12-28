import sqlite3


def ensure_connection(func):
    def inner(*args, **kwargs):
        with sqlite3.connect('db/database.db') as cons:
            res = func(*args, conn=cons, **kwargs)
        return res

    return inner


@ensure_connection
def init_db(conn, force: bool = False):
    c = conn.cursor()

    if force:
        c.execute('DROP TABLE IF EXISTS users')
        c.execute('DROP TABLE IF EXISTS partners')
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
        id          INTEGER PRIMARY KEY,
        user_id     INTEGER,
        name        TEXT,
        surname     TEXT,
        score       INTEGER
        )
        """)
    c.execute("""
            CREATE TABLE IF NOT EXISTS partners(
            id_user         INTEGER PRIMARY KEY,
            score_referrals INTEGER
            
            )
            """)


@ensure_connection
def cheсk_id(conn, user_id):  # просмотр: записан ли пользователдь в БД
    print(777777777777)
    c = conn.cursor()
    c.execute(
        'SELECT user_id FROM users WHERE user_id = ?', (user_id,)
    )
    print(888888888)
    one_result = c.fetchone()
    if one_result == None:
        return 0
    else:
        return 1



@ensure_connection
def add_user(conn, user_id: int, name: str, surname: str, score: int):
    c = conn.cursor()
    c.execute(
        'INSERT INTO users (user_id,name,surname,score) VALUES(?,?,?,?)', (user_id, name, surname, score))
    c.execute(
        """INSERT INTO partners (score_referrals) VALUES(0)"""
    )
    conn.commit()


@ensure_connection
def add_referral(conn, user_id: int):  # добавление одного реферала в таблицу
    c = conn.cursor()
    score = get_referrals_score(user_id=user_id)
    new_score = score[0] + 1
    c.execute(
        f"""INSERT INTO partners (score_referrals) VALUES('{new_score}')""")
    conn.commit()


@ensure_connection
def get_id(conn, user_id: int):
    c = conn.cursor()
    c.execute(
        'SELECT id FROM users WHERE user_id = ?', (user_id,)
    )
    result = c.fetchone()
    return result


@ensure_connection
def get_referrals_score(conn, user_id):
    new_id = get_id(user_id=user_id)
    print(new_id)
    c = conn.cursor()
    c.execute(
        f"""SELECT score_referrals FROM partners JOIN users
            ON partners.id_user = users.id
         WHERE id =  '{new_id[0]}'"""
    )
    result = c.fetchone()
    print(result)
    return result


@ensure_connection
def check_score(conn, user_id: int):
    c = conn.cursor()
    c.execute(
        'SELECT score FROM users WHERE user_id = ?', (user_id,)
    )
    result = c.fetchone()
    return result


@ensure_connection
def multiple_score(conn, user_id: int, value: int):
    _score = check_score(user_id=user_id)
    new_score = _score[0]
    print(user_id)
    new_score += value
    c = conn.cursor()
    c.execute(
        f"""UPDATE users SET score = '{new_score}' WHERE user_id ='{user_id}'"""
    )
    conn.commit()
