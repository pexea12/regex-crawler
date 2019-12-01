from tinydb import TinyDB


def init_db(path='db.json'):
    db = TinyDB(path)
    return db
