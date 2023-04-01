import sqlite3

db = sqlite3.connect('formulas.db', check_same_thread=False)
cur = db.cursor()


def create_table():
    cur.execute('CREATE TABLE formulas(title, formula_types)')


def insert_item(item):
    cur.execute(f'INSERT INTO formulas VALUES {item}')
    db.commit()


def get_items():
    res = cur.execute(f'SELECT * FROM formulas')
    return res.fetchall()


def get_similar_items(user_text):
    res = cur.execute(f"SELECT * FROM formulas WHERE title LIKE '%_{user_text[1:-1]}_%' LIMIT 2")
    return res.fetchall()


def find_formula(user_text):
    res = cur.execute(f"SELECT * FROM formulas WHERE formula_types LIKE '%_{user_text.replace('^', '**')}_%'")
    return res.fetchall()


def letter_exchange(user_text):
    res = cur.execute(f"SELECT letter FROM CI WHERE title LIKE '{user_text.capitalize().replace(' ', '')}'")
    return res.fetchall()[0][0]

