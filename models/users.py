from app.models import db_connect, db_close
from hashlib import md5


def get_user_id(id=0):
	"""Returns the record(tuple) of one user with identifiers id(int, bigint). """
	cnn = db_connect()
	cur = cnn.cursor()
	cur.execute(f'SELECT * FROM users WHERE id = {id}')
	res = cur.fetchone()
	db_close(cnn)
	
	if res is None:
		res = ()
	return res


def get_users_par(**dargs):
	"""returns user records(dictionary) selected according to the conditions passed in parameter(dict)"""
	cnn = db_connect()
	cur = cnn.cursor()
	#db_close(cnn)
	res = dargs
	sql = "SELECT * FROM users"
	i = 1

	for k in dargs.keys():
		if i == 1:
			sql += " WHERE " + k + "=:" + k
		else:
			sql += " AND " + k + "=:" + k
		i += 1	
	try:
		cur.execute(sql, dargs)
		res = cur.fetchall()
	except:
		res = []

	db_close(cnn)
	return res


def get_users_sql(sql=''):
	"""Returns user records(dictionary) on sql statment."""
	cnn = db_connect()
	cur = cnn.cursor()
	try:
		cur.execute(sql)
		res = cur.fetchall()
	except:
		print("Ошибка выполнения запроса")
		res = []
	
	db_close(cnn)
	return res


def add_user(**user):
	"""добавление записи в БД. Используется для регистрации, поэтому обязательные поля проверяются в форме ввода.
	Остальные поля проверяются на правильность типов данных здесь."""
	#проверка обязательных полей: alias,password,email
	#alias.проверка на размер (3-16) и уникальность
	alias = user.get('alias') 
	if alias == None:
		res = 'Не указан логин...'
		return res
	else:
		l = len(alias)
		if l < 3 or l > 16:
			res = 'Логин должен быть не менее 3 и не более 16 символов'
			return res
		else:
			if len(get_users_par(alias=alias)) > 0:
				res = f'Логин "{alias}" кем-то занят. Выберете другой логин'
				return res
	#password. здесь условие на значение и преобразование в MD5
	password = user.get('password')
	if password == None:
		res = 'Не указан пароль...'
		return res
	else:
		l = len(password)
		if l < 8:
			res = 'Пароль должен состоять не менее чем из 8 символов'
			return res
		
	#email проверка на корректность...
	email = user.get('password')
	if email != None and str('email') != "email":#некорректный email
		res = 'введен неверный email'
		return res

	#остальные поля пока не проверем...
	#хеширование пароля
	user['password'] = md5(password.encode()).hexdigest()
	
	i = 1
	for k in user.keys():
		if i == 1:
			fields = k; values = ':' + k
		else:
			fields += ', ' + k; values += ', :' + k
		i += 1
	
	cnn = db_connect();	cur = cnn.cursor()
	sql = "INSERT INTO users (" + fields + ") VALUES (" + values + ");"
	cur.execute(sql, user)
	cnn.commit()
	res = cur.lastrowid
	return res
	
	db_close(cnn)


def upd_user(**user):
	"""Uodate one user record. parametr - dictionary of updating fields. 
	On success return id updatted record. Enath - message about ancorrect data"""
	uid = user.get('id')
	if uid == None:
		res = 'Не указан идентификатор записи для изменения'
		return res
	else:
		if type(uid) != int:
			res = 'Идентификатор пользователя должен быть целым числом'
			return res
		else:
			
			if len(get_user_id(uid)) == 0:
				res = 'Пользователь с идентификаторам "' + str(uid) + '" не существует'
				return res

	alias = user.get('alias') 
	if alias == None:
		res = 'Не указан логин...'
		return res
	else:
		l = len(alias)
		if l < 3 or l > 16:
			res = 'Логин должен быть не менее 3 и не более 16 символов'
			return res
		else:
			if len(get_users_sql(f"SELECT id FROM users WHERE id != {uid} and alias = '{alias}'")) > 0:
				res = f'Логин "{alias}" кем-то занят. Выберете другой логин'
				return res
	#password. здесь условие на значение и преобразование в MD5
	password = user.get('password')
	if password == None:
		res = 'Не указан пароль...'
		return res
	else:
		l = len(password)
		if l < 8:
			res = 'Пароль должен состоять не менее чем из 8 символов'
			return res
	
	#email проверка на корректность...
	email = user.get('password')
	if email != None and str('email') != "email":#некорректный email
		res = 'введен неверный email'
		return res
	#остальные поля пока не проверем...
	#хеширование пароля
	user['password'] = md5(password.encode()).hexdigest()

	i = 1
	value = ''
	for k in user.keys():
		if i == 1 and k!='id':
			res = 'Идентификатор должен быть указан на месте 1 параметра'
			return res
		if i == 2:
			value = k + '=:' + k
		elif i > 2:
			value += ', ' + k + '=:' + k
		i += 1

	sql ="UPDATE users SET " + value + " WHERE id=:id"
	cnn = db_connect()
	cnn.execute(sql, user)
	cnn.commit()
	return uid
	db_close(cnn)


def del_user(id):
	if len(get_user_id(id)) == 0:
		res = 'Пользователь с идентификаторам "' + str(id) + '" не существует'
		return res
	else:
		cnn = db_connect()
		cnn.execute(f"DELETE FROM users WHERE id={id}")
	cnn.commit()
	return id


def login_user(**dargs):
	sql = "SELECT id FROM users"
	alias = dargs['alias']
	cnn = db_connect()
	cur = cnn.cursor()
	cur.execute("SELECT id, password FROM users WHERE alias=:alias", [alias])
	row = cur.fetchone()
	res = 0
	if row:
		res = row[0]
		password = dargs['password']
		password = md5(password.encode()).hexdigest()
		if password != row[1]:
			return "Введен неверный пароль"
	else:
		return "Пользователь не существует"

	return res

