import sqlite3


def db_connect():
    # print ('open')
    return sqlite3.connect('app\\test.db')


def db_close(dbcnn):
    dbcnn.close()
    pass