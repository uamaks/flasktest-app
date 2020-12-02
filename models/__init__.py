import sqlite3


def db_connect(rf = False):
	cnn = sqlite3.connect('app\\test.db')
	if rf: cnn.row_factory = sqlite3.Row
	return cnn


def db_close(dbcnn):
    dbcnn.close()
    pass