from app.models import db_connect, db_close


def get_booklist():
    cnn = db_connect()
    cur = cnn.cursor()
    cur.execute('SELECT * FROM books')
    res = cur.fetchall()
    db_close(cnn)
    if res is None:
        res = []
    return res